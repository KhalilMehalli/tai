import { Component, Input, numberAttribute, OnInit} from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Editor} from '../../components/editor/editor';
import { Console } from '../../components/console/console';
import { TestsDisplay } from '../../components/testsDisplay/tests-display/tests-display';
import { ExerciceStudentService } from '../../services/exerciseStudentService/exercise-student-service';
import { EditorConfig, STUDENT_CONFIG, Exercise, File, Hint, Test, CodePayload, TestDisplay } from '../../models/exercise.models';

@Component({
  selector: 'app-exercise-run',
  imports: [FormsModule, Editor, Console, TestsDisplay],
  templateUrl: './exercise-run.html',
  styleUrl: './exercise-run.css',
})
export class ExerciseRun {
  // The IDs in the url
  @Input({ transform: numberAttribute }) unitId!: number;

  @Input({ transform: numberAttribute }) courseId!: number;

  @Input({ transform: numberAttribute }) exerciseId!: number;

  options : EditorConfig = STUDENT_CONFIG;
  consoleText = '';

  exerciseData!: Exercise; 
  files : File[] = [];
  tests: TestDisplay[] = [];  
  hints: Hint[] = [];

  description: string = "";
  language: string = "";

  activeTab: string = 'tests';

  constructor(private exerciseStudentService: ExerciceStudentService){}

  ngOnInit(){
    this.fetchExercise(this.unitId, this.courseId, this.exerciseId);
  }

   
  private fetchExercise(UnitId: number, CourseId: number, ExerciseId: number): void {
    this.exerciseStudentService.getExerciseForStudent(UnitId, CourseId, ExerciseId).subscribe({
      next: (res) => {
        this.onConsoleMessage(JSON.stringify(res));
        this.exerciseData = res.data;
        this.files = this.exerciseData.files;

        this.tests = this.exerciseData.tests.map(t => ({
              id: t.id,
              argv: t.argv,
              expected_output: t.expected_output,
              comment: t.comment,
              actualOutput: undefined, 
              status: 'pending',
              position: t.position
           }));

        this.hints = this.exerciseData.hints;
        this.description = this.exerciseData.description;
        console.log(this.files[0].id)
        console.log(this.files[1].id)

      },
      error: (err) => {
        console.log('HTTP error complet :', err);
      console.log('err.error :', err.error);
        this.onConsoleMessage(err.error.detail);
      },
    });
  }


  onConsoleMessage(msg: String) : void{ // Add an new ligne of command in the console 
    const line = String(msg);
    this.consoleText = this.consoleText
      ? this.consoleText + '\n>' + line
      : '>' + line;
  }

  onFilesChange(files: File[]) : void {
    this.files = files;
    console.log(files);
  }

  // Change the tab between console, tests and hints tab
  setActiveTab(tab: string) {
    this.activeTab = tab;
  }

  OnStudentSend(): void { // Send the student file to the back 
    const payload : CodePayload = {
      files: this.files,
      language: this.exerciseData.language
    };

    this.onConsoleMessage(JSON.stringify(payload));
    this.exerciseStudentService.sendExerciseStudent(this.exerciseId,payload).subscribe({
      next: (res) => {
        this.onConsoleMessage(JSON.stringify(res));

      },
      error: (err) => {
        this.onConsoleMessage(JSON.stringify(err.error.detail));
      },
    });
  }
}
