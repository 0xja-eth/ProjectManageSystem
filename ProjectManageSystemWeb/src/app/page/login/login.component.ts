import {Component, EventEmitter, forwardRef, Inject, Input, OnInit, Output} from '@angular/core';
import {FormBuilder} from '@angular/forms';

import {ActivatedRoute} from '@angular/router';
import {Form} from '../../system/user_module/user_system';
import {ForgetForm, LoginForm, RegisterForm} from './forms';
import {UserSystem} from '../../system/user_module/user_system';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})

export class LoginComponent implements OnInit {

  constructor(private user: UserSystem, private routerinfo:ActivatedRoute,
    @Inject(forwardRef(() => FormBuilder)) private formBuilder: FormBuilder
  ) { };

  ngOnInit(): void {
    this.type = this.routerinfo.snapshot.params['type']
  };

  type: "login" | "register" | "forget" = "login";

  onDo($event: {tag: 'login'|'register'|'forget'|'register_code'|'forget_code', data: Form}): void {
    console.info($event);
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
      next: value => console.info(value),
      error: err => console.error(err),
      complete: () => console.info("Completed!")
    });
  }
  onLoginSuccessfully() {

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
}
