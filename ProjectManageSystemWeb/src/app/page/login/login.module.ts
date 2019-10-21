import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { LoginRoutingModule } from './login-routing.module';
import { LoginComponent } from './login.component';
import { ShareModule } from '../../share/share.module';
import { LoginWindowComponent } from './login-window/login-window.component';
import {UserSystem} from '../../system/user_module/user_system';
import {NetworkSystem} from '../../system/network_system';


@NgModule({
  declarations: [
    LoginComponent,
    LoginWindowComponent
  ],
  imports: [
    ShareModule,
    LoginRoutingModule
  ],
  providers: [UserSystem, NetworkSystem]
})
export class LoginModule { }
