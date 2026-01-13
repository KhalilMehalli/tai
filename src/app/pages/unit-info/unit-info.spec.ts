import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UnitInfo } from './unit-info';

describe('UnitInfo', () => {
  let component: UnitInfo;
  let fixture: ComponentFixture<UnitInfo>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UnitInfo]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UnitInfo);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
