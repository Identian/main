export class GeneralParamModel {
    parameter_name: string;
    parameter_value: string;
    rfl_process: string;
    description: string;

    constructor(
        parameter_name: string,
        parameter_value: string,
        rfl_process: string,
        description: string
    ) {
        this.parameter_name = parameter_name
        this.parameter_value = parameter_value
        this.rfl_process = rfl_process
        this.description = description
    }
}