import { Injectable } from '@angular/core';
import { MsalService } from "@azure/msal-angular";
import {Router} from "@angular/router"
import { AuthenticationResult} from "@azure/msal-browser";
import { environment } from 'src/environments/environment';

const loginRequest = {
  scopes: ['User.Read'],
  // prompt: 'login',
};

@Injectable({
  providedIn: 'root',
})


export class AuthService {
  constructor(private msalService: MsalService, private router: Router) {}

  logIn() {
    this.msalService.loginPopup(loginRequest).subscribe((response: AuthenticationResult) => {
            this.msalService.instance.setActiveAccount(response.account)
            this.msalService.handleRedirectObservable().subscribe(() => {
                const silentRequest = {
                    scopes: [environment.azureAuthConfig.clientId + "/.default"],
                    account: this.msalService.instance.getActiveAccount()!
                }
                this.msalService.instance.acquireTokenSilent(silentRequest).then(response => {
                    sessionStorage.setItem('token', JSON.stringify(response))
                    this.router.navigate(['request'])
                })
            })
        })
    /*this.msalService
      .loginPopup(loginRequest)
      .subscribe((response: AuthenticationResult) => {
        this.msalService.instance.setActiveAccount(response.account);
        this.msalService.handleRedirectObservable().subscribe(() => {
          this.router.navigate(['request']);
        });
      });*/
  }

  logOut() {
    this.msalService.logoutPopup({
      mainWindowRedirectUri: '/login',
    });
  }

  isLoggedIn(): boolean {
    return this.msalService.instance.getActiveAccount() != null;
  }

  userInfo() {
    return this.msalService.instance.getActiveAccount();
  }

  validateTokenExp() {

        const tokenExpirateOn: any = JSON.parse(sessionStorage.getItem('token')!)
        const forceRefresh = (new Date(tokenExpirateOn.expiresOn) < new Date());
        if (forceRefresh) {
            return true
        }
        return false
    }

    async refreshToken() {

        const silentRequest = {
            scopes: [environment.azureAuthConfig.clientId + "/.default"],
            account: this.msalService.instance.getActiveAccount()!
        }

        await this.msalService.instance.acquireTokenSilent(silentRequest).then(response => {
            sessionStorage.setItem('token', JSON.stringify(response))
        })

    }
}
