import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-notice',
  templateUrl: './notice.component.html',
  styleUrls: ['./notice.component.css']
})
export class NoticeComponent implements OnInit {
  existingProjects: Project[];

  constructor() { }

  ngOnInit() {
    this.existingProjects = [
      new Project('百日高考', '00001', 'Adam'),
      new Project('Exermon', '00002', 'Bill'),
      new Project('项目管理', '00003', 'Cindy'),
      new Project('软件测试', '00004', 'David'),
      new Project('test', '00005', 'Eric')
    ];
    this.existingProjects[0].publishNotice('abcd');
    this.existingProjects[0].publishNotice('abcd');
    console.log(this.existingProjects[0].notices);
  }



}

class Project {
  projectName: string;
  projectID: string;
  projectManager: string;
  notices: Notice[] = [];
  constructor(projectName: string, projectID: string, projectManager: string) {
    this.projectName = projectName;
    this.projectID = projectID;
    this.projectManager = projectManager;
  }
  publishNotice(noticeContent: string): void {
    this.notices.push(new Notice(noticeContent));
  }
}

class Notice {
  content: string;
  date: Date;
  day: string;
  time: string;
  constructor(content: string) {
    this.content = content;
    this.date = new Date();
    this.day = this.date.getFullYear() + '/' + (this.date.getMonth() + 1) + '/' + this.date.getDate();
    const hour = this.date.getHours();
    const minute = (this.date.getMinutes() < 10) ? ('0' + this.date.getMinutes().toString()) : this.date.getMinutes().toString();
    this.time = hour + ':' + minute;

  }
}


