import { TestBed } from '@angular/core/testing';

import { ExerciseStudentService } from './exercise-student-service';

describe('ExerciseStudentService', () => {
  let service: ExerciseStudentService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ExerciseStudentService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
