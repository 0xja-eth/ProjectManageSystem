import { Component, OnInit } from '@angular/core';
import {ProjectsInforComponent} from '../projects-infor.component';
import {ActivatedRoute, Router} from '@angular/router';
import {Project} from '../../../../system/project_module/project';
import {ProjectService} from '../../../../system/project_module/project.service';
import {DataSystem} from '../../../../system/data.system';

class MemberInfo {
  roles: string; status: string; free: string;
  constructor(public id: number,
              public name: string,
              public gender: string | number,
              public rids: number[],
              public email: string,
              public contact: string,
              public status_id: number,
              public is_free: boolean,
  ) {
    this.gender = DataSystem.get('Genders', gender as number).name;
    this.roles = rids.map(id=>DataSystem.get('Roles', id).name).join('、');
    this.status = DataSystem.get('LoginStatuses', status_id).name;
    this.free = is_free ? '是' : '否'
  }
}

class MemberTask {
  roles: string;
  constructor(public id: number,
              public name: string,
              public rids: number[],
              public sum_tasks: number,
              public unstart_tasks: number,
              public started_tasks: number,
              public finished_tasks: number,
              public progress: number,
              public total: boolean = false,
  ) {
    let tmp = rids.map(id=>DataSystem.get('Roles', id).name);
    this.roles = tmp.join('、');
  }
}

@Component({
  selector: 'app-members',
  templateUrl: './members.component.html',
  styleUrls: ['./members.component.css']
})
export class MembersComponent implements OnInit {

  ProjectSystem = ProjectService;
  father = ProjectsInforComponent;

  constructor(private project: ProjectService,
              private router_info: ActivatedRoute,
              private router:Router) {
    // 当路由发生变化，存储在浏览器里面的的用户信息发生变化的时候刷新组件
    router.events.subscribe(this.updateProject.bind(this));
  }

  project_obj: Project;

  member_infos: MemberInfo[] = [
    new MemberInfo(1,"利俊安",0, [1,2,3,4,5],
      "804173948@qq.com","QQ 804173948", 2, false),
    new MemberInfo(2,"李光耀",0, [2,3,5],
      "123456789@qq.com","QQ 1169969860", 1, false),
    new MemberInfo(6,"吴宁",0, [3,5,6],
      "1010101010@qq.com","", 2, true),
    new MemberInfo(3,"张景维",0, [3,4],
      "4645678678@qq.com","", 2, false),
    new MemberInfo(4,"邹博韬",0, [3,4],
      "boruto@scut.edu","17701941369", 1, false),
    new MemberInfo(5,"曾声云",1, [6,7],
      "xingyun6@xingyun6.com","", 1, false)
  ];

  member_tasks: MemberTask[] = [
    new MemberTask(1,'利俊安',[1,2,3,4,5],50,
      5,25,20,40),
    new MemberTask(2,'李光耀',[2,3,5],8,
      1,2,5,62.5),
    new MemberTask(6,'吴宁',[3,5,6],33,
      11,0,22,66.67),
    new MemberTask(3,'邹博韬',[3,4],24,
      9,3,12,50),
    new MemberTask(4,'张景维',[3,4],40,
      2,2,36,90),
    new MemberTask(5,'曾声云',[6,7],16,
      10,4,2,12.5),
    new MemberTask(0,'总计',[],100, 20,
      28,52,52, true),
  ];

  ngOnInit() {
    this.updateProject();
  }

  updateProject() {
    this.project_obj = ProjectService.Project;
    let pid = this.router_info.snapshot.params['id'];
    if(this.project_obj && this.project_obj.id == pid) return;
    this.project.getProject(pid).subscribe(this.setProject.bind(this));
  }

  setProject(proj) {
    this.project_obj=proj;
  }

  taskClassNameFilter(row: MemberTask, index: number): string {
    return row.total ? 'green_row bold_row' : '';
  }
  infoClassNameFilter(row: MemberInfo, index: number): string {
    return row.status_id==DataSystem.OnlineStatusID ? 'green_row' : '';
  }

  onInfoDetail(scope) {
    console.info("onDetail",{scope});
  }
  onTaskDetail(scope) {
    console.info("onDetail",{scope});
  }
  onDelete(scope) {
    console.info("onDelete",{scope});
  }
  onAssign(scope) {
    console.info("onDelete",{scope});
  }

}
