import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import { MaintainerFormData } from '../model/MaintainerFormData.model';
import { ConsultModel } from '../model/Consult.model';
import { ConsultVerifyResponseModel } from '../model/ConsultVerifyResponse.model';
import { RequestModel } from '../model/Request.model';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class MaintainerService {
  constructor(private http: HttpClient) { }
  getFields():Observable<MaintainerFormData>{
    return this.http.get<MaintainerFormData>(environment.apiConfiguration.apiBaseURI+environment.apiConfiguration.apiEndPoints.fieldsEndpoint);
  }

  validateQuery(consult: ConsultModel){
    const body = JSON.stringify(consult);
    const headers = { 'content-type': 'application/json'};
    return this.http.post(environment.apiConfiguration.apiBaseURI+environment.apiConfiguration.apiEndPoints.queryVerificatorEndpoint,body,{'headers':headers});
  }
  sendRequest(request: RequestModel){
    const body = JSON.stringify(request);
    const headers = { 'content-type': 'application/json'};
    return this.http.post(environment.apiConfiguration.apiBaseURI+environment.apiConfiguration.apiEndPoints.requestEndpoint,body,{'headers':headers});
  }
}
