
import {AbstractControl} from '@angular/forms';
import {NetworkSystem, InterfaceSystem} from '../network_system';
import {Injectable} from '@angular/core';
import {Observable} from 'rxjs';

// 所有表单的父类
export class Form {

  constructor(public name:string){

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

@Injectable()
export class UserSystem {
  static Token: string = '';

  constructor(private network: NetworkSystem) {

  }

  register(un, pw, email, code) : Observable<Object> {
    return this.network.send(InterfaceSystem.Interfaces.RegisterRoute, {un, pw, email, code});
  }
  login(un, pw) : Observable<Object> {
    return this.network.send(InterfaceSystem.Interfaces.LoginRoute, {un, pw});
  }
  forget(un, pw, email, code) : Observable<Object> {
    return this.network.send(InterfaceSystem.Interfaces.ForgetRoute, {un, pw, email, code});
  }
  sendCode(un, email, type: 'register' | 'forget') : Observable<Object> {
    return this.network.send(InterfaceSystem.Interfaces.SendCodeRoute, {un, email, type});
  }

  checkLogin() {

  }
}

