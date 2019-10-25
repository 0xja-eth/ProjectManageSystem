import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import {DetailComponent} from './detail/detail.component';
import {EditComponent} from './edit/edit.component';
import {MembersComponent} from './members/members.component';

const routes: Routes = [
  { path: 'detail/:id', component: DetailComponent},
  { path: 'edit/:id', component: EditComponent},
  { path: 'members/:id', component: MembersComponent},

  //{ path: '', redirectTo: 'detail', pathMatch: 'full' },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ProjectsInforRoutingModule { }
