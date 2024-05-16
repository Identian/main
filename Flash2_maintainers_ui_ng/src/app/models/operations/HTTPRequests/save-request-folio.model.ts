export class SaveRequestFolioModel{
    folio: number;
    trading_system: string;
    causal_id: number;

    constructor(folio: number, trading_system: string, causal_id: number){
        this.folio = folio;
        this.trading_system = trading_system;
        this.causal_id= causal_id;
    }
}