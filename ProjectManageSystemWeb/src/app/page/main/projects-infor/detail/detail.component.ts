import {Component, OnChanges, OnInit} from '@angular/core';
import { ProjectService } from '../../../../system/project_module/project.service';
import {Project} from '../../../../system/project_module/project';
import {ActivatedRoute, NavigationEnd, Router} from '@angular/router';
import {ProjectsInforComponent} from '../projects-infor.component';

@Component({
  selector: 'app-detail',
  templateUrl: './detail.component.html',
  styleUrls: ['./detail.component.css']
})
export class DetailComponent implements OnInit {

  ProjectSystem = ProjectService;
  father = ProjectsInforComponent;

  constructor(private project: ProjectService,
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
    this.project_obj = ProjectService.Project;
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
