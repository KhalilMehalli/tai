import { Component, Input, SimpleChanges } from '@angular/core';
import type { TestDisplay, Test } from '../../../models/exercise.models';

@Component({
  selector: 'app-tests-display',
  imports: [],
  templateUrl: './tests-display.html',
  styleUrl: './tests-display.css',
})
export class TestsDisplay {

  @Input() testsDisplay: TestDisplay[] = [];

}
