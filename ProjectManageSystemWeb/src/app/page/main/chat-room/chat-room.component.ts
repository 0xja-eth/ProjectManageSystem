import {Component, forwardRef, Inject, OnInit} from '@angular/core';
import {ElementRef, AfterViewChecked, ViewChild} from '@angular/core';
import { Chat } from '../chat-detail/chat';
import {FormBuilder, FormControl, FormGroup} from '@angular/forms';

@Component({
  selector: 'app-chat-room',
  templateUrl: './chat-room.component.html',
  styleUrls: ['./chat-room.component.css']
})
export class ChatRoomComponent implements OnInit, AfterViewChecked {

  @ViewChild("scrollMe", {static: false, read: ElementRef})
  private myScrollContainer: ElementRef;

  // TODO: myself
  friendsMsg: Chat[] = [
    {id: 0, name: 'LJA', msg:
        [{speaker: 'myself', content: '你好，friend1'},
        {speaker: 'myself', content: '你现在怎么样？'},
        {speaker: 'friend', content: '你好，LJA'},
        {speaker: 'myself', content: '哈哈'},
        {speaker: 'friend', content: '我现在人在美国'},
        {speaker: 'friend', content: '刚下飞机'},
        {speaker: 'friend', content: '利益相关，匿了，再见。'}]},

    {id: 1, name: 'LJB', msg: [{speaker: 'myself', content: '你好，friend2'},
        {speaker: 'myself', content: '你现在怎么样？'},
        {speaker: 'friend', content: '你好，LJB'},
        {speaker: 'friend', content: '我现在被抓了'},
        {speaker: 'friend', content: '现在要进去了'},
        {speaker: 'friend', content: '你好好保重！'}]},

    {id: 2, name: 'LJC', msg: [{speaker: 'myself', content: '你好，friend3'},
        {speaker: 'myself', content: '你现在怎么样？'},
        {speaker: 'friend', content: '你好，LJC'},
        {speaker: 'myself', content: '？？'},
        {speaker: 'friend', content: '滚'}]},

    {id: 3, name: 'LJD', msg: [{speaker: 'myself', content: '你好，friend4'},
        {speaker: 'myself', content: '你现在怎么样？'},
        {speaker: 'friend', content: '你好，LJD'},
        {speaker: 'myself', content: '哈哈'},
        {speaker: 'friend', content: '我有事，再见哈'}]},

    {id: 4, name: 'LJE', msg: [{speaker: 'myself', content: '你好，friend5'},
        {speaker: 'myself', content: '你现在怎么样？'},
        {speaker: 'friend', content: '拉黑了，拜拜'}]},

    {id: 5, name: '项目管理系统', msg: [{speaker: 'LJA', content: '大家好，我是LJA。'},
        {speaker: 'LJB', content: '大家好，我是LJB。'},
        {speaker: 'LJC', content: '大家好，我是LJC。'},
        {speaker: 'LJD', content: '大家好，我是LJD。'},
        {speaker: 'LJE', content: '大家好，我是LJE。'},
        {speaker: 'myself', content: '大家好，我是myself。'},
        {speaker: 'LJEF', content: '大家好，我是LJFFFFFF。'}], group: true }
  ];
  selectedFriend: number; // 被选中Chat的索引
  newMessage: string; // 文本框发送的消息
  splitMessage: string[];

  constructor() { }

  ngOnInit() {
    this.onSelect(0);
  }

  ngAfterViewChecked() {
    if(this.myScrollContainer) this.scrollToBottom();
  }

  scrollToBottom() {
    this.myScrollContainer.nativeElement.scrollTop = this.myScrollContainer.nativeElement.scrollHeight;
  }

  onSelect(friend: any): void {
    this.selectedFriend = friend;
  }

  onEnter(): void {
    this.newMessage = this.newMessage.replace(/\n/g, '<br>');
    this.pushNewMessage(this.newMessage);
    this.newMessage = '';
  }

  displayLatest(friend: Chat): string {
    this.splitMessage = friend.msg[friend.msg.length - 1].content.split(/<br>/g);
    if (friend.group) {
      // TODO: myself
      if (friend.msg[friend.msg.length - 1].speaker !== 'myself') {
        this.splitMessage[0] = friend.msg[friend.msg.length - 1].speaker + ': ' + this.splitMessage[0];
      }
    }
    return this.splitMessage[0];
  }

  pushMessage(): void {
    this.pushNewMessage(this.newMessage);
    this.newMessage = '';
  }

  pushNewMessage(msg: string, speaker: string = 'myself'): void {
    let chat = this.getChat(this.selectedFriend);
    chat.msg.push({speaker, content: msg});
  }

  getChat(id: number) {
    return this.friendsMsg[id]
  }
}
