import {Component, EventEmitter, forwardRef, Inject, Input, OnInit, Output} from '@angular/core';
import {FormBuilder} from '@angular/forms';

import {ActivatedRoute} from '@angular/router';
import {Form} from '../../system/user_module/user.service';
import {ForgetForm, LoginForm, RegisterForm} from './forms';
import {UserService, LoginResult} from '../../system/user_module/user.service';
import {ViewSystem} from '../../system/view.system';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})

export class LoginComponent implements OnInit {

  static LoginFailTitle = "登陆失败！";
  static RegisterFailTitle = "注册失败！";
  static ForgetFailTitle = "密码重置失败！";
  static SendCodeFailTitle = "发送验证码失败！";

  static LoginSuccessTitle = "登陆成功！";
  static LoginSuccessText = "登陆成功！欢迎您，{0}！";

  static RegisterSuccessTitle = "注册成功！";
  static RegisterSuccessText = "注册成功，请返回登录！";

  static ForgetSuccessTitle = "重置密码成功！";
  static ForgetSuccessText = "重置密码成功，请返回登录！";

  static SendCodeSuccessTitle = "发送验证码成功！";
  static SendCodeSuccessText = "验证码已成功发送到你的邮箱上，请查收！（60秒内有效）";

  constructor(private user: UserService, private router_info:ActivatedRoute,
              @Inject(forwardRef(() => FormBuilder)) private formBuilder: FormBuilder
  ) { };

  ngOnInit(): void {
    document.body.style.backgroundImage="linear-gradient(to right, rgba(192,255,192,0.5) 25%, rgba(228,255,228,0.75))";
    this.type = this.router_info.snapshot.params['type']
  };

  // 类型
  type: "login" | "register" | "forget" = "login";

  // 处理按钮事件
  onDo($event: {tag: 'login'|'register'|'forget'|'register_code'|'forget_code', data: Form}): void {
    console.error($event);
    switch ($event.tag) {
      case 'login':this.onLogin($event.data as LoginForm); break;
      case 'register': this.onRegister($event.data as RegisterForm); break;
      case 'register_code':  this.onRegisterCode($event.data as RegisterForm); break;
      case 'forget': this.onForget($event.data as ForgetForm); break;
      case 'forget_code':  this.onForgetCode($event.data as ForgetForm); break;
    }
  };
  // 处理登陆
  private onLogin(form: LoginForm) {
    form.do(this.user).subscribe({
      next: LoginComponent.onLoginSuccess,
      error: err => LoginComponent.onError(LoginComponent.LoginFailTitle, err),
      //complete: ()=> console.error("completed")
    });
  }
  // 成功登陆
  private static onLoginSuccess(result: LoginResult) {
    // @ts-ignore
    let text = LoginComponent.LoginSuccessText.format(result.user.name);
    ViewSystem.ShowAlert(LoginComponent.LoginSuccessTitle, text, ViewSystem.SuccessIcon);
  }

  // 处理注册
  private onRegister(form: RegisterForm) {
    form.do(this.user, 'do').subscribe({
      next: LoginComponent.onRegisterSuccess,
      error: err => LoginComponent.onError(LoginComponent.RegisterFailTitle, err),
      //complete: ()=> console.error("completed")
    });
  }
  // 成功注册
  private static onRegisterSuccess() {
    ViewSystem.ShowAlert(LoginComponent.RegisterSuccessTitle,
      LoginComponent.RegisterSuccessText, ViewSystem.SuccessIcon);
  }

  // 处理注册验证码
  private onRegisterCode(form: RegisterForm) {
    console.error("onRegisterCode",form);
    form.do(this.user, 'code').subscribe({
      next: LoginComponent.onRegisterCodeSuccess.bind(this, form),
      error: err => LoginComponent.onError(LoginComponent.SendCodeFailTitle, err),
      complete: ()=> console.error("completed")
    });
  }
  // 成功发送验证码
  private static onRegisterCodeSuccess(form: RegisterForm) {
    ViewSystem.ShowAlert(LoginComponent.SendCodeSuccessTitle,
      LoginComponent.SendCodeSuccessText, ViewSystem.SuccessIcon);
    form.setCode();
  }

  // 处理忘记密码
  private onForget(form: ForgetForm) {
    form.do(this.user, 'do').subscribe({
      next: LoginComponent.onForgetSuccess,
      error: err => LoginComponent.onError(LoginComponent.ForgetFailTitle, err),
      complete: ()=> console.error("completed")
    });
  }
  // 成功重置密码
  private static onForgetSuccess() {
    ViewSystem.ShowAlert(LoginComponent.ForgetSuccessTitle,
      LoginComponent.ForgetSuccessText, ViewSystem.SuccessIcon);
  }

  // 处理忘记密码验证码
  private onForgetCode(form: ForgetForm) {
    form.do(this.user, 'code').subscribe({
      next: LoginComponent.onForgetCodeSuccess.bind(this, form),
      error: err => LoginComponent.onError(LoginComponent.SendCodeFailTitle, err),
      complete: ()=> console.error("completed")
    });
  }
  // 成功发送验证码
  private static onForgetCodeSuccess(form: ForgetForm) {
    ViewSystem.ShowAlert(LoginComponent.SendCodeSuccessTitle,
      LoginComponent.SendCodeSuccessText, ViewSystem.SuccessIcon);
    form.setCode();
  }

  // 异常处理
  private static onError(title, err) {
    console.error(err);
    ViewSystem.HideLoading();
    ViewSystem.ShowAlert(title, err);
  }

}
