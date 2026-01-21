import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import type {
  Exercise, ApiResponse, RunResponse, CodePayload, TestRunPayload,
  ExerciseFull
} from '../../models/exercise.models';
import { environment } from '../../../environments/environment.development';


@Injectable({
  providedIn: 'root',
})
export class ExerciceTeacherService {
  private API_COMPILE_URL = `${environment.apiUrl}compilation`;
  private API_TEST_URL = `${environment.apiUrl}run_test`;
  private API_CREATE_EXERCISE_URL = `${environment.apiUrl}exercises`;

  constructor(private http: HttpClient) {}

  //Exercise create method
  compile(payload: CodePayload): Observable<ApiResponse<RunResponse>> {
    return this.http.post<ApiResponse<RunResponse>>(this.API_COMPILE_URL, payload);
  }

  runTest(payload: TestRunPayload): Observable<ApiResponse<RunResponse>> {
    return this.http.post<ApiResponse<RunResponse>>(this.API_TEST_URL, payload);
  }

  createExercise(payload: Exercise): Observable<ApiResponse<RunResponse>> {
    return this.http.post<ApiResponse<RunResponse>>(this.API_CREATE_EXERCISE_URL, payload);
  }

  //Exercise edit method

  getExerciseForEdit(exerciseId: number): Observable<ExerciseFull> {
    return this.http.get<ExerciseFull>(`${environment.apiUrl}update/exercise/${exerciseId}`);
  }

  updateExercise(exerciseId: number, payload: ExerciseFull): Observable<ApiResponse<{ id: number }>> {
    return this.http.put<ApiResponse<{ id: number }>>(`${environment.apiUrl}exercise/${exerciseId}`, payload);
  }
}
