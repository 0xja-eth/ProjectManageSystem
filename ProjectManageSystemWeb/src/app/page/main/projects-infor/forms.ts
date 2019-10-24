import { Form } from '../../../system/user_module/user_system';
import {ConfigSystem} from '../../../system/config_system';
import {Observable} from 'rxjs';
import {ProjectSystem} from '../../../system/project_module/project_system';
import {DataSystem} from '../../../system/data_system';

export class ProjectForm extends Form{
  constructor(name:string,
              public pid: number=-1,
              public pname: string='',
              public type_id: number=1,
              public start_date: string='',
              public description: string='',
  ){
    super(name);
  }

  do(service:ProjectSystem, type?) : Observable<Object> {
    if(!this.checkDo(type)) return;
    if(this.pid>0) {
      /*return service.editProject(this.pid, this.pname,
        this.type_id, this.description, this.start_date);*/
    } else {
      /*return service.newProject(this.pname, this.type_id,
        this.description, this.start_date);*/
    }

  }

  checkAll(type?): { message?: string; status: string }  {
    let res: { message?: string; status: string } = {status: 'success'};
    if(res.status=='success') res = this.checkSingle('pname', this.pname);
    if(res.status=='success') res = this.checkSingle('type_id', this.type_id);
    if(res.status=='success') res = this.checkSingle('description', this.description);
    if(res.status=='success') res = this.checkSingle('start_date', this.start_date);
    return res;
  }

  protected checkSingle(type:'pname' |
    'type_id' | 'description' | 'start_date', val) {
    switch (type) {
      case 'pname': return this.checkProjectName(val);
      case 'type_id': return this.checkTypeId(val);
      case 'start_date': return this.checkStartDate(val);
      case 'description': return this.checkDescription(val);
      default: return {status: 'error', message: ConfigSystem.UnknownType}
    }
  }

  checkProjectName(val:string) {
    if (!val) return { status: 'error', message: ConfigSystem.PnEmpty};
    if (val.length > ConfigSystem.PnLength)
      return { status: 'error', message: ConfigSystem.PnLong };
    return { status: 'success' }
  }
  checkTypeId(val:number) {
    if (!val) return { status: 'error', message: ConfigSystem.PTypeEmpty };
    if (!DataSystem.contains('ProjectTypes', val))
      return { status: 'error', message: ConfigSystem.PTypeError };
    return { status: 'success' }
  }
  checkStartDate(val:string) {
    if (!val) return { status: 'error', message: ConfigSystem.StartDateEmpty };
    return { status: 'success' }
  }
  checkDescription(val:string) {
    if (val.length > ConfigSystem.PDescLength)
      return { status: 'error', message: ConfigSystem.PDescLong };
    return { status: 'success' }
  }
}

