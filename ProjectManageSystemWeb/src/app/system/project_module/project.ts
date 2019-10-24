import {DataSystem} from '../data_system';

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
              public start_time: string,
              public end_time: string
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

export class Project {
  constructor(public id: number,
              public name: string,
              public type_id?: number,
              public start_time?: string,
              public end_time?: string,
              public create_time?: string,
              public description?: string,
              public members: ProjectMember[] = [],
              public tasks: ProjectTask[] = [],

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
    return this.completedCount()/this.tasks.length*100;
  }

  progressRate() {
    let rate = this.tasks.reduce((tot, t)=>tot+t.progress,0);
    return rate/this.tasks.length;
  }
  timeRate() {
    return this.passedTime()/this.deltaTime()*100;
  }

  startTime():Date {
    return new Date(this.start_time);
  }
  endTime():Date {
    return new Date(this.end_time);
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
}
