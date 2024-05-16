export class GeneralParamRequestModel {
    parameter_request_id: number;
    parameter_name: string;
    rfl_process: string;
    last_value_parameter: string;
    adjust_value_parameter: string;

    constructor(
        parameter_request_id: number,
        parameter_name: string,
        rfl_process: string,
        last_value_parameter: string,
        adjust_value_parameter: string
    ) {
        this.parameter_request_id = parameter_request_id
        this.parameter_name = parameter_name
        this.rfl_process = rfl_process
        this.last_value_parameter = last_value_parameter
        this.adjust_value_parameter = adjust_value_parameter
    }
}