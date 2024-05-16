export class RequestModel{
  'request_query': string;
  'database_name': string;
  'number_of_records': number;
  'requester_email':string;
  'approver_email':string;
  'request_description':string;
  'requester_name':string;
  constructor(request_query: string, database_name: string, records_to_affect: number, requester_email:string, approver_email:string, request_description:string, requester_name:string){
    this.approver_email = approver_email;
    this.number_of_records = records_to_affect;
    this.database_name = database_name;
    this.request_query = request_query;
    this.requester_email = requester_email;
    this.request_description = request_description;
    this.requester_name = requester_name;
  }
}
