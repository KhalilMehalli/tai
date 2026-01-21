import { Component, Input, numberAttribute, SimpleChanges} from '@angular/core';
import { NavigationInformationService } from '../../services/navigationInformation/navigation-information-service';
import { UnitNav, UnitUpdatePayload, CourseUpdatePayload, CourseCreatePayload } from '../../models/exercise.models';
import { validateEntityForm } from '../../utils/utils';
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

  errorMessage = '';

  errorMessageUnit = '';

  newCourse = {
    name: '',
    description: '',
    difficulty: 1,
    visibility: 'private'
  };

  // Unit edit state
  isEditingUnit = false;
  isSavingUnit = false;
  editedUnit = {
    name: '',
    description: '',
    difficulty: 1,
    visibility: 'private'
  };

  constructor(private navigationInformation: NavigationInformationService, private unitUpdateService: UnitUpdateService) {}

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

// Submits a new course to the backend after validation under the current unit

  submitCourse() {
    this.errorMessage = '';

    const validationError = validateEntityForm(this.newCourse);
    if (validationError) {
      this.errorMessage = validationError;
      return;
    }

    this.isCreating = true;
    const payload: CourseCreatePayload = { ...this.newCourse, unit_id: this.unitId, author_id: this.author_id };

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

  handleDeleteExercise(payload: { courseId: number, exerciseId: number }) {
    this.unitUpdateService.deleteExercise(payload.exerciseId).subscribe({
      next: () => {
        if (this.unitData) {
          // Find the specific course that contains the deleted exercise
          const courseToUpdate = this.unitData.courses.find(c => c.id === payload.courseId);

          if (courseToUpdate) {
            // Remove the exercise from the list by filtering it out
            courseToUpdate.exercises = courseToUpdate.exercises.filter(e => e.id !== payload.exerciseId);
          }
        }
      },
      error: (err) => {
        console.error("Erreur suppression exercice", err);
        alert("Erreur lors de la suppression de l'exercice.");
      }
    });
  }


  startEditingUnit(): void {
    if (this.unitData) {
      this.errorMessageUnit = "";
      this.editedUnit = {
        name: this.unitData.name,
        description: this.unitData.description,
        difficulty: this.unitData.difficulty,
        visibility: this.unitData.visibility
      };
      this.isEditingUnit = true;
    }
  }

  cancelEditingUnit(): void {
    this.isEditingUnit = false;
    this.errorMessageUnit = "";
  }

  saveUnitChanges(): void {
    if (!this.unitData) return;

    this.errorMessageUnit = '';

    const validationError = validateEntityForm(this.editedUnit);
    if (validationError) {
      this.errorMessageUnit = validationError;
      return;
    }

    this.isSavingUnit = true;
    const payload: UnitUpdatePayload = {
      name: this.editedUnit.name,
      description: this.editedUnit.description,
      difficulty: this.editedUnit.difficulty,
      visibility: this.editedUnit.visibility
    };

    this.unitUpdateService.updateUnit(this.unitData.id, payload).subscribe({
      next: (updated) => {
        if (this.unitData) {
          this.unitData = {
            ...this.unitData,
            name: updated.name,
            description: updated.description,
            difficulty: updated.difficulty,
            visibility: updated.visibility
          };
        }
        this.navigationInformation.clearUnitCache();
        this.isSavingUnit = false;
        this.isEditingUnit = false;
      },
      error: (err) => {
        console.error("Error updating unit", err);
        alert("Erreur lors de la modification du module.");
        this.isSavingUnit = false;
      }
    });
  }


  handleUpdateCourse(event: {courseId: number, payload: CourseUpdatePayload}): void {
    this.unitUpdateService.updateCourse(event.courseId, event.payload).subscribe({
      next: (updatedCourse) => {
        if (this.unitData) {
          const courseIndex = this.unitData.courses.findIndex(c => c.id === event.courseId);
          if (courseIndex !== -1) {
            this.unitData.courses[courseIndex] = {
              ...this.unitData.courses[courseIndex],
              name: updatedCourse.name,
              description: updatedCourse.description,
              difficulty: updatedCourse.difficulty,
              visibility: updatedCourse.visibility
            };
            this.unitData = { ...this.unitData };
          }
        }
        this.navigationInformation.clearUnitCache();
      },
      error: (err) => {
        console.error("Error updating course", err);
        alert("Erreur lors de la modification du cours.");
      }
    });
  }

}