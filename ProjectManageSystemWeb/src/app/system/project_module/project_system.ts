
import {Injectable} from '@angular/core';
import {InterfaceSystem, NetworkSystem} from '../network_system';
import {Project, ProjectMember, ProjectTask} from './project';
import {Observable} from 'rxjs';
import {UserSystem} from '../user_module/user_system';

@Injectable()
export class ProjectSystem{
  static Project: Project;

  public static setProject(proj) {
    ProjectSystem.Project = proj;
  }

  public static checkPrivilege() {
    return true;
  }

  projects_data: Project[] = [
    new Project(1, "百日高考",0,
      "2019/10/22 12:33:44", "2019/10/25 12:33:44",
      "2019/10/22 10:33:44", "一个学习游戏，很好玩的。",
      [
        new ProjectMember(1,"利俊安",1, "QQ 804173948"),
        new ProjectMember(2,"李光耀",2, "QQ 1169969860"),
        new ProjectMember(3,"张景维",3, ""),
        new ProjectMember(4,"邹博韬",3, "17701941369"),
        new ProjectMember(5,"曾声云",3, "")
      ],[
        new ProjectTask(1, 1, "启动阶段", 100,1,
          3, '2019/9/20 12:23:34', '2019/10/02 12:23:34'),
        new ProjectTask(2, 2, "计划阶段", 100, 1,
          3, '2019/10/02 15:23:34', '2019/10/21 02:23:34'),
        new ProjectTask(3, 3, "执行阶段", 44,1,
          2, '2019/10/04 01:23:34', '2019/11/24 12:23:34'),
        new ProjectTask(4, 4, "监督控制阶段", 68,1,
          2, '2019/10/12 12:20:35', '2019/11/20 23:23:34'),
        new ProjectTask(5, 5, "收尾阶段",  0,1,
          1, '2019/11/24 10:21:34', '2019/12/02 12:23:34'),
      ]),
    new Project(2, "艾瑟萌学院",0,
      "2019/10/26 15:33:44", "2019/10/30 12:33:44",
      "2019/10/22 12:33:44", "《百日高考》的进化版。",
      [
        new ProjectMember(1,"利俊安",1, "QQ 804173948"),
        new ProjectMember(2,"李光耀",2, "QQ 1169969860"),
        new ProjectMember(4,"邹博韬",3, "17701941369"),
      ]),
    new Project(3, "星云6项目管理系统",0,
      "2019/10/26 05:33:44", "2019/11/30 12:33:44",
      "2019/10/22 02:33:44", "本项目管理系统。基于Angular8" +
      "和Django开发，是一个先进的项目管理系统。拥有用户模块、项目模块、任务模块和聊天模块，" +
      "是一个强大的项目管理辅助工具。现在买入只需998，只需998就能终身体验一流的项目管理辅助" +
      "服务！心动不如行动，赶紧打进电话预约吧！",
      [
        new ProjectMember(1,"利俊安",1, "QQ 804173948"),
        new ProjectMember(2,"李光耀",2, "QQ 1169969860"),
        new ProjectMember(6,"吴宁",4, ""),
        new ProjectMember(3,"张景维",3, ""),
        new ProjectMember(4,"邹博韬",3, "17701941369"),
        new ProjectMember(5,"曾声云",3, "")
      ],[
        new ProjectTask(1, 1, "启动阶段", 100,1,
          3, '2019/9/20 12:23:34', '2019/10/02 12:23:34'),
        new ProjectTask(2, 2, "计划阶段", 100, 1,
          3, '2019/10/02 15:23:34', '2019/10/21 02:23:34'),
        new ProjectTask(3, 3, "执行阶段", 44,1,
          2, '2019/10/04 01:23:34', '2019/11/24 12:23:34'),
        new ProjectTask(4, 4, "监督控制阶段", 68,1,
          2, '2019/10/12 12:20:35', '2019/11/20 23:23:34'),
        new ProjectTask(5, 5, "收尾阶段",  0,1,
          1, '2019/11/24 10:21:34', '2019/12/02 12:23:34'),
      ]),
    new Project(4, "星云7黑市系统",0,
      "2019/10/26 05:33:44", "2019/12/31 15:33:44",
      "2019/10/10 22:33:44", "基于命令行的高级黑市系统。",
      [
        new ProjectMember(5,"曾声云",1, "")
      ]),
  ];

  constructor(private network: NetworkSystem) {

  }

  getProjects() {
    return new Observable<Project[]>((obs)=>obs.next(this.projects_data));
    //return this.network.send(InterfaceSystem.Interfaces.GetProjects);
  }

  getProject(pid) {
    return new Observable<Project>((obs)=>obs.next(
      this.projects_data.find(p=>p.id==pid)));
    //return this.network.send(InterfaceSystem.Interfaces.GetProject, {pid});
  }

  getTasks(tids=[], pid=null, uid=null) {

  }
  getTask(tid) {

  }

  newProject(name, type_id, desc, start_date) {

  }
  editProject(pid, name, type_id, desc, start_date) {

  }
  endProject(pid, pwd) {

  }

  addMember(pid, mids, pwd) {

  }
  deleteMember(pid, mids, pwd) {

  }

}
