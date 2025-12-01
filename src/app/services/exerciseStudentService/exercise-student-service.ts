import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import type { Exercise, ApiResponse, File, Test, CodePayload } from '../../models/exercise.models';
import { environment } from '../../../environments/environment.development'; // On importe l'environnement



@Injectable({
  providedIn: 'root',
})
export class ExerciceStudentService {
  private API_STUDENT_EXERCISE = `${environment.apiUrl}student/exercise/`;
  
  constructor(private http: HttpClient) {}

  getExerciseForStudent(ExerciseId: number): Observable<ApiResponse<Exercise>> {
    return this.http.get<ApiResponse<Exercise>>(`${this.API_STUDENT_EXERCISE}${ExerciseId}`);
  }

  sendExerciseStudent(ExerciseId: number, payload: CodePayload): Observable<ApiResponse<any>> {
    return this.http.post<ApiResponse<any>>(`${this.API_STUDENT_EXERCISE}${ExerciseId}/test`, payload);
  }

}
