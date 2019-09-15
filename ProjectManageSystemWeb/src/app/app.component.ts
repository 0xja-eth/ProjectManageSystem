import { Component } from '@angular/core';
import {InputData} from './input-field/input_data';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'ProjectManageSystemWeb';
  handle = function(index: string): void {
    console.log(index)
  };

  onLogin = function($event): void {
    console.info($event);
  }
  onRegister = function($event): void {
    console.info($event);
  }
}
