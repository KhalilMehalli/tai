import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import type { File, Exercise, ApiResponse } from '../../models/exercise.models';
import { environment } from '../../../environments/environment.development'; // On importe l'environnement

export interface CompilePayload {
  files: File[];
  language: string;
}

export interface TestRunPayload {
  files: File[];
  language: string;   
  argv: string;
}

interface RunResponse {
  stdout: string;
  stderr: string;
  exit_code: number;
}


@Injectable({
  providedIn: 'root',
})
export class ExerciceTeacherService {
  private API_COMPILE_URL = `${environment.apiUrl}compilation`;
  private API_TEST_URL = `${environment.apiUrl}run_test`;
  private API_CREATE_EXERCISE_URL = `${environment.apiUrl}exercises`;
  
  constructor(private http: HttpClient) {}

  compile(payload: CompilePayload): Observable<ApiResponse<RunResponse>> {
    return this.http.post<ApiResponse<RunResponse>>(this.API_COMPILE_URL, payload);
  }

  runTest(payload: TestRunPayload): Observable<ApiResponse<RunResponse>> {
    return this.http.post<ApiResponse<RunResponse>>(this.API_TEST_URL, payload);
  }

  createExercise(payload: Exercise): Observable<ApiResponse<RunResponse>> {
  return this.http.post<ApiResponse<RunResponse>>(this.API_CREATE_EXERCISE_URL, payload);
}
}
