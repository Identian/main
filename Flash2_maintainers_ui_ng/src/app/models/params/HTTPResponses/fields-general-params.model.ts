export class FieldsGeneralParamModel {
    fields: { [key: string]: string[] }

    constructor(fields: { [key: string]: string[] }) {
        this.fields = fields
    }
}