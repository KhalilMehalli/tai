import { Injectable } from '@angular/core';
import {
  CourseCreatePayload, CourseNav, UnitSummary,
  UnitCreatePayload, UnitUpdatePayload, CourseUpdatePayload
} from '../../models/exercise.models';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment.development';

@Injectable({
  providedIn: 'root',
})
export class UnitUpdateService {

  constructor(private http: HttpClient) { }

  // Course methods

  createCourse(payload: CourseCreatePayload): Observable<CourseNav> {
    return this.http.post<CourseNav>(`${environment.apiUrl}create-course`, payload);
  }

  deleteCourse(courseId: number): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}course/${courseId}`);
  }

  updateCourse(courseId: number, payload: CourseUpdatePayload): Observable<CourseNav> {
    return this.http.put<CourseNav>(`${environment.apiUrl}course/${courseId}`, payload);
  }

  // Exercise method

  deleteExercise(exerciseId: number): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}exercise/${exerciseId}`);
  }

  // Unit method

  createUnit(payload: UnitCreatePayload): Observable<UnitSummary> {
    return this.http.post<UnitSummary>(`${environment.apiUrl}create-unit`, payload);
  }

  updateUnit(unitId: number, payload: UnitUpdatePayload): Observable<UnitSummary> {
    return this.http.put<UnitSummary>(`${environment.apiUrl}unit/${unitId}`, payload);
  }

  deleteUnit(unitId: number): Observable<void> {
    return this.http.delete<void>(`${environment.apiUrl}unit/${unitId}`);
  }
}
