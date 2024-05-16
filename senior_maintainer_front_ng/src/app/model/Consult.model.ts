export class ConsultModel{
  'query': string;
  'database': string;

  constructor(query:string="", database:string=""){
    this.query = query;
    this.database = database;
  }
}
