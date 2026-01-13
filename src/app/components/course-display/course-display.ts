import { Component, Input } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CourseNav } from '../../models/exercise.models';

@Component({
  selector: 'app-course-display',
  imports: [RouterLink],
  templateUrl: './course-display.html',
  styleUrl: './course-display.css',
})
export class CourseDisplay {
  @Input() courses: CourseNav[] = [];
  @Input() unitId!: number;
}
