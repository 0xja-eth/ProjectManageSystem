import {UserService, Form, LoginResult} from '../../system/user_module/user.service';
import {ConfigSystem} from '../../system/config.system';
import {Observable} from 'rxjs';

export class LoginForm extends Form{
  constructor(name:string='登陆', public username: string='', public password: string=''){
    super(name);
  }

  do(service:UserService, type?) : Observable<LoginResult> {
    if(!this.checkDo(type)) return;
    return service.login(this.username, this.password);
  }

  checkAll(type?): { message?: string; status: string }  {
    let res: { message?: string; status: string } = {status: 'success'};
    if(res.status=='success') res = this.checkSingle('username', this.username);
    if(res.status=='success') res = this.checkSingle('password', this.password);
    return res;
  }

  protected checkSingle(type:'password' | 'username', val:string) {
    switch (type) {
      case 'password': return this.checkPassword(val);
      case 'username': return this.checkUsername(val);
      default: return {status: 'error', message: ConfigSystem.UnknownType}
    }
  }

  checkUsername(val:string) {
    if (!val) return { status: 'error', message: ConfigSystem.UnEmpty};
    if (val.length > ConfigSystem.UnLength)
      return { status: 'error', message: ConfigSystem.UnLong };
    return { status: 'success' }
  }
  checkPassword(val:string) {
    if (!val) return { status: 'error', message: ConfigSystem.PwdEmpty };
    if (val.length < ConfigSystem.PwdLength[0])
      return { status: 'error', message: ConfigSystem.PwdShort };
    if (val.length > ConfigSystem.PwdLength[1])
      return { status: 'error', message: ConfigSystem.PwdLong };
    return { status: 'success' }
  }
}

export class RegisterForm extends LoginForm {
  code_time: Date = undefined;
  code_interval: number = undefined;
  delta_second: number = 0;

  constructor(name:string='注册', username: string='', password: string='',
              public repassword: string='', public email: string='', public code: string=''){
    super(name, username, password);
  }

  updateCodeTime() {
    let now: Date = new Date();
    if (this.code_time && now<=this.code_time)
      // @ts-ignore
      this.delta_second = Math.round((this.code_time-now)/1000);
    else {
      clearInterval(this.code_interval);
      this.code_interval = undefined;
      this.code_time = undefined;
      this.delta_second = 0;
    }
  }

  setCode() {
    this.code_time = new Date();
    this.code_time.setTime(this.code_time
      .getTime() + ConfigSystem.CodeSecond*1000);
    this.delta_second = ConfigSystem.CodeSecond;
    this.code_interval = setInterval(this.updateCodeTime.bind(this), 500);
  }

  do(service:UserService, type: 'code' | 'do') : Observable<any> {
    if(!this.checkDo(type)) return;
    console.info("after check");
    switch (type) {
      case 'code': return service.sendCode(this.username, this.email, 'register');
      case 'do': return service.register(this.username, this.password, this.email, this.code);
    }
  }

  checkAll(type: 'code' | 'do') {
    let res: { message?: string; status: string } = {status: 'success'};
    switch (type) {
      case 'code':
        if(res.status=='success') res = this.checkSingle('username', this.username);
        if(res.status=='success') res = this.checkSingle('email', this.email);
        break;
      case 'do':
        if(res.status=='success') res = this.checkSingle('username', this.username);
        if(res.status=='success') res = this.checkSingle('password', this.password);
        if(res.status=='success') res = this.checkSingle('repassword', this.repassword);
        if(res.status=='success') res = this.checkSingle('email', this.email);
        break;
      default:
        res = {status: 'error', message: ConfigSystem.UnknownType};
        break;
    }
    return res;
  }

  protected checkSingle(type:'code' | 'email' | 'repassword' | 'password' | 'username', val:string) {
    switch (type) {
      case 'code': return this.checkCode(val);
      case 'email': return this.checkEmail(val);
      case 'repassword': return this.checkRePassword(val);
      default: return super.checkSingle(type, val);
    }
  }

  checkEmail(val:string) {
    if (!val) return { status: 'error', message: ConfigSystem.EmailEmpty };
    if (!ConfigSystem.EmailReg.test(val))
      return { status: 'error', message: ConfigSystem.EmailInvalid };
    return { status: 'success' };
  }
  checkCode(val:string) {
    if (!val) return { status: 'error', message: ConfigSystem.CodeEmpty };
    if (val.length < ConfigSystem.CodeLength)
      return { status: 'error', message: ConfigSystem.CodeShort };
    return { status: 'success' };
  }
  checkRePassword(val:string) {
    let res = this.checkPassword(val);
    if (res.status == 'error') return res;
    if (val != this.password)
      return { status: 'error', message: ConfigSystem.PwdDiff };
    return { status: 'success' }
  }

}

export class ForgetForm extends RegisterForm {
  constructor(name:string='忘记密码', username: string='', password: string='',
              repassword: string='', email: string='', code: string=''){
    super(name, username, password, repassword, email, code);
  }

  do(service:UserService, type: 'code' | 'do') : Observable<any> {
    if(!this.checkDo(type)) return;
    switch (type) {
      case 'code': return service.sendCode(this.username, this.email, 'forget');
      case 'do': return service.forget(this.username, this.password, this.email, this.code);
    }
  }

}
