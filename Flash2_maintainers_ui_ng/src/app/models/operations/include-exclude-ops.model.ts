import { CauseExcludeIncludeModel } from "./HTTPResponses/cause-exclude-include.model";

export class IncludeExcludeOperationsModel{
    folio: number;
    trading_system: string;
    action: string;
    cause: string;
    causal_id: number;

    constructor(folio: number, trading_system: string, action: string, cause: string, causal_id:number){
        this.cause = cause;
        this.action = action;
        this.folio =folio;
        this.trading_system = trading_system;
        this.causal_id = causal_id;
    }

}