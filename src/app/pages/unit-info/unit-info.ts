import { Component, Input, numberAttribute, SimpleChanges} from '@angular/core';
import { NaviagtionInfomration } from '../../services/navigationInformation/naviagtion-infomration';
import { UnitNav, } from '../../models/exercise.models';
import { CourseDisplay } from '../../components/course-display/course-display';
import { UnitUpdateService } from '../../services/unitUpdateService/unit-update-service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-unit-info',
  imports: [CourseDisplay, FormsModule],
  templateUrl: './unit-info.html',
  styleUrl: './unit-info.css',
})
export class UnitInfo {
  @Input({ transform: numberAttribute }) unitId!: number;

  author_id = 1;

  unitData: UnitNav | undefined; 
  isLoading = false;

  // Variables for the creation of a new course 
  isAddingCourse = false; // Show or not the temporary form
  isCreating = false;

  errorMessage: string = '';

  newCourse = {
    name: '',
    description: '',
    difficulty: 1,
    visibility: 'private'
  };
  constructor (private navigationInformation: NaviagtionInfomration, private unitUpdateService : UnitUpdateService) {}

  ngOnChanges(changes: SimpleChanges): void {
      if (this.unitId) {
        this.fetchCourseData();
      }
    }

  private fetchCourseData(): void {
    this.isLoading = true;
    this.navigationInformation.getUnitStructure(this.unitId).subscribe({
      next: (data) => {
        this.unitData = data;
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Erreur chargement unité:', err);
        this.isLoading = false;
      }
    });
  }

  startAddingCourse() {
    this.newCourse = { name: '', description: '', difficulty: 1, visibility: 'private' };
    this.isAddingCourse = true;
  }

  cancelAdding() {
    this.isAddingCourse = false;
    this.errorMessage = '';
  }

  submitCourse() {
    this.errorMessage = '';

    if (!this.newCourse.name || this.newCourse.name.trim() === '') {
        this.errorMessage = "Le nom du cours est obligatoire.";
        console.log("Pas de nom")
        return; 
    }

    if (!this.newCourse.description || this.newCourse.description.trim() === '') {
        this.errorMessage = "La description ne peut pas être vide.";
        return;
    }

    if (this.newCourse.difficulty < 1 || this.newCourse.difficulty > 5) {
        this.errorMessage = "Le niveau de difficulté doit être entre 1 et 5.";
        return;
    }
    this.isCreating = true;

    const payload = { ...this.newCourse, unit_id: this.unitId, author_id : this.author_id};
    console.log(payload);

    this.unitUpdateService.createCourse(payload).subscribe({
        next: (course) => {
            if (this.unitData) {
              // Complete recreation of this variable to force Angular to update the UI
                this.unitData = {
                    ...this.unitData,
                    courses: [...this.unitData.courses, course]
                };
            }
            this.isCreating = false;
            this.isAddingCourse = false; 
        },
        error: (err) => {
            console.error(err);
            this.errorMessage = "Erreur lors de la création du cours."; 
            this.isCreating = false;
        }
    });
  }

  handleDeleteCourse(courseId: number) {
    this.unitUpdateService.deleteCourse(courseId).subscribe({
      next: () => {
        if (this.unitData) {
            // Complete reccreation of the list of courses without the course the user delete
            this.unitData = {
                ...this.unitData,
                courses: this.unitData.courses.filter(c => c.id !== courseId)
            };
        }
      },
      error: (err) => {
        console.error("Impossible de supprimer", err);
        alert("Erreur lors de la suppression du cours.");
      }
    });
  }

}