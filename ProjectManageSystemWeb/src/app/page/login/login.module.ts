import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { LoginRoutingModule } from './login-routing.module';
import { LoginComponent } from './login.component';
import { ShareModule } from '../../share/share.module';
import { LoginWindowComponent } from './login-window/login-window.component';
import {UserService} from '../../system/user_module/user.service';
import {NetworkService} from '../../system/network.service';


@NgModule({
  declarations: [
    LoginComponent,
    LoginWindowComponent
  ],
  imports: [
    ShareModule,
    LoginRoutingModule
  ],
  providers: [UserService, NetworkService]
})
export class LoginModule { }
