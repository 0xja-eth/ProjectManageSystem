import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MainModule } from './page/main/main.module';
import { LoginModule } from './page/login/login.module';
import { MainComponent } from './page/main/main.component';
import { LoginComponent } from './page/login/login.component';

const routes: Routes = [
  {
    path: 'main', component: MainComponent,
    loadChildren: () => import('./page/main/main.module').then(mod => mod.MainModule),
  },
  { path: 'welcome/:type', component: LoginComponent, },
  { path: '', redirectTo: '/welcome/login', pathMatch: 'full' },
  { path: 'welcome', redirectTo: '/welcome/login', pathMatch: 'full' },
  { path: 'login', redirectTo: '/welcome/login', pathMatch: 'full' },
  { path: 'register', redirectTo: '/welcome/register', pathMatch: 'full' },
  { path: 'forget', redirectTo: '/welcome/forget', pathMatch: 'full' }
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes,
      { enableTracing: true})
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
