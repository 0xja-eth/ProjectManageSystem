import { Component, OnInit } from '@angular/core';
import {ProjectsInforComponent} from '../projects-infor.component';
import {ActivatedRoute, Router} from '@angular/router';
import {Project} from '../../../../system/project_module/project';
import {ProjectSystem} from '../../../../system/project_module/project_system';

@Component({
  selector: 'app-tasks',
  templateUrl: './tasks.component.html',
  styleUrls: ['./tasks.component.css']
})
export class TasksComponent implements OnInit {

  ProjectSystem = ProjectSystem;
  father = ProjectsInforComponent;

  constructor(private project: ProjectSystem,
              private router_info: ActivatedRoute,
              private router:Router) {
    // 当路由发生变化，存储在浏览器里面的的用户信息发生变化的时候刷新组件
    router.events.subscribe(this.updateProject.bind(this));
  }

  project_obj: Project;

  ngOnInit() {
    this.updateProject();
  }

  updateProject() {
    this.project_obj = ProjectSystem.Project;
    let pid = this.router_info.snapshot.params['id'];
    if(this.project_obj && this.project_obj.id == pid) return;
    this.project.getProject(pid).subscribe(proj=>this.project_obj=proj);
  }

  completedRate() {
    return this.format(this.project_obj.completedRate())
  }
  progressRate() {
    return this.format(this.project_obj.progressRate())
  }

  format(x: number) {
    return Math.max(Math.min(Math.round(x*100)/100, 100),0);
  }

}
