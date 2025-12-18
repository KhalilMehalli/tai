import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import type { Exercise, ApiResponse, File, Test, CodePayload, TestRespond } from '../../models/exercise.models';
import { environment } from '../../../environments/environment.development'; // On importe l'environnement



@Injectable({
  providedIn: 'root',
})
export class ExerciceStudentService {
  
  constructor(private http: HttpClient) {}

  getExerciseForStudent(UnitId: number, CourseId: number, ExerciseId: number): Observable<ApiResponse<Exercise>> {
    return this.http.get<ApiResponse<Exercise>>(`${environment.apiUrl}student/unit/${UnitId}/course/${CourseId}/exercise/${ExerciseId}`);
  }

  
  sendExerciseStudent(UnitId: number, CourseId: number, ExerciseId: number, payload: CodePayload): Observable<ApiResponse<any>> {
    return this.http.post<ApiResponse<TestRespond>>(`${environment.apiUrl}student/unit/${UnitId}/course/${CourseId}/exercise/${ExerciseId}`, payload);
  }
    

}
