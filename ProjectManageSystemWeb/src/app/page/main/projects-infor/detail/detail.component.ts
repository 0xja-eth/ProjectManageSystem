import {Component, OnChanges, OnInit} from '@angular/core';
import { ProjectSystem } from '../../../../system/project_module/project_system';
import {Project} from '../../../../system/project_module/project';
import {ActivatedRoute, NavigationEnd, Router} from '@angular/router';
import {ProjectsInforComponent} from '../projects-infor.component';

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.css']
})
export class DetailComponent implements OnInit {

  ProjectSystem = ProjectSystem;
  father = ProjectsInforComponent;

  constructor(private project: ProjectSystem,
              private router_info: ActivatedRoute,
              private router:Router) {
    router.events.subscribe(this.updateProject.bind(this));
  }

  project_obj: Project;

  ngOnInit() {
    this.updateProject();
  }

  updateProject() {
    // 当路由发生变化，存储在浏览器里面的的用户信息发生变化的时候刷新组件
    this.project_obj = ProjectSystem.Project;
    let pid = this.router_info.snapshot.params['id'];
    if(this.project_obj && this.project_obj.id == pid) return;
    this.project.getProject(pid).subscribe(proj=>this.project_obj=proj);
  }

  completedRate() {
    return this.format(this.project_obj.completedRate())
  }
  timeRate() {
    return this.format(this.project_obj.timeRate())
  }
  progressRate() {
    return this.format(this.project_obj.progressRate())
  }

  onLinkClick(tag){
    this.router.navigateByUrl(ProjectsInforComponent
      .getRoute(tag, this.project_obj.id));
  }

  format(x: number) {
    return Math.max(Math.min(Math.round(x*100)/100, 100),0);
  }

}
