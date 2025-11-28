import { Routes } from '@angular/router';
import { Login } from './pages/login/login';
import { Dashboard } from './pages/dashboard/dashboard';
import { ExerciseCreate } from './pages/exercise-create/exercise-create';
import { ExerciseRun } from './pages/exercise-run/exercise-run';

export const routes: Routes = [
    { path: 'login', component: Login },
    { path: 'dashboard', component: Dashboard },
    { path: 'exercise-create', component: ExerciseCreate }, 
    { path: 'exercise-run/:id', component: ExerciseRun },
    { path: '', redirectTo: '/exercise-create', pathMatch: 'full' }
];
