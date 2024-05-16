import { TestBed } from '@angular/core/testing';

import { BetasParamsService } from './betas-params.service';

describe('BetasParamsService', () => {
  let service: BetasParamsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BetasParamsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
