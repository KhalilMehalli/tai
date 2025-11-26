import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import type { FileCreate, ExerciseCreatePayload } from '../../models/exercise.models';
import { environment } from '../../../environments/environment.development'; // On importe l'environnement

export interface CompilePayload {
  files: FileCreate[];
  language: string;
}

export interface TestRunPayload {
  files: FileCreate[];
  language: string;   
  argv: string;
}

export interface BackEndResponse {
  status: boolean;
  message: string;
  stdout?: string;
  stderr?: string;
  exit_code?: number;
}


@Injectable({
  providedIn: 'root',
})
export class ExerciceTeacherService {
  private API_COMPILE_URL = `${environment.apiUrl}compilation`;
  private API_TEST_URL = `${environment.apiUrl}run_test`;
  private API_CREATE_EXERCISE_URL = `${environment.apiUrl}exercises`;
  
  constructor(private http: HttpClient) {}

  compile(payload: CompilePayload): Observable<BackEndResponse> {
    return this.http.post<BackEndResponse>(this.API_COMPILE_URL, payload);
  }

  runTest(payload: TestRunPayload): Observable<BackEndResponse> {
    return this.http.post<BackEndResponse>(this.API_TEST_URL, payload);
  }

  createExercise(payload: ExerciseCreatePayload): Observable<BackEndResponse> {
  return this.http.post<BackEndResponse>(this.API_CREATE_EXERCISE_URL, payload);
}
}
