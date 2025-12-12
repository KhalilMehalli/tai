import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestsDisplay } from './tests-display';

describe('TestsDisplay', () => {
  let component: TestsDisplay;
  let fixture: ComponentFixture<TestsDisplay>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TestsDisplay]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TestsDisplay);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
