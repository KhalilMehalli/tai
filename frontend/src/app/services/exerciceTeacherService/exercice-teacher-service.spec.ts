import { TestBed } from '@angular/core/testing';

import { ExerciceTeacherService } from './exercice-teacher-service';

describe('ExerciceTeacherService', () => {
  let service: ExerciceTeacherService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ExerciceTeacherService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
