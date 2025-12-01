import { Component, EventEmitter, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import type { Test } from '../../models/exercise.models';

interface TestRow extends Test{
  id: number; 
  validated: boolean;
}

@Component({
  selector: 'app-tests',
  imports: [FormsModule],
  templateUrl: './tests.html',
  styleUrl: './tests.css',
})

export class Tests {
  @Output() testsChange = new EventEmitter<Test[]>()
  @Output() runTest = new EventEmitter<Test>();
  @Output() consoleMessage = new EventEmitter<string>()

  tests: TestRow[] = [];
  private counter = 0;

  addTest() : void {
    this.tests.push({
      id: this.counter++,
      argv: "",
      expected_output: "",
      comment: "",
      position: this.tests.length,
      validated: false
    });
  }

  private deleteTest(test: TestRow): void {
    //Removes the row
    this.tests = this.tests.filter(t => t.id !== test.id);
    // Re calculate the position of the remaining hints
    this.tests.forEach((t, index) => (t.position = index));
    this.emitTests();
  }

  // When we click on the "Valider" or "Supprimer" button
  onValidateOrDelete(test: TestRow): void {
    if (!test.validated) {
      if (test.expected_output.trim() === 'error') {
        return;
      }
      test.validated = true;
      this.emitTests();
    } else {
      this.deleteTest(test);
    }
  }

  // When we click on the "Test" button, send the test to the parent component 
  // we send directly the object test to allow hiim to be directly modify
  onRunClicked(test: TestRow): void {
    this.runTest.emit(test);
  }

  // Send the list of tests conforming to the backend type to the parent component 
  private emitTests(): void {
    const payload: Test[] = this.tests
      .filter(t => t.validated && t.argv.trim() !== '')
      .map((t, index) => ({
        argv: t.argv.trim(),
        expected_output: t.expected_output.trim(),
        comment: t.comment.trim(),
        position: index,
      }));

    this.consoleMessage.emit(JSON.stringify(payload));
    this.testsChange.emit(payload);
  }
}
