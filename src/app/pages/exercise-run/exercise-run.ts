import { Component, Input, numberAttribute, SimpleChanges} from '@angular/core';
import { finalize } from 'rxjs/operators'

import { FormsModule } from '@angular/forms';
import { Editor} from '../../components/editor/editor';
import { Console } from '../../components/console/console';
import { TestsDisplay } from '../../components/testsDisplay/tests-display/tests-display';
import { ExerciceStudentService } from '../../services/exerciseStudentService/exercise-student-service';
import { NaviagtionInfomration } from '../../services/navigationInformation/naviagtion-infomration';
import { EditorConfig, STUDENT_CONFIG, Exercise, File, Hint, Test, TestDisplay, StudentSubmissionPayload, RunResponse, TestRespond, UnitNav} from '../../models/exercise.models';
import { HintsDisplay } from '../../components/hintsDisplay/hints-display/hints-display';
import { SideBar } from '../../side-bar/side-bar';

interface TestRespondList {
  test_responses : TestRespond[];
}

@Component({
  selector: 'app-exercise-run',
  imports: [FormsModule, Editor, Console, TestsDisplay, HintsDisplay, SideBar],
  templateUrl: './exercise-run.html',
  styleUrl: './exercise-run.css',
})
export class ExerciseRun {
  // The IDs in the url
  @Input({ transform: numberAttribute }) unitId!: number;
  @Input({ transform: numberAttribute }) courseId!: number;
  @Input({ transform: numberAttribute }) exerciseId!: number;

  // Editor configuration 
  options : EditorConfig = STUDENT_CONFIG;
  consoleText = '';

  exerciseData!: Exercise; 
  files : File[] = [];
  tests: TestDisplay[] = [];  
  hints: Hint[] = [];

  description: string = "";
  language: string = "";
  activeTab: string = 'console';
  attemptsCount = 0;
  isSubmitting = false; // Deseable the submit button after a submit

  //Data for the SideB
  unitNavigation: UnitNav | null = null;

  constructor(private exerciseStudentService: ExerciceStudentService,
              private navigationInformation : NaviagtionInfomration
  ){}

  
  ngOnChanges(changes: SimpleChanges): void {
    
    // Fetch the Exercise Content (Code, Tests, etc.)
    // If exerciseId changed, we must reload the editor content. 
    // Navigation in sidebar
    if (changes['exerciseId'] && this.exerciseId) {
        this.fetchExercise(this.unitId, this.courseId, this.exerciseId);
    }

    // Fetch the Sidebar Navigation (Unit Structure)
    // Only fetch if unitId changed (or on first load).
    if (changes['unitId'] && this.unitId) {
        this.fetchSidebarContent(this.unitId);
    }
  }


  private fetchSidebarContent(unitId: number): void {
      this.navigationInformation.getUnitStructure(unitId).subscribe({
          next: (navData) => {
              this.unitNavigation = navData;
              this.onConsoleMessage(this.unitNavigation.name)
          },
          error: (err) => console.error('Failed to load sidebar navigation', err)
      });
  }

  private fetchExercise(UnitId: number, CourseId: number, ExerciseId: number): void {
    // Remove the old data
    this.resetExerciseState();

    
    this.exerciseStudentService.getExerciseForStudent(UnitId, CourseId, ExerciseId).subscribe({
      next: (res) => {
        this.onConsoleMessage(JSON.stringify(res));
        this.exerciseData = res.data;
        this.files = this.exerciseData.files;
        this.hints = this.exerciseData.hints;
        this.description = this.exerciseData.description;

        this.tests = this.exerciseData.tests.map(t => ({
              id: t.id,
              argv: t.argv,
              expected_output: t.expected_output,
              comment: t.comment,
              actualOutput: undefined, 
              status: 'pending',
              position: t.position
           }));;

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

  onSubmitStudentCode(): void {
      if (this.isSubmitting) return; // Prevent double click
      this.isSubmitting = true;

      const payload: StudentSubmissionPayload = {
        user_id: 1, //Temporary user
        files: this.files,
        language: this.exerciseData.language
      };

      this.attemptsCount++;
      this.onConsoleMessage('Envoi de la soumission en cours...');

      this.exerciseStudentService.sendExerciseStudent(this.unitId, this.courseId, this.exerciseId, payload)
        .pipe(finalize(() => this.isSubmitting = false)) // Reset loading state whatever happens
        .subscribe({
          next: (res) => {
            
            // Failure (Complilation, Format, etc...)
            if (res.status === false) {
              this.handleErrorResponse(res.message, res.data);
              return;
            }

            // Success 
            if (res.status === true) {
              this.handleGradingSuccess(res.data as TestRespondList);
            }
          },
          error: (err) => {
            console.log('HTTP error complet :', err);
            console.log('err.error :', err.error);
            this.onConsoleMessage(err.error.detail);
            this.markAllTestAsFail('Erreur')
          }
        });
  }

private markAllTestAsFail(text :string) : void {
  // Mark all tests as failed visually
  this.tests = this.tests.map(t => ({
    ...t,
    status: 'failure',
    actualOutput: text,
    error_log: undefined
  }));
}
private handleErrorResponse(serverMessage: string, data: any): void {
  this.setActiveTab('console');
  
  // Format error
  if (data.format_error) {
      const cleanMessage = data.format_error; 
      this.onConsoleMessage(`${serverMessage} :\n${cleanMessage}`);
      
      this.markAllTestAsFail('Format Invalide'); 
      return;
  }

  // CCompilation error
  if (data.stderr) {
      const errorMsg = data.stderr;
      const exitCode = data.exit_code;
      this.onConsoleMessage(`${serverMessage} (Code ${exitCode}) :\n${errorMsg}`);

      this.markAllTestAsFail('Erreur Compilation');
      return;
  }

  // Other error 
  this.onConsoleMessage(`Erreur : ${serverMessage}`);
  this.markAllTestAsFail('Erreur');

}


private handleGradingSuccess(data: TestRespondList): void {
    this.setActiveTab('tests');
    this.onConsoleMessage('Correction terminée. Voir l\'onglet Résultats.');

    // Search the testRespond for each test
    this.tests = this.tests.map(existingTest => {
      const result = data.test_responses.find(r => r.id === existingTest.id);

      if (result) {
        let displayOutput = result.actual_output;
        // If the log error is not empty, print it rather than the result
        if (result.error_log && result.error_log.trim() !== '') {
          displayOutput = `Error: ${result.error_log}`;
        }

        return {
          ...existingTest,
          status: result.status,
          actualOutput: displayOutput
        };
      }
      return existingTest;
    });
  }
  
  // Clears all current exercise data.
  private resetExerciseState(): void {
    this.files = [];
    this.tests = [];
    this.hints = [];
    this.description = "";
    this.language = "";
    this.consoleText = ""; 
    this.activeTab = 'console'; 
    this.attemptsCount = 0; 

    this.exerciseData = undefined!; 
  }
}
