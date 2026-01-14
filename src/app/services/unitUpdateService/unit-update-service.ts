import { Injectable } from '@angular/core';
import { CourseCreatePayload } from '../../models/exercise.models';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment.development';
import { CourseNav } from '../../models/exercise.models';

@Injectable({
  providedIn: 'root',
})
export class UnitUpdateService {
  
  constructor(private http: HttpClient) { }
  
  createCourse(payload: CourseCreatePayload): Observable<CourseNav> {
    return this.http.post<CourseNav>(`${environment.apiUrl}create-course`, payload);
  }

  deleteCourse(courseId: number): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}course/${courseId}`);
  }

  deleteExercise(exerciseId: number): Observable<void> {
  return this.http.delete<void>(`${environment.apiUrl}exercise/${exerciseId}`);
}
}
