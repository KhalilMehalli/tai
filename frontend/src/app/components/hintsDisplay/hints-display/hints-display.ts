import { Component, Input, SimpleChanges } from '@angular/core';
import type { HintDisplay, Hint } from '../../../models/exercise.models';

@Component({
  selector: 'app-hints-display',
  imports: [],
  templateUrl: './hints-display.html',
  styleUrl: './hints-display.css',
})

export class HintsDisplay {

  @Input() hints: Hint[] = [];

  @Input() attemptsCount: number = 0;

  displayHints: HintDisplay[] = [];

  ngOnChanges(changes: SimpleChanges): void {
    // When the back will send the hints, this component will convert it from Tests type to TestDisplay
    if (changes['hints'] && this.hints) {
      this.displayHints = this.hints.map(h => ({
        ...h,
        isRevealed: false // Au début, tout est caché
      }));
    }
  }

  revealHint(hint: HintDisplay) {
    hint.isRevealed = true;
  }

  getRemainingAttempts(unlockAt: number): number {
      return Math.max(0, unlockAt - this.attemptsCount);
    }
}
