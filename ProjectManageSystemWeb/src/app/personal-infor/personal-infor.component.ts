import {Component, forwardRef, Inject, OnInit} from '@angular/core';
import {SafeUrl} from '@angular/platform-browser';
import { ElMessageService} from 'element-angular/release/message/message.service';
import { DomSanitizer} from "@angular/platform-browser";
import {AbstractControl, FormBuilder, FormControl, FormGroup} from "@angular/forms";

@Component({
  selector: 'app-personal-infor',
  templateUrl: './personal-infor.component.html',
  styleUrls: ['./personal-infor.component.css']
})

export class PersonalInforComponent implements OnInit {
  private personalForm: FormGroup;
  private imageUrl: SafeUrl;
  private personsex: any[] = [
    {label: '男', value: 'man'},
    {label: '女', value: 'woman'}
    ];
  private sexValue: string;
  private edubgs: any[] =  [
    {label: '小学', education: 'primary_school'},
    {label: '初中', education: 'junior_school'},
    {label: '高中', education: 'senior_school'},
    {label: '大学', education: 'university'},
    {label: '研究生', education: 'graduate'}
  ];


  constructor(private message: ElMessageService,
              private sanitizer: DomSanitizer,
              @Inject(forwardRef(() => FormBuilder)) private formBuilder: FormBuilder) { }

  ngOnInit() {
    this.personalForm = this.formBuilder.group({
      nickName: ['', [this.nickValidator]],
      realName: ['', [this.realValidator]],
      sex: [''],
      birthday: [''],
      address: ['', [this.addValidator]],
      edubg: [''],
      job: [''],
      contact: [''],
      description: ['']
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
  }

  private realValidator = (control: FormControl): ValidateResult => {
    if (!control.value) {
      return { status: 'error', message: '必须输入真实姓名'};
    }
    return { status: 'success', message: ''};
  }

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
