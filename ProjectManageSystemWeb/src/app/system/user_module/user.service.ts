
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
    let interface_ = InterfaceSystem.RegisterRoute;
    return this.network.send(interface_, {un, pw, email, code});
  }

  login(un, pw) : Observable<LoginResult> {
    let interface_ = InterfaceSystem.LoginRoute;
    return this.network.send(interface_, {un, pw})
      .pipe(map(UserService.onLoginSuccess));
  }

  forget(un, pw, email, code) : Observable<void> {
    let interface_ = InterfaceSystem.ForgetRoute;
    return this.network.send(interface_, {un, pw, email, code});
  }

  sendCode(un, email, type: 'register' | 'forget') : Observable<void> {
    let interface_ = InterfaceSystem.SendCodeRoute;
    return this.network.send(interface_, {un, email, type});
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

  getInfo(id, type) {
    let interface_ = InterfaceSystem.GetInfoRoute;
    return this.network.send(interface_, {id, type}, true);
  }

  editInfo(name, gender, birth, city, edu_id, duty, contact, desc) {
    let interface_ = InterfaceSystem.EditInfoRoute;
    return this.network.send(interface_, {name, gender, birth,
      city, edu_id, duty, contact, desc}, true);
  }

  resetPwd(old, new_) {
    let interface_ = InterfaceSystem.ResetPwdRoute;
    return this.network.send(interface_, {old, new_}, true);
  }

  getFriends(): Observable<User[]> {
    return this.randomFriends(30);
    // let interface_ = InterfaceSystem.GetFriendsRoute;
    // return this.network.send(interface_, {}, true);
  }

  searchFriend(un): Observable<User> {
    let interface_ = InterfaceSystem.SearchFriendRoute;
    return this.network.send(interface_, {}, true);
  }

  addFriend(uid) {
    let interface_ = InterfaceSystem.AddFriendRoute;
    return this.network.send(interface_, {uid}, true);
  }

  deleteFirend(uid) {
    let interface_ = InterfaceSystem.DeleteFriendRoute;
    return this.network.send(interface_, {uid}, true);
  }

  operFriendReq(req, accept) {
    let interface_ = InterfaceSystem.OperFriendRoute;
    return this.network.send(interface_, {req, accept}, true);
  }


  randomName(len: number): string {
    const $chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';
    const maxPos = $chars.length;
    let pwd = '';
    for (let i = 0; i < len; i++) {
      pwd += $chars.charAt(Math.floor(Math.random() * maxPos));
    }
    console.log(pwd);
    return pwd;
  }

  randomUsername(): string {
    const $chars = '0123456789';
    const accountLen = 11;
    let pwd = '';
    for (let i = 0; i < accountLen; i++) {
      pwd += $chars.charAt(Math.floor(Math.random() * accountLen));
    }
    return pwd;
  }

  // 随机数据（测试用）
  randomFriends(len: number): Observable<User[]> {
    let data: User[] = [];
    for ( let i = 0; i < len; i++) {
      let un = this.randomUsername();
      let name = this.randomName(10);
      let gender = Math.floor(Math.random() * 2) ? '男' : '女';
      let avatar = '../../assets/images/' + Math.floor(Math.random() * 5 + 1) + '.jpg';

      data.push(new User(i+1, un, "example@qq.com" ,name, gender, avatar,
        "1949/10/1 ", "广州", 1, "学生", "",
        "", "2019/11/10" ,1));
    }
    return new Observable<User[]>((obs)=>obs.next(data));
  }
}

