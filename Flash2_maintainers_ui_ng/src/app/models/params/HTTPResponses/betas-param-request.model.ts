export class BetasParamRequestModel {
    parameter_beta_request_id: number
    cc_curve: string
    model_param: string
    param_restriction: string
    last_restriction_value: number
    Adjust_value_parameter: number
    date_request_parameter_beta: string

    constructor(
        parameter_beta_request_id: number,
        cc_curve: string,
        param_restriction: string,
        last_restriction_value: number,
        Adjust_value_parameter: number,
        date_request_parameter_beta: string,
        model_param: string
    ) {
        this.parameter_beta_request_id = parameter_beta_request_id
        this.cc_curve = cc_curve
        this.param_restriction = param_restriction
        this.last_restriction_value = last_restriction_value
        this.Adjust_value_parameter = Adjust_value_parameter
        this.date_request_parameter_beta = date_request_parameter_beta
        this.model_param = model_param
    }
}