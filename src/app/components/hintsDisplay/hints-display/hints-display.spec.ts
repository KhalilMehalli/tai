import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HintsDisplay } from './hints-display';

describe('HintsDisplay', () => {
  let component: HintsDisplay;
  let fixture: ComponentFixture<HintsDisplay>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HintsDisplay]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HintsDisplay);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
