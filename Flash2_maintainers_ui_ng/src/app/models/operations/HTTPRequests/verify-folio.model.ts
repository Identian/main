export class VerifyFolioModel{
    folio: string;
    trading_system: string;
    action: string;
    date:string;

    constructor(folio: string, trading_system: string, action: string, date = ""){
        this.folio = folio;
        this.trading_system = trading_system;
        this.action = action;
        this.date = date;
    }
}