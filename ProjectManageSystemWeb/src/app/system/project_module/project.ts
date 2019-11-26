import {DataSystem} from '../data.system';

export class ProjectMember {
  constructor(public id: number,
              public name: string,
              public role_id: number,
              public contact: string
  ) {}

  role():string {
    return DataSystem.get('Roles', this.role_id).name;
  }
}

export class ProjectTask {
  constructor(public id: number,
              public order: number,
              public name: string,
              public progress: number,
              public level: number,
              public status_id: number,
              public start_date: string,
              public end_date: string
  ) {}

  status():string {
    return DataSystem.get('TaskStatuses', this.status_id).name;
  }
  levelText():string {
    return DataSystem.get('TaskLevels', this.level).name;
  }

  isCompleted():boolean {
    return this.status_id == DataSystem.CompletedStatusId;
  }
  isStarted():boolean {
    return this.status_id == DataSystem.StartedStatusId;
  }
  isFailed(): boolean {
    return this.status_id == DataSystem.FailedStatusId;
  }
}

export class Notice {
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

export class Project {
  constructor(public id: number,
              public name: string,
              public type_id?: number,
              public start_date?: string,
              public end_date?: string,
              public create_time?: string,
              public description?: string,
              public members: ProjectMember[] = [],
              public tasks: ProjectTask[] = [],
              public notices: Notice[] = []
  ) {}

  creator(): ProjectMember {
    if(this.members) return this.members.find(
      m=>m.role_id==DataSystem.ProjectManagerRoleId);
  }

  startedCount() {
    return this.tasks.filter(t=>t.isStarted()).length;
  }
  failedCount() {
    return this.tasks.filter(t=>t.isFailed()).length;
  }
  completedCount() {
    return this.tasks.filter(t=>t.isCompleted()).length;
  }
  completedRate() {
    if(this.tasks.length <= 0) return 0;
    return this.completedCount()/this.tasks.length*100;
  }

  progressRate() {
    if(this.tasks.length <= 0) return 0;
    let rate = this.tasks.reduce((tot, t)=>tot+t.progress,0);
    return rate/this.tasks.length;
  }
  timeRate() {
    if(this.deltaTime() <= 0) return 0;
    return this.passedTime()/this.deltaTime()*100;
  }

  startTime():Date {
    return new Date(this.start_date);
  }
  endTime():Date {
    return new Date(this.end_date);
  }
  deltaTime() {
    // @ts-ignore
    return this.endTime()-this.startTime();
  }
  passedTime() {
    // @ts-ignore
    return (new Date())-this.startTime();
  }

  memberIds(): number[] | void {
    if(this.members) return this.members.map(m=>m.id);
  }
  taskIds(): number[] | void {
    if(this.tasks) return this.tasks.map(m=>m.id);
  }

  type():string {
    return DataSystem.get('ProjectTypes', this.type_id).name;
  }

  publishNotice(noticeContent: string): void {
    this.notices.push(new Notice(noticeContent));
  }
}
