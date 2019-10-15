import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { GanttModule } from './gantt/gantt.module';

import { ElModule } from 'element-angular';
import { InputFieldComponent } from './input-field/input-field.component';
import {FormsModule} from '@angular/forms';
import { LoginComponent } from './login/login.component';
import { RouterModule, Routes} from '@angular/router';
import { PersonalInforComponent } from './personal-infor/personal-infor.component';
import { CodeChangeComponent } from './code-change/code-change.component';
import { ReactiveFormsModule} from "@angular/forms";
import { ChatRoomComponent } from './chat-room/chat-room.component';
import { ChatDetailComponent } from './chat-detail/chat-detail.component';

// import {DayPilotModule} from 'daypilot-pro-angular';

@NgModule({
  declarations: [
    AppComponent,
    InputFieldComponent,
    LoginComponent,
    PersonalInforComponent,
    CodeChangeComponent,
    ChatRoomComponent,
    ChatDetailComponent,
    /*GanttComponent*/
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    AppRoutingModule,
    GanttModule,
    ElModule.forRoot(),
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})

export class AppModule {
}
