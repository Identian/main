import { CauseExcludeIncludeModel } from "./cause-exclude-include.model";

export class FieldsExcludeIncludeModel{
    'Excluir': CauseExcludeIncludeModel[];
    'Incluir': CauseExcludeIncludeModel[];
    'Cambiar num_control': CauseExcludeIncludeModel[];

    constructor(exclude: CauseExcludeIncludeModel[], include: CauseExcludeIncludeModel[], change_num: CauseExcludeIncludeModel[]){
        this["Excluir"] = exclude;
        this["Cambiar num_control"] = change_num;
        this["Incluir"] = include;
    }
}