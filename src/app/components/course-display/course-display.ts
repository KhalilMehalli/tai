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

  @Output() deleteCourseRequest = new EventEmitter<number>();
  @Output() deleteExerciseRequest = new EventEmitter<{courseId: number, exerciseId: number}>();

  onDeleteClick(courseId: number) {
    // "confirm" function will open a pop up and "ask" a question to the user
    if (confirm('Voulez-vous vraiment supprimer ce cours et tous ses exercices ?')) {
      this.deleteCourseRequest.emit(courseId); 
      console.log("oui")
      return;
    }
  }

  onDeleteExerciseClick(courseId: number, exerciseId: number, event: Event) {
    // IMPORTANT : Empêche le clic de "remonter" vers la balise <a> et de changer de page
    event.preventDefault();
    event.stopPropagation();

    if (confirm('Voulez-vous vraiment supprimer cet exercice ?')) {
      this.deleteExerciseRequest.emit({ courseId, exerciseId });
    }
  }
}
