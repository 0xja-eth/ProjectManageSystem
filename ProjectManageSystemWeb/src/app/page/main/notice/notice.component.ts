import { Component, OnInit } from '@angular/core';
import {Project} from '../../../system/project_module/project';
import {ProjectService} from '../../../system/project_module/project.service';

@Component({
  selector: 'app-notice',
  templateUrl: './notice.component.html',
  styleUrls: ['./notice.component.css']
})
export class NoticeComponent implements OnInit {
  existingProjects: Project[];

  constructor(private project: ProjectService) { }

  ngOnInit() {

    this.existingProjects = this.project.projects_data;

    this.existingProjects[0].publishNotice('abcd');
    this.existingProjects[0].publishNotice('abcd');

  }


}


