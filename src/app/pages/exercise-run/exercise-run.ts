import { Component, Input, numberAttribute, OnInit} from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Editor} from '../../components/editor/editor';
import { Console } from '../../components/console/console';
import { ExerciceStudentService } from '../../services/exerciseStudentService/exercise-student-service';
import { EditorConfig, STUDENT_CONFIG, Exercise, File } from '../../models/exercise.models';


@Component({
  selector: 'app-exercise-run',
  imports: [FormsModule, Editor, Console],
  templateUrl: './exercise-run.html',
  styleUrl: './exercise-run.css',
})
export class ExerciseRun {
  // The ID in the url
  @Input({ transform: numberAttribute }) id!: number;

  options : EditorConfig = STUDENT_CONFIG;
  consoleText = '';
  exerciseData!: Exercise; 
  files : File[] = [];


  description: string = "";
  language: string = "";


  constructor(private exerciseStudentService: ExerciceStudentService){}

  ngOnInit(){
    this.fetchExercise(this.id);
  }

  private fetchExercise(id: number): void {
    this.exerciseStudentService.getExerciseForStudent(id).subscribe({
      next: (res) => {
        this.consoleText = JSON.stringify(res);
        this.exerciseData = res.data;
        this.files = this.exerciseData.files;
        console.log(this.exerciseData);
        console.log(this.files);

      },
      error: (err) => {
        this.consoleText = JSON.stringify(err.error.detail);
      },
    });
  }


  onConsoleMessage(msg: String) : void{ // Add an new ligne of command in the console 
    const line = String(msg);
    this.consoleText = this.consoleText
      ? this.consoleText + '\n>' + line
      : '>' + line;
  }
}
