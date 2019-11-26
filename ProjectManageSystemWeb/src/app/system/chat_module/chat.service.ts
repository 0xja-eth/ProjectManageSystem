
import {Injectable} from '@angular/core';
import {InterfaceSystem, NetworkService} from '../network.service';
import {observableToBeFn} from 'rxjs/internal/testing/TestScheduler';
import {Observable} from 'rxjs';
import {Chat} from './chat';

@Injectable()
export class ChatService{

  chats: Chat[] = [
    {id: 0, name: 'LJA', msg:
        [{speaker: 'myself', content: '你好，friend1'},
          {speaker: 'myself', content: '你现在怎么样？'},
          {speaker: 'friend', content: '你好，LJA'},
          {speaker: 'myself', content: '哈哈'},
          {speaker: 'friend', content: '我现在人在美国'},
          {speaker: 'friend', content: '刚下飞机'},
          {speaker: 'friend', content: '利益相关，匿了，再见。'}], fid: 0},

    {id: 1, name: 'LJB', msg: [{speaker: 'myself', content: '你好，friend2'},
        {speaker: 'myself', content: '你现在怎么样？'},
        {speaker: 'friend', content: '你好，LJB'},
        {speaker: 'friend', content: '我现在被抓了'},
        {speaker: 'friend', content: '现在要进去了'},
        {speaker: 'friend', content: '你好好保重！'}], fid: 1},

    {id: 2, name: 'LJC', msg: [{speaker: 'myself', content: '你好，friend3'},
        {speaker: 'myself', content: '你现在怎么样？'},
        {speaker: 'friend', content: '你好，LJC'},
        {speaker: 'myself', content: '？？'},
        {speaker: 'friend', content: '滚'}], fid: 2},

    {id: 3, name: 'LJD', msg: [{speaker: 'myself', content: '你好，friend4'},
        {speaker: 'myself', content: '你现在怎么样？'},
        {speaker: 'friend', content: '你好，LJD'},
        {speaker: 'myself', content: '哈哈'},
        {speaker: 'friend', content: '我有事，再见哈'}], fid: 3},

    {id: 4, name: 'LJE', msg: [{speaker: 'myself', content: '你好，friend5'},
        {speaker: 'myself', content: '你现在怎么样？'},
        {speaker: 'friend', content: '拉黑了，拜拜'}], fid: 4},

    {id: 5, name: '星云6项目管理系统', msg: [{speaker: 'LJA', content: '大家好，我是LJA。'},
        {speaker: 'LJB', content: '大家好，我是LJB。'},
        {speaker: 'LJC', content: '大家好，我是LJC。'},
        {speaker: 'LJD', content: '大家好，我是LJD。'},
        {speaker: 'LJE', content: '大家好，我是LJE。'},
        {speaker: 'myself', content: '大家好，我是myself。'},
        {speaker: 'LJEF', content: '大家好，我是LJFFFFFF。'}], pid: 3 }
  ];


  constructor(private network: NetworkService) {

  }

  getChats(): Observable<Chat[]> {
    return new Observable<Chat[]>((obs)=>obs.next(this.chats));
    // let interface_ = InterfaceSystem.GetChatsRoute;
    // return this.network.send(interface_, {}, true);
  }

  getChat(cid): Observable<Chat> {
    return new Observable<Chat>((obs)=>obs.next(this.chats[cid]));
    // let interface_ = InterfaceSystem.GetChatRoute;
    // return this.network.send(interface_, {cid}, true);
  }

  sendMessage(msg, fid = null, pid = null) {
    let interface_ = InterfaceSystem.SendMessageRoute;
    return this.network.send(interface_, {msg, fid, pid}, true);
  }

  onMessageReceive(speaker, message) {

  }

  chatWith(uid = null, pid = null) {

  }
}
