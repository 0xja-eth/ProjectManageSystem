import { NgModule } from '@angular/core';
import {MainModule} from './main/main.module';
import {LoginModule} from './login/login.module';


@NgModule({
  declarations: [],
  imports: [
    LoginModule,
    MainModule,
  ],
  exports: [
    LoginModule,
    MainModule,
  ]
})
export class PageModule { }
