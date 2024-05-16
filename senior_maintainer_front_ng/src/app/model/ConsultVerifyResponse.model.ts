export class ConsultVerifyResponseModel{
  'rowcount': number;
  'msg_error': string;

  constructor(rowcount:number=0, msg_error:string=""){
    this.rowcount = rowcount;
    this.msg_error = msg_error;
  }
}
