import { Component, Input, numberAttribute } from '@angular/core';
import { Router } from '@angular/router';
import { Editor } from '../../components/editor/editor';
import { Tests } from '../../components/tests/tests';
import { Hints } from '../../components/hints/hints';
import { File, Hint, Test, Exercise, EditorConfig, TEACHER_CONFIG, CodePayload } from '../../models/exercise.models'; 
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

export class ExerciseCreate {
  @Input({ transform: numberAttribute }) unitId!: number;
  @Input({ transform: numberAttribute }) courseId!: number;

  // THe options the editor has (Teacher = all options)
  options: EditorConfig = TEACHER_CONFIG;

  hints: Hint[] = [];
  files: File[] = [];
  tests: Test[] = [];
  consoleText = '';

  title: string = "";
  description: string = "";

  language: string = "c";
  visibility: string = "private";
  difficulty: number = 1;


  position: number = 0;

  constructor(private exerciceTeacherService: ExerciceTeacherService,
              private navigationInformation: NaviagtionInfomration,
              private router: Router
  ) {}

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

  onConsoleMessage(msg: String) : void{ // Add an new ligne of command in the console 
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
        // update the expected_output
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

   onCreateExercise(): void {
    if (!this.title.trim()) {
      this.onConsoleMessage('Le titre est obligatoire.');
      return;
    }

    if (!this.description.trim()) {
      this.onConsoleMessage('La description est obligatoire.');
      return;
    }
    if (this.files.length === 0) {
      this.onConsoleMessage('Vous devez définir au moins deux fichiers (main + ...).');
      return;
    }

    // Payload construct
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

    // Send to the back
    this.onConsoleMessage('Envoi de l’exercice au serveur...');

    this.exerciceTeacherService.createExercise(payload).subscribe({
      next: (res) => {
        this.onConsoleMessage(
          'Exercice créé avec succès !\n' + JSON.stringify(res, null, 2),
        );

        // Clean the unit cache to display correctly the new exercise created
        this.navigationInformation.clearUnitCache();
        setTimeout(() => {
            this.router.navigate(['/unit', this.unitId]);
        }, 2000); // Small delay to allow the user to read the message
      },
      error: (err) => {
        this.onConsoleMessage(err.error.detail);
      },
    });
  }
}
