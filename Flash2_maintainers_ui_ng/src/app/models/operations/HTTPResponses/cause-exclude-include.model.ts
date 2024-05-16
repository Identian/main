export class CauseExcludeIncludeModel{
    causal_id: number;
    causal: string;

    constructor(causal_id:number, causal:string){
        this.causal = causal;
        this.causal_id = causal_id;
    }
}