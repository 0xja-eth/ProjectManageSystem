
class Data {
  constructor(public id:number, public name:string,
              public description:string=null) {}
}

export class DataSystem {
  public static Genders = ['男','女'];
  public static Educations : Data[];
  public static LoginStatuses : Data[];
  public static ProjectTypes : Data[];
  public static TaskStatuses : Data[];
  public static Roles : Data[];

  // 初始化所有数据
  public static initialize() {

  }

  // 获取数据
  // type: 类型
  // id: 根据ID获取
  // name: 根据名称获取
  public static get(type:string, id:number=null, name:string=null): Data {
    let container: Data[] = this[type];
    for(let data of container)
      if(data.id==id || data.name==name) return data;
  }
}
