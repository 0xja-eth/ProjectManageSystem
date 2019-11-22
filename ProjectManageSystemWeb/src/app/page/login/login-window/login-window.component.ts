import {Component, EventEmitter, forwardRef, Inject, Input, OnInit, Output} from '@angular/core';
import {AbstractControl, FormBuilder, FormControl, FormGroup} from '@angular/forms';
import {ConfigSystem} from '../../../system/config.system';
import {LoginForm, RegisterForm, ForgetForm} from '../forms';

@Component({
  selector: 'app-login-window',
  templateUrl: './login-window.component.html',
  styleUrls: ['./login-window.component.css']
})
export class LoginWindowComponent implements OnInit {
  ConfigSystem = ConfigSystem;

  @Input() type: "login" | "register" | "forget" = "login";

  @Output() onSubmit = new EventEmitter();

  private loginForm = new LoginForm();
  private registerForm = new RegisterForm();
  private forgetForm = new ForgetForm();

  inputForms = {
    "login": this.loginForm,
    "register": this.registerForm,
    "forget": this.forgetForm,
  };

  formGroup: FormGroup;

  inputData = () => this.inputForms[this.type];

  constructor(
    @Inject(forwardRef(() => FormBuilder)) private formBuilder: FormBuilder
  ) { };

  ngOnInit(): void {
    this.switchForm(this.type);
  };

  switchForm(type) {
    this.type = type;
    this.formGroup = this.formBuilder.group(this.inputData());
    console.log('switchForm:',type, this);
    console.log('this.formGroup:',this.formGroup);
  }

  onClick(tag) { this.onSubmit.emit({ tag, data : this.inputData() }); }

  statusCtrl(item: string): string {
    let control: AbstractControl = this.formGroup.controls[item];
    this.inputData()[item] = control.value;
    let res = this.inputData().check(item, control);
    return control.dirty ? res.status : '';
  }

  messageCtrl(item: string): string {
    let control: AbstractControl = this.formGroup.controls[item];
    this.inputData()[item] = control.value;
    let res = this.inputData().check(item, control);
    return control.dirty ? res.message : '';
  }

}
