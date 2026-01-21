import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment.development'; // On importe l'environnement

@Injectable({
  providedIn: 'root'
})

export class Auth {
  private apiUrl = `${environment.apiUrl}api/auth`;

  constructor(private http: HttpClient) {}

  login(email : string, password : string) : Observable<any>{
    return this.http.post(`${this.apiUrl}/login`, { email, password });
  }
}
