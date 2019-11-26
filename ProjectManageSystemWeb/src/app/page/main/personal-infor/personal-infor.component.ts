import {Component, forwardRef, Inject, OnInit} from '@angular/core';
import {SafeUrl} from '@angular/platform-browser';
import { ElMessageService} from 'element-angular/release/message/message.service';
import { DomSanitizer} from "@angular/platform-browser";
import {AbstractControl, FormBuilder, FormControl, FormGroup} from "@angular/forms";
import {UserService} from '../../../system/user_module/user.service';
import {ConfigSystem} from '../../../system/config.system';
import {DataSystem} from '../../../system/data.system';

@Component({
  selector: 'app-personal-infor',
  templateUrl: './personal-infor.component.html',
  styleUrls: ['./personal-infor.component.css']
})

export class PersonalInforComponent implements OnInit {
  private personalForm: FormGroup;
  private imageUrl: SafeUrl;
  private sexValue: string;

  DataSystem = DataSystem;

  constructor(private message: ElMessageService,
              private user: UserService,
              private sanitizer: DomSanitizer,
              @Inject(forwardRef(() => FormBuilder)) private formBuilder: FormBuilder) { }

  ngOnInit() {
    this.personalForm = this.formBuilder.group({
      /*nickName: ['', [this.nickValidator]],*/
      name: ['', [this.realValidator]],
      gender: [''],
      birth: [''],
      city: ['', [this.addValidator]],
      edu_id: [''],
      duty: [''],
      contact: [''],
      desc: ['']
    });
  }

  successHandle(file: any): void {
    this.imageUrl = this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(file.raw));
    this.message.info('文件上传成功');
  }

  errorHandle(err: any): void {
    this.message.error('文件上传失败:' + err);
  }

  sexHandle(event: any): void {
    this.sexValue = event;
  }

  timeHandle(time: any): void {
    console.log(time);
  }

  eduHandle(event: any): void {
    console.log(event);
  }

  submit(): void {
    console.log(this.personalForm.value);

    let name = this.personalForm.value.name;
    let gender = this.personalForm.value.gender;
    let birth = this.personalForm.value.birth;
    let city = this.personalForm.value.city;
    let edu_id = this.personalForm.value.edu_id;
    let duty = this.personalForm.value.duty;
    let contact = this.personalForm.value.contact;
    let desc = this.personalForm.value.desc;

    this.user.editInfo(name, gender, birth, city, edu_id, duty, contact, desc);
  }

  // statusCtrl(item: string): string {
  //   if (!this.personalForm.controls[item]) {
  //     const control: AbstractControl = this.personalForm.controls[item];
  //     return control
  //   }
  //   return control.dirty && control.hasError('status') ? control.errors.status : '';
  // }

  private nickValidator = (control: FormControl): ValidateResult => {
    if (!control.value) {
      return { status: 'error', message: '必须输入用户名'};
    }
    return { status: 'success', message: ''};
  };

  private realValidator = (control: FormControl): ValidateResult => {
    if (!control.value) {
      return { status: 'error', message: '必须输入真实姓名'};
    }
    return { status: 'success', message: ''};
  };

  private addValidator = (control: FormControl): ValidateResult => {
    if (!control.value) {
      return { status: 'error', message: '必须输入地址'};
    }
    if (!/[一-龥]/.test(control.value)) {
      return { status: 'error', message: '必须输入中文'};
    }
    return { status: 'success', message: ''};
  }
}
class ValidateResult {
  status: string;
  message: string;
}
