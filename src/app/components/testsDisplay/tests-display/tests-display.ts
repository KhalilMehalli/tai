import { Component, Input } from '@angular/core';
import type { TestDisplay } from '../../../models/exercise.models';

@Component({
  selector: 'app-tests-display',
  imports: [],
  templateUrl: './tests-display.html',
  styleUrl: './tests-display.css',
})
export class TestsDisplay {

  @Input() tests: TestDisplay[] = [];
}
