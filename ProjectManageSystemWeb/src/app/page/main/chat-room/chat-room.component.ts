import {Component, forwardRef, Inject, OnInit} from '@angular/core';
import {ElementRef, AfterViewChecked, ViewChild} from '@angular/core';
import { Chat } from '../../../system/chat_module/chat';
import {FormBuilder, FormControl, FormGroup} from '@angular/forms';
import {ChatService} from '../../../system/chat_module/chat.service';
import {map} from 'rxjs/operators';

@Component({
  selector: 'app-chat-room',
  templateUrl: './chat-room.component.html',
  styleUrls: ['./chat-room.component.css']
})
export class ChatRoomComponent implements OnInit, AfterViewChecked {

  @ViewChild("scrollMe", {static: false, read: ElementRef})
  private myScrollContainer: ElementRef;

  // TODO: myself
  friendsMsg: Chat[] = [];

  selectedFriend: number; // 被选中Chat的索引
  newMessage: string; // 文本框发送的消息
  splitMessage: string[];

  constructor(private chatServices: ChatService) { }

  ngOnInit() {
    this.getChats();
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
    if (friend.pid != undefined) {
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

    this.chatServices.sendMessage(msg, chat.fid, chat.pid)
  }

  getChats() {
    this.chatServices.getChats().subscribe(chats => this.friendsMsg = chats);
  }

  getChat(id: number) {
    let res : Chat;
    this.chatServices.getChat(id).subscribe(chat => res = chat);
    return res;
  }
}
