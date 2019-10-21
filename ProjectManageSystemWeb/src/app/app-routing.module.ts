import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MainModule } from './page/main/main.module';
import { LoginModule } from './page/login/login.module';
import { MainComponent } from './page/main/main.component';
import { LoginComponent } from './page/login/login.component';

const routes: Routes = [
  {
    path: 'main', component: MainComponent
    //loadChildren: () => import('./page/main/main.module').then(mod => mod.MainModule),
  },
  {
    path: 'login/:type', component: LoginComponent,
    //loadChildren: () => import('./page/login/login.module').then(mod => mod.LoginModule),
    data: {type: 'Register'}
  },
  { path: '', redirectTo: '/login/login', pathMatch: 'full' },
  { path: 'login', redirectTo: '/login/login', pathMatch: 'full' },
  { path: 'register', redirectTo: '/login/register', pathMatch: 'full' },
  { path: 'forget', redirectTo: '/login/forget', pathMatch: 'full' }
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes,
      { enableTracing: true})
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
