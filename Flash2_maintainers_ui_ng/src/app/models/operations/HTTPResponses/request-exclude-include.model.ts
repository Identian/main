export class RequestExcludeIncludeModel{
    action_request_id: number;
    causal_id: number;
    folio: number;
    trading_system: string;
    exclusion_date: string;
    action: string;
    causal: string;
  constructor(
    action_request_id: number, 
    causal_id: number, 
    folio: number, 
    trading_system: string, 
    exclusion_date: string, 
    action: string,
    causal: string) {
    this.action_request_id = action_request_id;
    this.causal_id = causal_id;
    this.folio = folio;
    this.trading_system = trading_system;
    this.exclusion_date = exclusion_date;
    this.action = action;
    this.causal = causal;
  }
}