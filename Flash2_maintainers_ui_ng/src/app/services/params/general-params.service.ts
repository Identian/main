import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { GeneralParamModel } from 'src/app/models/params/HTTPResponses/general-param.model';

@Injectable({
  providedIn: 'root'
})
export class GeneralParamsService {

  private baseUrl = "https://2n6cv9cnik.execute-api.us-east-1.amazonaws.com/";
  
  constructor(private http: HttpClient) { }
  
  getFields(){
    return this.http.get(this.baseUrl + "load-fields-general-params");
  }
  
  searchParam(process: string, param: string){
    return this.http.get<GeneralParamModel>(this.baseUrl + "/get-general-param"
                                            +"?process="+process
                                            +"&param="+param);
  }

}
