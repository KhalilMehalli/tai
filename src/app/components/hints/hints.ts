
import { Component, EventEmitter, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';
import type { HintCreate } from '../../models/exercise.models';

interface HintRow extends HintCreate {
  id: number; // For tracking in @for loops
  validated: boolean;
}

@Component({
  selector: 'app-hints',
  imports: [FormsModule],
  templateUrl: './hints.html',
  styleUrl: './hints.css',
})
export class Hints {
  @Output() hintsChange = new EventEmitter<HintCreate[]>();

  hints: HintRow[] = [] ;
  private counter = 0;

  addHint(): void {
    this.hints.push({
      id: this.counter++,
      body: '',
      unlock_after_attempts: 1,
      position: this.hints.length,
      validated: false,
    });
  }

  private deleteHint(hint: HintRow): void {
    //Removes the row
    this.hints = this.hints.filter(h => h.id !== hint.id);
    // Re calculate the position of the remaining hints
    this.hints.forEach((h, index) => (h.position = index));
    this.emitHints();
  }

  // When we click on the "Valider" or "Supprimer" button
  onValidateOrDelete(hint: HintRow): void {
    if (!hint.validated) {

      // Security, the body need to be fill and the number of attempts greater than 0
      if (hint.body.trim() === '' || hint.unlock_after_attempts < 1) {
        return; 
    }
      hint.validated = true;
      this.emitHints();
    } else {
      this.deleteHint(hint);
    }
  }

  // Send the list of hints conforming to the backend type to the parent component 
  private emitHints(): void {
    const payload: HintCreate[] = this.hints
      .filter(h => h.validated && h.body.trim() !== '' && h.unlock_after_attempts > 0)
      .map((h, index) => ({
        body: h.body.trim(),
        unlock_after_attempts: h.unlock_after_attempts,
        position: index,
      }));

    this.hintsChange.emit(payload);
  }
}

