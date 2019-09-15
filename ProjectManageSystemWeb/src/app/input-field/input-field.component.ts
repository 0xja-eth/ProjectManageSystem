import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {InputData} from './input_data';

@Component({
  selector: 'app-input-field',
  templateUrl: './input-field.component.html',
  styleUrls: ['./input-field.component.css']
})
export class InputFieldComponent implements OnInit {

  @Input() data: InputData;
  @Output() onClick = new EventEmitter();

  constructor() { }

  ngOnInit() { }

}
