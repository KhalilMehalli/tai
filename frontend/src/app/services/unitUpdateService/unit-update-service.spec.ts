import { TestBed } from '@angular/core/testing';

import { UnitUpdateService } from './unit-update-service';

describe('UnitUpdateService', () => {
  let service: UnitUpdateService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(UnitUpdateService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
