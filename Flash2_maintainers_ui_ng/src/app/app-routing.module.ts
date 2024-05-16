import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './views/home/home.component';

const routes: Routes = [
  {path:'',component:HomeComponent},
  {path:'operations',loadChildren: () => import('./modules/operations/operations.module').then(mod => mod.OperationsModule)},
  {path:'requests',loadChildren: () => import('./modules/approval-requests/approval-requests.module').then(mod => mod.ApprovalRequestsModule)},
  {path:'params',loadChildren: () => import('./modules/params/params.module').then(mod => mod.ParamsModule)},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
