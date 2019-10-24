import {UserSystem} from './user_module/user_system';
import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import {Observable, EMPTY, concat, of, interval} from 'rxjs';
import {ViewSystem} from './view_system';
import {take} from 'rxjs/operators';

export class Interface {
  constructor(public route:string, public method:'GET'|'POST'|'WS'='GET'){

  }
}

export class InterfaceSystem {
  static Interfaces = {
    // DataSystem
    InitializeData: new Interface(''),

    // UserSystem
    LoginRoute: new Interface('', 'POST'),
    RegisterRoute: new Interface('', 'POST'),
    ForgetRoute: new Interface('', 'POST'),
    SendCodeRoute: new Interface('', 'POST'),

    // ProjectSystem
    GetProjects: new Interface(''),
    GetProject: new Interface(''),
  };

  static getInterface(type:string) {
    return this.Interfaces[type];
  }
}

@Injectable()
export class NetworkSystem {
  static HTTP_URL = '';
  static WS_URL = '';
  //static WS_URL = 'ws://127.0.0.1:8000/ws/chat/123/';

  private WSObject: WebSocket;

  constructor(private http: HttpClient) {

  }

  startWS() {
    this.WSObject = new WebSocket(NetworkSystem.WS_URL);
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
    data.auth = UserSystem.Token;
    return data;
  }

  send(interface_:Interface, data?, auth:boolean=false, headers?):Observable<Object> {
    let do_: Observable<Object>;
    let show:Observable<Object> = new Observable(
      (obs)=>{ViewSystem.ShowLoading = true; obs.complete();});
    let hide:Observable<Object> = new Observable(
      (obs)=>{ViewSystem.ShowLoading = false; obs.complete();});
    if(auth) data = NetworkSystem.getAuthedData(data);
    if(interface_.method == 'WS') do_ = this.sendWS(interface_.route, data);
    else do_ = this.sendHTTP(interface_.method, interface_.route, data, headers);
    return concat(show, hide, do_);
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

  sendHTTP(method: 'GET'|'POST', route:string, data?, headers?): Observable<Object> {
    //let res = await fetch(NetworkSystem.HTTP_URL+route, this.config(method, data, headers));
    let url = NetworkSystem.HTTP_URL+route;
    return this.http[method.toLowerCase()](url, data, {headers});
  }
  sendWS(route:string, data?): Observable<Object> {
    data = {route, data};
    this.WSObject.send(JSON.stringify(data));
    return EMPTY;
  }
}
