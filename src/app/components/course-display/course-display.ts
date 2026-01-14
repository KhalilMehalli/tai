import { Component, Input, Output, EventEmitter } from '@angular/core';
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

  @Output() deleteRequest = new EventEmitter<number>();

  onDeleteClick(courseId: number) {
    // "confirm" function will open a pop up and "ask" a question to the user
    if (confirm('Voulez-vous vraiment supprimer ce cours et tous ses exercices ?')) {
      this.deleteRequest.emit(courseId); 
      console.log("oui")
      return;
    }
  }
}
