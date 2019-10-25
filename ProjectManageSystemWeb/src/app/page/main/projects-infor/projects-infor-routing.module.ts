import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import {DetailComponent} from './detail/detail.component';
import {EditComponent} from './edit/edit.component';
import {MembersComponent} from './members/members.component';
import {TasksComponent} from './tasks/tasks.component';

const routes: Routes = [
  { path: 'detail/:id', component: DetailComponent},
  { path: 'edit/:id', component: EditComponent},
  { path: 'members/:id', component: MembersComponent},
  { path: 'tasks/:id', component: TasksComponent},

  //{ path: '', redirectTo: 'detail', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProjectsInforRoutingModule { }
