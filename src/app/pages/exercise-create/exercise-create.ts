import { Component, Input, numberAttribute, SimpleChanges } from '@angular/core';
import { Router } from '@angular/router';
import { Editor } from '../../components/editor/editor';
import { Tests } from '../../components/tests/tests';
import { Hints } from '../../components/hints/hints';
import { File, Hint, Test, Exercise, EditorConfig, TEACHER_CONFIG, CodePayload, ExerciseFull } from '../../models/exercise.models';
import { Console } from '../../components/console/console';
import { FormsModule } from '@angular/forms';
import { ExerciceTeacherService } from '../../services/exerciceTeacherService/exercice-teacher-service';
import { NaviagtionInfomration } from '../../services/navigationInformation/naviagtion-infomration';

@Component({
  selector: 'app-exercise-create',
  imports: [
    Editor,
    Tests,
    Hints,
    Console,
    FormsModule
  ],
  templateUrl: './exercise-create.html',
  styleUrl: './exercise-create.css',
})

export class ExerciseCreate{
  @Input({ transform: numberAttribute }) unitId!: number;
  @Input({ transform: numberAttribute }) courseId!: number;
  @Input({ transform: numberAttribute }) exerciseId?: number; // Optional - present in edit mode

  // The options the editor has (Teacher = all options)
  options: EditorConfig = TEACHER_CONFIG;


  hints: Hint[] = [];

  files: File[] = [];
  editorInputFiles: File[] = []; 

  tests: Test[] = [];
  consoleText = '';

  title: string = "";
  description: string = "";

  language: string = "c";
  visibility: string = "private";
  difficulty: number = 1;

  position: number = 0;

  // Edit mode state
  isEditMode = false;
  isLoading = false;

  constructor(private exerciceTeacherService: ExerciceTeacherService,
              private navigationInformation: NaviagtionInfomration,
              private router: Router
  ) {}

  ngOnChanges(changes: SimpleChanges): void {
    // Check if exerciseId changed and is defined (edit mode)
    if (changes['exerciseId'] && this.exerciseId) {
      this.isEditMode = true;
      this.loadExerciseForEdit();
    } else if (!this.exerciseId) {
      this.isEditMode = false;
    }
  }

  private loadExerciseForEdit(): void {
    if (!this.exerciseId) return;

    this.isLoading = true;
    this.onConsoleMessage('Chargement de l\'exercice...');

    this.exerciceTeacherService.getExerciseForEdit(this.exerciseId).subscribe({
      next: (exercise) => {
        // Populate form with exercise data
        this.title = exercise.name;
        this.description = exercise.description;
        this.language = exercise.language;
        this.visibility = exercise.visibility;
        this.difficulty = exercise.difficulty;
        this.position = exercise.position;

        // Set files, tests, hints
        this.files = exercise.files;
        this.editorInputFiles = exercise.files;
        this.tests = exercise.tests;
        this.hints = exercise.hints;

        this.isLoading = false;
        this.onConsoleMessage(`Exercice charge avec succes. `);
        console.log(exercise.files);
      },
      error: (err) => {
        this.isLoading = false;
        this.onConsoleMessage(`Erreur lors du chargement: ${err.message ?? err}`);
      }
    });
  }

  onFilesChange(files: File[]) : void {
    this.files = files;
    console.log(files);
  }

  onTestsChange(tests: Test[]) : void{
    this.tests = tests;
    console.log(tests);
  }

  onHintsChange(hints: Hint[]) : void {
    this.hints = hints;
    console.log(hints);
  }

  onConsoleMessage(msg: String) : void {
    const line = String(msg);
    this.consoleText = this.consoleText
      ? this.consoleText + '\n>' + line
      : '>' + line;
  }

  onCompileRequest(): void {
    const payload : CodePayload = {
      files: this.files,
      language: this.language
    };

    this.onConsoleMessage('Compilation en cours...');
    this.onConsoleMessage(JSON.stringify(payload));

    this.exerciceTeacherService.compile(payload).subscribe({
      next: (res) => {
        this.onConsoleMessage( JSON.stringify(res, null, 2));
      },
      error: (err) => {
        this.onConsoleMessage(`Erreur : ${err.message ?? err}`);
      },
    });
  }

  onRunTest(test: Test): void {
    const payload = {
      files: this.files,
      language: this.language,
      argv: test.argv,
    };

    this.onConsoleMessage(`Lancement du test avec argv="${test.argv}"...`);

    this.exerciceTeacherService.runTest(payload).subscribe({
      next: res => {
        this.onConsoleMessage(JSON.stringify(res, null, 2));
        if(res.status)
          test.expected_output = res.data.stdout?.trim() ?? test.expected_output;
        else
          test.expected_output = "error";
      },
      error: err => {
        this.onConsoleMessage(`Erreur : ${err.message ?? err}`);
      },
    });
  }

  onSubmitExercise(): void {
    if (!this.title.trim()) {
      this.onConsoleMessage('Le titre est obligatoire.');
      return;
    }

    if (!this.description.trim()) {
      this.onConsoleMessage('La description est obligatoire.');
      return;
    }

    if (this.files.length === 0) {
      this.onConsoleMessage('Vous devez definir au moins un fichier.');
      return;
    }

    if (this.isEditMode && this.exerciseId) {
      this.updateExercise();
    } else {
      this.createExercise();
    }
  }

  private createExercise(): void {
    const payload: Exercise = {
      course_id: this.courseId,
      name: this.title.trim(),
      description: this.description.trim(),
      visibility: this.visibility,
      language: this.language,
      difficulty: this.difficulty,
      position: this.position,
      files: this.files,
      tests: this.tests,
      hints: this.hints,
    };

    this.onConsoleMessage(JSON.stringify(payload));
    this.onConsoleMessage('Envoi de l\'exercice au serveur...');

    this.exerciceTeacherService.createExercise(payload).subscribe({
      next: (res) => {
        this.onConsoleMessage(
          'Exercice cree avec succes !\n' + JSON.stringify(res, null, 2),
        );

        this.navigationInformation.clearUnitCache();
        setTimeout(() => {
          this.router.navigate(['/unit', this.unitId]);
        }, 2000);
      },
      error: (err) => {
        this.onConsoleMessage(err.error?.detail ?? 'Erreur lors de la creation');
      },
    });
  }

  private updateExercise(): void {
    if (!this.exerciseId) return;

    const payload: ExerciseFull = {
      id : this.exerciseId,
      course_id: this.courseId,
      name: this.title.trim(),
      description: this.description.trim(),
      visibility: this.visibility,
      language: this.language,
      difficulty: this.difficulty,
      position: this.position,
      files: this.files,
      tests: this.tests,
      hints: this.hints,
    };

    this.onConsoleMessage(JSON.stringify(payload));
    this.onConsoleMessage('Mise a jour de l\'exercice...');

    this.exerciceTeacherService.updateExercise(this.exerciseId, payload).subscribe({
      next: (res) => {
        this.onConsoleMessage(
          'Exercice mis a jour avec succes !\n' + JSON.stringify(res, null, 2),
        );

        this.navigationInformation.clearUnitCache();
        setTimeout(() => {
          this.router.navigate(['/unit', this.unitId]);
        }, 2000);
      },
      error: (err) => {
        this.onConsoleMessage( 'Erreur lors de la mise a jour');
        console.log(err);
      },
    });
  }
}
