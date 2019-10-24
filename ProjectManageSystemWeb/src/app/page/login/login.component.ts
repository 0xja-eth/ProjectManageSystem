import {Component, EventEmitter, forwardRef, Inject, Input, OnInit, Output} from '@angular/core';
import {FormBuilder} from '@angular/forms';

import {ActivatedRoute} from '@angular/router';
import {Form} from '../../system/user_module/user_system';
import {ForgetForm, LoginForm, RegisterForm} from './forms';
import {UserSystem} from '../../system/user_module/user_system';
import {ViewSystem} from '../../system/view_system';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})

export class LoginComponent implements OnInit {

  constructor(private user: UserSystem, private router_info:ActivatedRoute,
    @Inject(forwardRef(() => FormBuilder)) private formBuilder: FormBuilder
  ) { };

  ngOnInit(): void {
    document.body.style.backgroundImage="linear-gradient(to right, rgba(192,255,192,0.5) 25%, rgba(228,255,228,0.75))";
    this.type = this.router_info.snapshot.params['type']
  };

  type: "login" | "register" | "forget" = "login";

  onDo($event: {tag: 'login'|'register'|'forget'|'register_code'|'forget_code', data: Form}): void {
    switch ($event.tag) {
      case 'login':this.onLogin($event.data as LoginForm); break;
      case 'register': this.onRegister($event.data as RegisterForm); break;
      case 'register_code':  this.onRegisterCode($event.data as RegisterForm); break;
      case 'forget': this.onForget($event.data as ForgetForm); break;
      case 'forget_code':  this.onForgetCode($event.data as ForgetForm); break;
    }
  };
  onLogin(form: LoginForm) {
    form.do(this.user).subscribe({
      next: this.onLoginSuccessfully,
      error: err => this.onError("登陆失败",err),
      complete: ()=> console.error("completed")
    });
  }
  onLoginSuccessfully(value) {
    console.info("onLoginSuccessfully:",value)
  }

  onRegister(form: RegisterForm) {
    form.do(this.user, 'do');
  }
  onRegisterCode(form: RegisterForm) {
    form.do(this.user, 'code');
  }
  onForget(form: ForgetForm) {
    form.do(this.user, 'do');
  }
  onForgetCode(form: ForgetForm) {
    form.do(this.user, 'code');
  }

  onError(title, err) {
    //ViewSystem.ShowLoading = false;
    console.error(err); this.showAlert(title, err.message);
  }

  // Alert

  alert_shown = false;
  alert_title = '';
  alert_content = '';

  showAlert(title: string, content:string) {
    this.alert_title = title;
    this.alert_content = content;
    this.alert_shown = true;
  }

}
