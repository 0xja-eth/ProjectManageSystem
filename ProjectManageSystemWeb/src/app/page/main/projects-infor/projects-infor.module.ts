import { NgModule } from '@angular/core';

import { ProjectsInforRoutingModule } from './projects-infor-routing.module';
import { ProjectsInforComponent } from './projects-infor.component';
import {ShareModule} from '../../../share/share.module';
import { DetailComponent } from './detail/detail.component';
import {ProjectSystem} from '../../../system/project_module/project_system';
import { EditComponent } from './edit/edit.component';

@NgModule({
  declarations: [ProjectsInforComponent, DetailComponent, EditComponent],
  imports: [
    ShareModule,
    ProjectsInforRoutingModule
  ],
  providers: [ProjectSystem]
})
export class ProjectsInforModule { }
