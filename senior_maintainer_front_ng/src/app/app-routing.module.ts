import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthGuard } from './guards/auth.guard';

const routes: Routes = [
  {path:'request',loadChildren: () => import('./modules/request/request.module').then(mod => mod.RequestModule),canActivate:[AuthGuard.canActivate]},
  {path:'login',loadChildren: () => import('./modules/auth/auth.module').then(mod => mod.AuthModule)},
  {path:'',redirectTo:'login',pathMatch:'full'}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
