import { CUSTOM_ELEMENTS_SCHEMA, NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { RequestRoutingModule } from './request-routing.module';
import { BuilderComponent } from './builder/builder.component';
import { HTTP_INTERCEPTORS } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { MSAL_INSTANCE } from '@azure/msal-angular';
import { MSLAInstanceFactory } from 'src/app/app.module';


@NgModule({
  declarations: [
    BuilderComponent
  ],
  imports: [
    CommonModule,
    RequestRoutingModule,
    ReactiveFormsModule
  ],schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class RequestModule { }
