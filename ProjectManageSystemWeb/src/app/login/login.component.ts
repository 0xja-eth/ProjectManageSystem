import {Component, EventEmitter, forwardRef, Inject, Input, OnInit, Output} from '@angular/core';
import {InputData} from '../input-field/input_data';
import {AbstractControl, FormBuilder, FormControl, FormGroup} from '@angular/forms';

import {Config} from '../utils/config'

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})

export class LoginComponent implements OnInit {

  @Input() type: "Login" | "Register" | "Forget" = "Login";

  @Output() onSubmit = new EventEmitter();

  inputData = {
    username: new InputData("用户名","", "Text", {
      placeholder: "请输入你的用户名", maxLength: Config.UnLength, required: true,

    }),
    password: new InputData("密码","","Password",{
      placeholder: "请输入你的密码", maxLength: Config.PwdLength[1], required: true,
    }),
    new_password: new InputData("密码","","Password",{
      placeholder: "请输入你新的密码", maxLength: Config.PwdLength[1], required: true,
    }),
    rept_password: new InputData("重复密码","","Password",{
      placeholder: "请再次输入密码", maxLength: Config.PwdLength[1], required: true,
    }),
    email: new InputData("邮箱","","Text",{
      placeholder: "请输入邮箱", button: null, required: true,
    }),
    code: new InputData("验证码","","Text",{
      placeholder: "请输入 "+Config.CodeLength+" 位验证码", maxLength: Config.CodeLength, button: "发送验证码", required: true,
    }),
  };

  inputFilter = {
    "Login": ["登陆", ['username', 'password']],
    "Register": ["注册", ['username', 'password', 'rept_password', 'email', 'code']],
    "Forget": ["忘记密码", ['username', 'new_password', 'rept_password', 'email', 'code']],
  };

  loginForm: FormGroup;

  controlConfig = {
    username: [ '', [(control: FormControl) => {
      if (!control.value)
        return { status: 'error', message: Config.UnEmpty};
      if (control.value.length > Config.UnLength)
        return { status: 'error', message: Config.UnLong };
      return { status: 'success' }
    }]],

    password: [ '', [(control: FormControl) => {
      console.error(control);
      if (!control.value)
        return { status: 'error', message: Config.PwdEmpty };
      if (control.value.length < Config.PwdLength[0])
        return { status: 'error', message: Config.PwdShort };
      if (control.value.length > Config.PwdLength[1])
        return { status: 'error', message: Config.PwdLong };
      return { status: 'success' }
    }]],

    new_password: [ '', [(control: FormControl) => {
      if (!control.value)
        return { status: 'error', message: Config.PwdEmpty };
      if (control.value.length < Config.PwdLength[0])
        return { status: 'error', message: Config.PwdShort };
      if (control.value.length > Config.PwdLength[1])
        return { status: 'error', message: Config.PwdLong };
      return { status: 'success' }
    }]],

    rept_password: [ '', [(control: FormControl) => {
      if (!control.value)
        return { status: 'error', message: Config.PwdEmpty };
      if (control.value.length < Config.PwdLength[0])
        return { status: 'error', message: Config.PwdShort };
      if (control.value.length > Config.PwdLength[1])
        return { status: 'error', message: Config.PwdLong };
      if (this.type == "Register" && control.value != this.inputData.password.value)
        return { status: 'error', message: Config.PwdDiff };
      if (this.type == "Forget" && control.value != this.inputData.new_password.value)
        return { status: 'error', message: Config.PwdDiff };
      return { status: 'success' }
    }]],

    mail: [ '', [(control: FormControl) => {
      if (!control.value)
        return { status: 'error', message: Config.EmailEmpty };
      if (!Config.MailReg.test(control.value))
        return { status: 'error', message: Config.EmailInvalid };
      return { status: 'success' };
    }] ],

    code: ['', [(control: FormControl) => {
      if (!control.value)
        return { status: 'error', message: Config.CodeEmpty };
      if (control.value.length < Config.CodeLength)
        return { status: 'error', message: Config.CodeShort };
    }]]
  };

  constructor(
    @Inject(forwardRef(() => FormBuilder)) private formBuilder: FormBuilder
  ) { };

  ngOnInit(): void {
    this.loginForm = this.formBuilder.group(this.controlConfig)
  };

  onClick(tag) { this.onSubmit.emit({ tag, data : this.inputData }); }

  statusCtrl(item: string): string {
    console.error("statusCtrl: ", item, this.loginForm);
    if (!this.loginForm.controls[item]) return;
    const control: AbstractControl = this.loginForm.controls[item];
    return control.dirty && control.hasError('status') ? control.errors.status : '';
  }

  messageCtrl(item: string): string {
    if (!this.loginForm.controls[item]) return;
    const control: AbstractControl = this.loginForm.controls[item];
    return control.dirty && control.hasError('message') ? control.errors.message : '';
  }

}
