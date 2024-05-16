import { SaveRequestFolioModel } from "./save-request-folio.model";

export class saveRequestsModel{
    user: string;
    requests: SaveRequestFolioModel[];

    constructor(requests: SaveRequestFolioModel[], user="evesga"){
        this.user = user;
        this.requests = requests;
    }
}