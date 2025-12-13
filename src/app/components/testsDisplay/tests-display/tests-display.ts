import { Component, Input, SimpleChanges } from '@angular/core';
import type { TestDisplay, Test } from '../../../models/exercise.models';

@Component({
  selector: 'app-tests-display',
  imports: [],
  templateUrl: './tests-display.html',
  styleUrl: './tests-display.css',
})
export class TestsDisplay {

  @Input() tests: Test[] = [];

  testsDisplay : TestDisplay[] = [];

  ngOnChanges(changes: SimpleChanges): void {
    // When the back will send the tests, this component will convert it from Tests type to TestDisplay
    if (changes['tests'] && this.tests) {
      this.testsDisplay = this.tests.map(t => ({
              id: t.id,
              argv: t.argv,
              expected_output: t.expected_output,
              comment: t.comment,
              actualOutput: undefined, 
              status: 'pending',
              position: t.position
           }));
    }
  }

}
