import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {InputData} from '../input-field/input_data';

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
      placeholder: "请输入你的用户名", maxLength: 12
    }),
    password: new InputData("密码","","Password",{
      placeholder: "请输入你的密码", maxLength: 16
    }),
    password2: new InputData("重复密码","","Password",{
      placeholder: "重复输入密码", maxLength: 16
    }),
    email: new InputData("邮箱","","Text",{
      placeholder: "请输入邮箱", button: null
    }),
    code: new InputData("验证码","","Text",{
      placeholder: "请输入验证码", maxLength: 6, button: "发送验证码"
    }),
  };

  constructor() { }; ngOnInit() { };

  onClick(tag) { this.onSubmit.emit({ tag, data : this.inputData }); }
}
