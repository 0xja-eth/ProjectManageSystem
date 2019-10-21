import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {ElModule} from 'element-angular/release/element-angular.module';

// ShareModule: 储存全局指令、模块

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    ElModule
  ],
  exports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    ElModule
  ]
})
export class ShareModule { }
