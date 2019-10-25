import {Component, ComponentFactoryResolver} from '@angular/core';

import {ViewSystem} from './system/view_system';
import {DataSystem} from './system/data_system';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = '*星云*6项目管理系统';

  ViewSystem = ViewSystem;

  constructor(private data: DataSystem) {
    data.initialize();
  }

  showAlert() {

  }
}
