import {DataSystem} from '../data_system';

export class Stranger {
  constructor(public id: number,
              public username: string,
              public description: string
  ) {}
}

export class User {

  constructor(public id: number,
              public username: string,
              public email: string,
              public name: string,
              public gender: string,
              public avatar: string,
              public birth: string,
              public city: string,
              public education_id: number,
              public duty: string,
              public contact: string,
              public description: string,
              public create_time: string,
              public status_id: number
  ) {}

  education():string {
    return DataSystem.get('Educations', this.education_id).name;
  }
  status():string {
    return DataSystem.get('LoginStatuses', this.status_id).name;
  }
}
