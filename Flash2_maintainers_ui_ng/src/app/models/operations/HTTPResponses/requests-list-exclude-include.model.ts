import { RequestExcludeIncludeModel } from "./request-exclude-include.model";

export class RequestListExcludeIncludeModel {
  user: string;
  requests: RequestExcludeIncludeModel[];
  decision: string;

  constructor(user: string, requests: RequestExcludeIncludeModel[], decision: string) {
    this.user = user
    this.requests = requests
    this.decision = decision
  }
}