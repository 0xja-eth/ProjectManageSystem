import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {InputData} from './input_data';
import {AbstractControl, FormGroup} from '@angular/forms';

@Component({
  selector: 'app-input-field',
  templateUrl: './input-field.component.html',
  styleUrls: ['./input-field.component.css']
})
export class InputFieldComponent implements OnInit {

  @Input() inputData: {key: InputData};
  @Input() key: string;
  //@Input() messageCtrl;

  validateForm: FormGroup;

  @Output() onClick = new EventEmitter();

  constructor() { }

  ngOnInit() { }

  statusCtrl(item: string): string {
    console.error("statusCtrl: ", item, this.validateForm);
    if (!this.validateForm.controls[item]) return;
    const control: AbstractControl = this.validateForm.controls[item];
    return control.dirty && control.hasError('status') ? control.errors.status : '';
  }

  messageCtrl(item: string): string {
    if (!this.validateForm.controls[item]) return;
    const control: AbstractControl = this.validateForm.controls[item];
    return control.dirty && control.hasError('message') ? control.errors.message : '';
  }

}
