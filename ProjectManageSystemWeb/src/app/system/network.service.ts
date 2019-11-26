import {UserService} from './user_module/user.service';
import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import {Observable, EMPTY, concat} from 'rxjs';
import {map} from 'rxjs/operators';
import {ViewSystem} from './view.system';
import {take} from 'rxjs/operators';

type HTTPResult<T> = {
  status: number, data?: T, errmsg?: string
}

export class Interface {
  constructor(
    public route:string,
    public method:'GET'|'POST'|'WS'='GET'){

  }
}

export class InterfaceSystem {
  //static Interfaces = {
  // DataService
  static InitializeData = new Interface('system/data');

  // UserService
  static LoginRoute = new Interface('user/login', 'POST');
  static RegisterRoute = new Interface('user/register', 'POST');
  static ForgetRoute = new Interface('user/forget', 'POST');
  static SendCodeRoute = new Interface('user/code', 'POST');

  static ResetPwdRoute = new Interface('');
  static EditInfoRoute = new Interface('');
  static GetInfoRoute = new Interface('');

  static GetFriendsRoute = new Interface('');
  static SearchFriendRoute = new Interface('');
  static AddFriendRoute = new Interface('');
  static OperFriendRoute = new Interface('');
  static DeleteFriendRoute = new Interface('');

  // ProjectService
  static CreateProjectRoute = new Interface('');
  static GetProjectsRoute = new Interface('');
  static GetProjectRoute = new Interface('');

  static AddMemberRoute = new Interface('');
  static DeleteMemberRoute = new Interface('');
  static EditMemRoleRoute = new Interface('');
  static ChangeManagerRoute = new Interface('');

  static GetNoticesRoute = new Interface('');
  static PushNoticeRoute = new Interface('');
  static DeleteNoticeRoute = new Interface('');

  static GetTasksRoute = new Interface('');
  static GetTaskDetailRoute = new Interface('');
  static GetUserTasksRoute = new Interface('');
  static EditTaskTakeRoute = new Interface('');

  static RequestProgressRoute = new Interface('');
  static OperProgressRoute = new Interface('');

  static AddTaskRoute = new Interface('');
  static EditTaskRoute = new Interface('');
  static DeleteTaskRoute = new Interface('');

  // ChatService
  static GetChatsRoute = new Interface('');
  static GetChatRoute = new Interface('');
  static SendMessageRoute = new Interface('');
  //};
}

@Injectable()
export class NetworkService {
  static HTTP_URL = '/api/';
  static WS_URL = '';
  //static WS_URL = 'ws://127.0.0.1:8000/ws/chat/123/';

  private WSObject: WebSocket;

  constructor(private http: HttpClient) {

  }

  startWS() {
    this.WSObject = new WebSocket(NetworkService.WS_URL);
    return new Observable(
      observer => {
        this.WSObject.onmessage = (event) => observer.next(event.data);
        this.WSObject.onerror = (event) => observer.error(event);
        this.WSObject.onclose = () => observer.complete();
      });
  }
  endWS() {
    this.WSObject.close();
  }

  private static getAuthedData(data?) {
    data = data || {};
    data.auth = UserService.Auth? UserService.Auth.token : '';
    return data;
  }

  send<T>(interface_:Interface, data?, auth:boolean=false, headers?):Observable<T> {
    console.info("send", interface_, data);
    // 显示 Loading
    let show:Observable<T> = new Observable(
      obs=>{ViewSystem.ShowLoading(); obs.complete();});
    // 隐藏 Loading
    let hide:Observable<T> = new Observable(
      obs=>{ViewSystem.HideLoading(); obs.complete();});
    // 授权
    if(auth) data = NetworkService.getAuthedData(data);
    // 执行
    let do_: Observable<T>;
    if(interface_.method == 'WS') do_ = this.sendWS<T>(interface_.route, data);
    else do_ = this.sendHTTP<T>(interface_.method, interface_.route, data, headers);
    return concat(show, do_, hide);
  }
/*
  config(method, data, headers) {
    headers = headers || {};
    headers['Content-Type'] = "application/json";
    let res = {method, headers};
    if(data) res['body'] = JSON.stringify(data);
    return res;
  };
*/

  sendHTTP<T>(method: 'GET'|'POST', route:string, data?, headers?): Observable<T> {
    //let res = await fetch(NetworkSystem.HTTP_URL+route, this.config(method, data, headers));
    // 804173948@qq.com

    //headers = headers || {};
    //headers['Content-Type'] = "application/x-www-form-urlencoded;charset=utf-8";//"application/json";

    let url = NetworkService.HTTP_URL+route;
    let http: Observable<HTTPResult<T>> = this.http[method.toLowerCase()](url, data, {headers});
    return http.pipe(map(result => {
      if(result.status==0) return result.data; throw result.errmsg;
    }));
  }

  sendWS<T>(route:string, data?): Observable<T> {
    data = {route, data};
    this.WSObject.send(JSON.stringify(data));
    return EMPTY;
  }
}
