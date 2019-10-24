import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import {PersonalInforComponent} from './personal-infor/personal-infor.component';
import {ChatRoomComponent} from './chat-room/chat-room.component';
import {ProjectsInforComponent} from './projects-infor/projects-infor.component';

const routes: Routes = [
  //{ path: 'code-change', component: CodeChangeComponent},
  { path: 'projects', component: ProjectsInforComponent,
    loadChildren: () => import('./projects-infor/projects-infor.module').then(mod => mod.ProjectsInforModule),
  },
  { path: 'chats', component: ChatRoomComponent},
  { path: 'personal', component: PersonalInforComponent},

  { path: '', redirectTo: 'projects', pathMatch: 'full' },
  { path: 'projects/', redirectTo: 'projects', pathMatch: 'full' },
  { path: 'chats/', redirectTo: 'chats', pathMatch: 'full' },
  { path: 'personal/', redirectTo: 'personal', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class MainRoutingModule { }
