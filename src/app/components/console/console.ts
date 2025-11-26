import { Component, Input  } from '@angular/core';

@Component({
  selector: 'app-console',
  imports: [],
  templateUrl: './console.html',
  styleUrl: './console.css',
})
export class Console {
  @Input() text: string = "";
}
