import { Component, OnInit} from '@angular/core';
import { NgxSpinnerService } from 'ngx-spinner';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit{
  constructor(private authService: AuthService, private spinnerService: NgxSpinnerService){}
  ngOnInit(): void {
    this.spinnerService.show();
    this.authService.logIn();
  }
  logIn(){
    this.authService.logIn();
  }

}
