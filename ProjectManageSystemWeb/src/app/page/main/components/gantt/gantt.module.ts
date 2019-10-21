// @ts-ignore
// import {DataService} from './data.service';
// import {HttpClient} from '@angular/common/http';
import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {BrowserModule} from '@angular/platform-browser';
import {DayPilotModule} from 'daypilot-pro-angular';
import {GanttComponent} from './gantt.component';

@NgModule({
  imports:      [
    BrowserModule,
    FormsModule,
    // HttpClient,
    DayPilotModule
  ],
  declarations: [
    GanttComponent
  ],
  exports:      [ GanttComponent ],
  providers:    [ /*DataService*/ ]
})
export class GanttModule { }
