import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {PersonalInforComponent} from './personal-infor/personal-infor.component';
import {CodeChangeComponent} from './code-change/code-change.component';
import {ChatRoomComponent} from './chat-room/chat-room.component';


const routes: Routes = [
  { path: 'personal-infor', component: PersonalInforComponent},
  { path: 'code-change', component: CodeChangeComponent},
  { path: 'chat-room', component: ChatRoomComponent}
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes,
      { enableTracing: true})
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
