import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor
} from '@angular/common/http';
import { Observable, finalize, from, lastValueFrom } from 'rxjs';
import { NgxSpinnerService } from 'ngx-spinner';
import { AuthService } from '../services/auth.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(private spinnerService: NgxSpinnerService, private authenticationService: AuthService) {

  }

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    return from(this.handle(request, next))
  }

  async handle(req: HttpRequest<any>, next: HttpHandler) {

    this.spinnerService.show();

    if (this.authenticationService.validateTokenExp()) {

        await this.authenticationService.refreshToken()

        let token = JSON.parse(sessionStorage.getItem('token')!).accessToken
        req = req.clone({
            headers: req.headers.set('Authorization', `${token}`)
        });

        return await lastValueFrom(next.handle(req).pipe(
            finalize(() => {
                this.spinnerService.hide()
            })
        ))
    }

    let token = JSON.parse(sessionStorage.getItem('token')!).accessToken

    req = req.clone({
        headers: req.headers.set('Authorization', `${token}`)
    });

    return await lastValueFrom(next.handle(req).pipe(
        finalize(() => {
            this.spinnerService.hide()
        })
    ))

}
}
