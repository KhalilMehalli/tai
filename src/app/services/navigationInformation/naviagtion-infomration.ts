import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { tap } from 'rxjs/operators';
import { UnitSummary, UnitNav} from '../../models/exercise.models';
import { environment } from '../../../environments/environment.development'; // On importe l'environnement

@Injectable({
  providedIn: 'root',
})
export class NaviagtionInfomration {

  // Stores the ID and structure of the last loaded unit to avoid redundant API calls.
  private UnitId: number | null = null;
  private Structure: UnitNav | null = null;
  private DashboardList: UnitSummary[] | null = null;

  constructor(private http: HttpClient) { }

  // Ask for the units a student can do. Use for the dashbord
  getDashboardUnits(): Observable<UnitSummary[]> {
    // Check "cache"
    if (this.DashboardList) {
      return of(this.DashboardList); // of convert the respond to an observable
    }

    // Call backend
    return this.http.get<UnitSummary[]>(`${environment.apiUrl}units?user_id=1`).pipe(
      tap((data) => {
        this.DashboardList = data; // Store in memory
      })
    );
  }


  // Ask for the structure of an unit. Use for the sidebar in an exercise and in page course
  getUnitStructure(unitId: number): Observable<UnitNav> {
    
    // Check "cache"
    // If we have data in memory and it matches the requested ID
    // Good when a student is in the exercise 1 of the course 1 and go to the exercise 2 of the same course
    // No need to call the backend again because the information are the same
    if (this.Structure && this.UnitId === unitId) {
      console.log("Data from cache")
      return of(this.Structure); 
    }

    // Call backend                                                           // Temporary query parameters
    return this.http.get<UnitNav>(`${environment.apiUrl}unit/${unitId}/courses?user_id=1`).pipe(
      // tap intercept the respond of the back before it reaches the component.
      tap((data) => {
        this.UnitId = unitId;
        this.Structure = data;
      })
    );
  }
  clearUnitCache(): void {
    this.UnitId = null;
    this.Structure = null;
  }
  clearAllCache(): void {
    this.UnitId = null;
    this.Structure = null;
    this.DashboardList = null;
  }


}
