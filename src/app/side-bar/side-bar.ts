import { Component, Input } from '@angular/core';
import { UnitNav } from '../models/exercise.models';
import { RouterLink } from '@angular/router';
@Component({
  selector: 'app-side-bar',
  imports: [RouterLink],
  templateUrl: './side-bar.html',
  styleUrl: './side-bar.css',
})
export class SideBar {
  @Input() unit: UnitNav | null = null;
  @Input() currentExerciseId: number | null = null;
}
