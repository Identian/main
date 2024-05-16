import { MsalService } from "@azure/msal-angular";
import {Router} from "@angular/router"
import {inject} from "@angular/core"

export namespace AuthGuard{
  export const canActivate = ()=>{
    const msalService = inject(MsalService);
    const router = inject(Router);
  }
}
