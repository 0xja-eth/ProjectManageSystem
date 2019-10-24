
import {InterfaceSystem, NetworkSystem} from './network_system';
import {Injectable} from '@angular/core';

class Data {
  static EMPTY = new Data(-1,'未知数据');
  constructor(public id:number, public name:string,
              public description:string=null) {}
}

@Injectable()
export class DataSystem {
  static Genders = ['男','女'];
  static Educations : Data[];
  static LoginStatuses : Data[];
  static ProjectTypes : Data[];
  static TaskStatuses : Data[];
  static TaskLevels : Data[];
  static Roles : Data[];

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
      .subscribe(this.saveData);
  }

  private saveData(data) {
    console.info(data);
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
