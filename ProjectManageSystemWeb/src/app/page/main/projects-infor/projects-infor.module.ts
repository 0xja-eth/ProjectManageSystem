import { NgModule } from '@angular/core';

import { ProjectsInforRoutingModule } from './projects-infor-routing.module';
import { ProjectsInforComponent } from './projects-infor.component';
import {ShareModule} from '../../../share/share.module';
import { DetailComponent } from './detail/detail.component';
import {ProjectService} from '../../../system/project_module/project.service';
import { EditComponent } from './edit/edit.component';
import { MembersComponent } from './members/members.component';
import {DayPilotModule} from 'daypilot-pro-angular';
import { TasksComponent } from './tasks/tasks.component';

@NgModule({
  declarations: [ProjectsInforComponent, DetailComponent, EditComponent, MembersComponent, TasksComponent],
  imports: [
    ShareModule,
    ProjectsInforRoutingModule,
    DayPilotModule
  ],
  providers: [ProjectService]
})
export class ProjectsInforModule { }
