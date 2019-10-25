import { Component, OnInit } from '@angular/core';
import {ProjectsInforComponent} from '../projects-infor.component';
import {ActivatedRoute, Router} from '@angular/router';
import {Project} from '../../../../system/project_module/project';
import {ProjectSystem} from '../../../../system/project_module/project_system';

class MemberData {
  constructor(public name: string,
              public role: string,
              public sum_tasks: number,
              public unstart_tasks: number,
              public started_tasks: number,
              public finished_tasks: number,
              public progress: number,
              public total: boolean = false,
  ) {}

}

@Component({
  selector: 'app-members',
  templateUrl: './members.component.html',
  styleUrls: ['./members.component.css']
})
export class MembersComponent implements OnInit {

  ProjectSystem = ProjectSystem;
  father = ProjectsInforComponent;

  constructor(private project: ProjectSystem,
              private router_info: ActivatedRoute,
              private router:Router) {
    // 当路由发生变化，存储在浏览器里面的的用户信息发生变化的时候刷新组件
    router.events.subscribe(this.updateProject.bind(this));
  }

  project_obj: Project;

  member_data: MemberData[] = [
    new MemberData('利俊安','项目经理',50,
      5,25,20,40),
    new MemberData('李光耀','项目成员',8,
      1,2,5,62.5),
    new MemberData('吴宁','测试经理',33,
      11,0,22,66.67),
    new MemberData('邹博韬','项目成员',24,
      9,3,12,50),
    new MemberData('张景维','项目成员',40,
      2,2,36,90),
    new MemberData('曾声云','项目成员',16,
      10,4,2,12.5),
    new MemberData('总计','-',100, 20,
      28,52,52, true),
  ];

  ngOnInit() {
    this.updateProject();
  }

  updateProject() {
    this.project_obj = ProjectSystem.Project;
    let pid = this.router_info.snapshot.params['id'];
    if(this.project_obj && this.project_obj.id == pid) return;
    this.project.getProject(pid).subscribe(this.setProject.bind(this));
  }

  setProject(proj) {
    this.project_obj=proj;
  }

  generateMemberData() {

  }

  format(x: number) {
    return Math.max(Math.min(Math.round(x*100)/100, 100),0);
  }

  rowClassNameFilter(row: any, index: number): string {
    console.info("rowClassNameFilter", row, index);
    return row.total ? 'total-row' : '';
  }

  onDetail(scope) {
    console.info("onDetail",{scope});
  }
  onDelete(scope) {
    console.info("onDelete",{scope});
  }

}
