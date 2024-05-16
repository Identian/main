import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';

import { NgxSpinnerModule } from 'ngx-spinner';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { SweetAlert2Module } from '@sweetalert2/ngx-sweetalert2';
import { IPublicClientApplication, PublicClientApplication } from '@azure/msal-browser';
import { MSAL_INSTANCE, MsalService } from '@azure/msal-angular';
import { environment } from 'src/environments/environment';
import { AuthInterceptor } from './interceptors/auth-interceptor.interceptor';

const isIE =
  window.navigator.userAgent.indexOf('MSIE ') > -1 ||
  window.navigator.userAgent.indexOf('Trident/') > -1;

export function MSLAInstanceFactory(): IPublicClientApplication {
  return new PublicClientApplication({
    auth: {
      clientId: environment.azureAuthConfig.clientId,
      authority: environment.azureAuthConfig.authority,
    },
    cache: {
      cacheLocation: 'sessionStorage',
      storeAuthStateInCookie: isIE,
    },
  });
}

@NgModule({
  declarations: [AppComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    NgxSpinnerModule,
    SweetAlert2Module.forRoot(),
  ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  providers: [
    { provide: MSAL_INSTANCE, useFactory: MSLAInstanceFactory }, MsalService,
    {provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true}
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
