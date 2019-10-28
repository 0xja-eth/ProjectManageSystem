
import {InterfaceSystem, NetworkSystem} from './network_system';
import {Injectable} from '@angular/core';
import {ConfigSystem} from './config_system';

class Data {
  static EMPTY = new Data(-1,'未知数据');
  constructor(public id:number, public name:string,
              public description:string=null) {}
}

@Injectable()
export class DataSystem {
  static Genders = [new Data(0,'男'), new Data(1,'女')];
  static Educations : Data[];
  static LoginStatuses : Data[];
  static ProjectTypes : Data[];
  static TaskStatuses : Data[];
  static TaskLevels : Data[];
  static Roles : Data[];

  static OfflineStatusID = 1;
  static OnlineStatusID = 2;

  static ProjectManagerRoleId = 1;

  static BeforeStartStatusId = 1;
  static StartedStatusId = 2;
  static CompletedStatusId = 3;
  static FailedStatusId = 4;
  static PausedStatusId = 5;
  static CancelledStatusId = 6;

  constructor(private network: NetworkSystem){ }

  // 初始化所有数据
  initialize() {
    this.network.send(InterfaceSystem.Interfaces.InitializeData)
      .subscribe(DataSystem.saveData);
  }

  private static saveData(data) {
    DataSystem.Educations = data.Educations;
    DataSystem.LoginStatuses = data.LoginStatuses;
    DataSystem.ProjectTypes = data.ProjectTypes;
    DataSystem.TaskStatuses = data.TaskStatuses;
    DataSystem.TaskLevels = data.TaskLevels;
    DataSystem.Roles = data.Roles;

    DataSystem.OfflineStatusID = data.OfflineStatusID;
    DataSystem.OnlineStatusID = data.OnlineStatusID;

    DataSystem.ProjectManagerRoleId = data.ProjectManagerRoleId;

    DataSystem.BeforeStartStatusId = data.BeforeStartStatusId;
    DataSystem.StartedStatusId = data.StartedStatusId;
    DataSystem.CompletedStatusId = data.CompletedStatusId;
    DataSystem.FailedStatusId = data.FailedStatusId;
    DataSystem.PausedStatusId = data.PausedStatusId;
    DataSystem.CancelledStatusId = data.CancelledStatusId;

    ConfigSystem.UnLength = data.UnLength;
    ConfigSystem.PwdLength = data.PwdLength;
    ConfigSystem.EmailReg = data.EmailReg;
    ConfigSystem.CodeLength = data.CodeLength;
    ConfigSystem.CodeSecond = data.CodeSecond;

    console.info("saveData", DataSystem, ConfigSystem);
  }

  // 获取数据
  // type: 类型
  // id: 根据ID获取
  // name: 根据名称获取
  static get(type:string, id:number=null, name:string=null): Data {
    let container: Data[] = this[type];
    for(let index in container){
      let data = container[index];
      if(data.id==id || data.name==name) return data;
    }
    return Data.EMPTY;
  }

  // 判断数据
  static contains(type:string, id:number=null, name:string=null): boolean {
    return DataSystem.get(type, id, name) != Data.EMPTY;
  }
}
