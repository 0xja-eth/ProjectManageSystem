
import {AbstractControl} from '@angular/forms';
import {NetworkService, InterfaceSystem} from '../network.service';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {Authorization, User} from './user';

// 所有表单的父类
export class Form {

  constructor(public from_name:string){

  }

  do(service:any, type:string) : any {
    if(!this.checkDo(type)) return false;
  }

  check(type:string, control: AbstractControl=null, val=''): { message?: string; status: string } {
    if(control) val = control.value;
    return this.checkSingle(type, val);
  }

  checkAll(type:string): { message?: string; status: string }  {
    return {status: 'success'};
  }

  protected checkDo(type:string) {
    let res = this.checkAll(type);
    if(res.status == 'error')
      this.handleError(res);
    else return true;
  }

  protected handleError(res) {
    alert(res.message);
  }

  protected checkSingle(type:string, val:string): { message?: string; status: string } {
    return {status: 'success'};
  }

}

export type LoginResult = {
  auth: Authorization,
  user: User
}

@Injectable()
export class UserService {
  static Auth: Authorization;
  static User: User;

  constructor(private network: NetworkService) {

  }

  register(un, pw, email, code) : Observable<void> {
    return this.network.send(InterfaceSystem.Interfaces.RegisterRoute, {un, pw, email, code});
  }
  login(un, pw) : Observable<LoginResult> {
    return this.network.send(InterfaceSystem.Interfaces.LoginRoute, {un, pw})
      .pipe(map(UserService.onLoginSuccess));
  }
  forget(un, pw, email, code) : Observable<void> {
    return this.network.send(InterfaceSystem.Interfaces.ForgetRoute, {un, pw, email, code});
  }
  sendCode(un, email, type: 'register' | 'forget') : Observable<void> {
    return this.network.send(InterfaceSystem.Interfaces.SendCodeRoute, {un, email, type});
  }

  // 登陆成功回调
  private static onLoginSuccess(result: LoginResult): LoginResult{
    UserService.Auth = result.auth;
    UserService.User = result.user;
    return result;
  }

  setUser(user) {

  }

  checkLogin() {

  }
}

