import { Component, OnInit } from '@angular/core';
import { Project } from '../../../system/project_module/project';
import {ConfigSystem} from '../../../system/config_system';
import {ProjectSystem} from '../../../system/project_module/project_system';
import {ActivatedRoute, Router} from '@angular/router';

@Component({
  selector: 'app-projects-infor',
  templateUrl: './projects-infor.component.html',
  styleUrls: ['./projects-infor.component.css']
})
export class ProjectsInforComponent implements OnInit {

  // 静态类代号
  ProjectSystem = ProjectSystem;
  self = ProjectsInforComponent;

  static DefaultPage = "detail";

  static getRoute(page, pid) {
    return 'main/projects/'+page+'/'+pid;
  }

  projects_data: Project[];

  selected_pid: number = 0;

  drop_down_data = [];
  dropDownData() {
    if(this.drop_down_data.length<=0){
      let proj = this.project.projects_data.map(p=>[p.id, p.name]);
      proj.push([-1, ConfigSystem.AddProjectText]);
      this.drop_down_data = proj;
    }
    return this.drop_down_data;
  }

  page:string = ProjectsInforComponent.DefaultPage;

  constructor(private router: Router,
              private activate:ActivatedRoute,
              private project: ProjectSystem) {
    // 当路由发生变化，存储在浏览器里面的的用户信息发生变化的时候刷新组件
    router.events.subscribe(this.updateProject.bind(this));
  }

  ngOnInit() {
    this.updateProject();
  }

  updateProject() {
    this.initProjectsData();
    if(ProjectSystem.Project)
      this.onProjectChange(ProjectSystem.Project.id);
    else this.locatePage();
  }

  initProjectsData() {
    this.project.getProjects().subscribe(data=>this.projects_data = data);
  }

  locatePage() {
    let fc = this.activate.firstChild || this.activate;
    // @ts-ignore
    this.page = fc.url.value[0].path;
    //this.selected_pid = Number(fc.params.value.id);
    // @ts-ignore
    this.selected_pid = Number(fc.params.value.id);
  }

  selectedProject() {
    return ProjectSystem.Project || this.getProject(this.selected_pid);
  }
  getProject(pid: number) {
    let proj: Project = null;
    this.project.getProject(pid).subscribe(data=>proj = data);
    return proj;
  }

  onProjectSelect($event) {
    if($event==-1) this.onProjectAdd();
    else this.onProjectChange($event);
  }

  onProjectChange(pid) {
    if(this.selected_pid == pid) return;
    this.selected_pid = pid;
    this.page = ProjectsInforComponent.DefaultPage;
    ProjectSystem.setProject(this.getProject(pid));
    this.router.navigateByUrl(this.getCurrentUrl());
  }

  getCurrentUrl() {
    return ProjectsInforComponent.getRoute(this.page, this.selected_pid);
  }

  onProjectAdd() {

  }
}
