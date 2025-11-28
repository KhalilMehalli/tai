import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExerciseRun } from './exercise-run';

describe('ExerciseRun', () => {
  let component: ExerciseRun;
  let fixture: ComponentFixture<ExerciseRun>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ExerciseRun]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ExerciseRun);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
