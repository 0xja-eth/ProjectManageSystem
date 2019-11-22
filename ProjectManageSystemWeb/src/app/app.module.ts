import {NgModule} from '@angular/core';

import { AppComponent } from './app.component';

import {CoreModule} from './core/core.module';
import {DataSystem} from './system/data.system';


@NgModule({
  declarations: [
    AppComponent,
  ],
  imports: [
    CoreModule,
  ],
  providers: [DataSystem],
  bootstrap: [AppComponent]
})

export class AppModule {
}
