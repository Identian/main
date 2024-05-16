import { ApproveUserField } from "./ApproveUserField.model";
import { DatabaseField } from "./DatabaseField.model";

export class MaintainerFormData{
    'database_list': DatabaseField[];
    'approve_user_list': ApproveUserField[];

    constructor(){
      this.approve_user_list = [];
      this.database_list = [];
    }
}
