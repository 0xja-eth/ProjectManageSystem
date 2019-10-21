import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {PersonalInforComponent} from './personal-infor/personal-infor.component';
import {ChatRoomComponent} from './chat-room/chat-room.component';
import {CodeChangeComponent} from './code-change/code-change.component';

const routes: Routes = [
  { path: 'personal-infor', component: PersonalInforComponent},
  { path: 'code-change', component: CodeChangeComponent},
  { path: 'chat-room', component: ChatRoomComponent}
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MainRoutingModule { }
