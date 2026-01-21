import { TestBed } from '@angular/core/testing';

import { NaviagtionInfomration } from './naviagtion-infomration';

describe('NaviagtionInfomration', () => {
  let service: NaviagtionInfomration;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NaviagtionInfomration);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
