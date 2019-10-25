import {Component, forwardRef, Inject, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from '@angular/router';
import {ProjectsInforComponent} from '../projects-infor.component';
import {Project} from '../../../../system/project_module/project';
import { ProjectSystem } from 'src/app/system/project_module/project_system';
import {AbstractControl, FormBuilder, FormGroup} from '@angular/forms';
import {ProjectForm} from '../forms';
import {ConfigSystem} from '../../../../system/config_system';
import {DataSystem} from '../../../../system/data_system';

@Component({
  selector: 'app-edit',
  templateUrl: './edit.component.html',
  styleUrls: ['./edit.component.css']
})
export class EditComponent implements OnInit {

  DataSystem = DataSystem;
  ConfigSystem = ConfigSystem;
  ProjectSystem = ProjectSystem;
  father = ProjectsInforComponent;

  constructor(private router:Router,
              private project: ProjectSystem,
              private router_info: ActivatedRoute,
              @Inject(forwardRef(() => FormBuilder))
                private formBuilder: FormBuilder) {
    // 当路由发生变化，存储在浏览器里面的的用户信息发生变化的时候刷新组件
    router.events.subscribe(this.updateProject.bind(this));
  }

  static FormName = '修改项目';

  project_obj: Project;

  inputForm : ProjectForm;

  formGroup: FormGroup;

  ngOnInit() {
    this.updateProject();
  }

  updateProject() {
    this.project_obj = ProjectSystem.Project;
    let pid = this.router_info.snapshot.params['id'];
    if(this.project_obj && this.project_obj.id == pid)
      return this.makeProjectEditForm();
    this.project.getProject(pid).subscribe(this.setProject.bind(this));
  }

  setProject(proj) {
    this.project_obj = proj;
    this.makeProjectEditForm();
  }

  makeProjectEditForm() {
    this.inputForm = new ProjectForm(EditComponent.FormName,
      this.project_obj.id, this.project_obj.name, this.project_obj.type_id,
      this.project_obj.start_time, this.project_obj.description);
    this.formGroup = this.formBuilder.group(this.inputForm);
  }


  statusCtrl(item: string): string {
    let control: AbstractControl = this.formGroup.controls[item];
    this.inputForm[item] = control.value;
    let res = this.inputForm.check(item, control);
    return control.dirty ? res.status : '';
  }

  messageCtrl(item: string): string {
    let control: AbstractControl = this.formGroup.controls[item];
    this.inputForm[item] = control.value;
    let res = this.inputForm.check(item, control);
    return control.dirty ? res.message : '';
  }

  onEdit() {
    this.inputForm.do(this.project);
  }
  onDelete() {

  }

}
