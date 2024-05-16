import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { observable, Observable } from 'rxjs';
import { VerifyFolioModel } from 'src/app/models/operations/HTTPRequests/verify-folio.model';
import { FieldsExcludeIncludeModel } from 'src/app/models/operations/HTTPResponses/fields-exclude-include.model';
import { IncludeExcludeOperationsModel } from 'src/app/models/operations/include-exclude-ops.model';
import { map, filter, tap } from 'rxjs/operators'
import { saveRequestsModel } from 'src/app/models/operations/HTTPRequests/save-request.model';
import { SaveRequestFolioModel } from 'src/app/models/operations/HTTPRequests/save-request-folio.model';
import { RequestExcludeIncludeModel } from 'src/app/models/operations/HTTPResponses/request-exclude-include.model';
import { RequestListExcludeIncludeModel } from 'src/app/models/operations/HTTPResponses/requests-list-exclude-include.model';

@Injectable({
  providedIn: 'root'
})
export class IncludeExcludeOperationsService {

  private baseUrl = "https://lze1e0qlod.execute-api.us-east-1.amazonaws.com/";
  constructor(private http: HttpClient) { }

  getFields(){
    //REST API
    return this.http.get<FieldsExcludeIncludeModel>("https://zgjrlwcpde.execute-api.us-east-1.amazonaws.com/dev/load-fields-include-exclude-operations");
  }

  getRequests(){
    return this.http.get<RequestListExcludeIncludeModel>(this.baseUrl + "load-requests-include-exclude-operations");
  }

  verifyFolio(folio: VerifyFolioModel){
    folio.date = "2022-12-21";
    let body=JSON.stringify(folio);
    let completeUrl = this.baseUrl + "verify-fields-include-exclude-operations?"
                                    +"date="+folio.date
                                    +"&folio="+folio.folio
                                    +"&trading_system="+folio.trading_system
                                    +"&action="+folio.action;
    return this.http.get<boolean>(completeUrl)
  }
  
  saveRequests(requests: IncludeExcludeOperationsModel[]){
    let request_list_to_save: SaveRequestFolioModel[] = [];
    requests.forEach(
      request => {
        request_list_to_save.push(new SaveRequestFolioModel(request.folio, request.trading_system, request.causal_id))
      }
    )
    console.log(request_list_to_save)
    const body = JSON.stringify(new saveRequestsModel(request_list_to_save))
    console.log(body)
    const headers = { 'content-type': 'application/json'}
    return this.http.post(this.baseUrl+"save-include-exclude-operations-requests",body,{'headers':headers});
  }

  proccesRequests(request_list_to_process: RequestListExcludeIncludeModel){
    console.log(request_list_to_process)
    const body = JSON.stringify(request_list_to_process)
    console.log(body)
    const headers = { 'content-type': 'application/json'}
    return this.http.post(this.baseUrl+"process-include-exclude-operations",body,{'headers':headers});
  }

}
