import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import type { Exercise, ApiResponse } from '../../models/exercise.models';
import { environment } from '../../../environments/environment.development'; // On importe l'environnement


@Injectable({
  providedIn: 'root',
})
export class ExerciceStudentService {
  private API_GET_EXERCISE = `${environment.apiUrl}exercises/`;
  
  constructor(private http: HttpClient) {}

  getExerciseForStudent(id: number): Observable<ApiResponse<Exercise>> {
    return this.http.get<ApiResponse<Exercise>>(`${this.API_GET_EXERCISE}${id}`);
  }

}
