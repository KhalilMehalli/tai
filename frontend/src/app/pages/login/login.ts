import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import {Auth} from "../../services/auth/auth"

@Component({
  selector: 'app-login',
  imports: [FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {

  email : string = "";
  password : string = "";
  errorMessage : string = "";

  constructor(private authService: Auth, private router: Router) {}

  onLogin() : void {
    this.authService.login(this.email, this.password).subscribe({

        next: () => {
          this.router.navigate(['/dashboard']);
        },
        error: (err) => {
          this.errorMessage = err.error.message; 
        }
      });
  }

}
