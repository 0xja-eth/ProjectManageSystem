import { NgModule } from '@angular/core';

import { MainRoutingModule } from './main-routing.module';
import { MainComponent } from './main.component';
import {PersonalInforComponent} from './personal-infor/personal-infor.component';
import {ChatRoomComponent} from './chat-room/chat-room.component';
import {ChatDetailComponent} from './chat-detail/chat-detail.component';
import {CodeChangeComponent} from './code-change/code-change.component';
import {ShareModule} from '../../share/share.module';
import {ProjectsInforModule} from './projects-infor/projects-infor.module';

import {FriendInfoComponent} from "./friend-info/friend-info.component";
import { NoticeComponent } from './notice/notice.component';
import {ProjectService} from '../../system/project_module/project.service';
import {UserService} from '../../system/user_module/user.service';
import {ChatService} from '../../system/chat_module/chat.service';


@NgModule({
  declarations: [
    MainComponent,
    PersonalInforComponent,
    ChatRoomComponent,
    ChatDetailComponent,
    CodeChangeComponent,

    FriendInfoComponent,
    NoticeComponent,
  ],
  imports: [
    ShareModule,
    MainRoutingModule,
    ProjectsInforModule
  ],
  providers: [ProjectService, UserService, ChatService]
})
export class MainModule { }
