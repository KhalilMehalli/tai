import { Component, OnInit } from '@angular/core';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { NaviagtionInfomration } from '../../services/navigationInformation/naviagtion-infomration';
import { UnitUpdateService } from '../../services/unitUpdateService/unit-update-service';
import { UnitSummary, UnitCreatePayload } from '../../models/exercise.models';

@Component({
  selector: 'app-dashboard',
  imports: [RouterLink, FormsModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard implements OnInit {
  author_id = 1; // Temporary hardcoded user

  units: UnitSummary[] = [];
  isLoading = false;

  // Unit creation form state
  isAddingUnit = false;
  isCreating = false;
  errorMessage = '';

  newUnit = {
    name: '',
    description: '',
    difficulty: 1,
    visibility: 'private'
  };

  constructor(
    private navigationInformation: NaviagtionInfomration,
    private unitUpdateService: UnitUpdateService
  ) {}

  ngOnInit(): void {
    this.fetchUnits();
  }

  private fetchUnits(): void {
    this.isLoading = true;
    this.navigationInformation.getDashboardUnits().subscribe({
      next: (data) => {
        this.units = data;
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Erreur chargement unités:', err);
        this.isLoading = false;
      }
    });
  }

  startAddingUnit(): void {
    this.newUnit = { name: '', description: '', difficulty: 1, visibility: 'private' };
    this.isAddingUnit = true;
    this.errorMessage = '';
  }

  cancelAdding(): void {
    this.isAddingUnit = false;
    this.errorMessage = '';
  }

  submitUnit(): void {
    this.errorMessage = '';

    if (!this.newUnit.name || this.newUnit.name.trim() === '') {
      this.errorMessage = "Le nom du module est obligatoire.";
      return;
    }

    if (!this.newUnit.description || this.newUnit.description.trim() === '') {
      this.errorMessage = "La description ne peut pas etre vide.";
      return;
    }

    if (this.newUnit.difficulty < 1 || this.newUnit.difficulty > 5) {
      this.errorMessage = "Le niveau de difficulte doit etre entre 1 et 5.";
      return;
    }

    this.isCreating = true;

    const payload: UnitCreatePayload = {
      ...this.newUnit,
      author_id: this.author_id
    };

    this.unitUpdateService.createUnit(payload).subscribe({
      next: (unit) => {
        this.units = [...this.units, unit];
        this.navigationInformation.clearAllCache();
        this.isCreating = false;
        this.isAddingUnit = false;
      },
      error: (err) => {
        console.error(err);
        this.errorMessage = "Erreur lors de la creation du module.";
        this.isCreating = false;
      }
    });
  }

  handleDeleteUnit(unitId: number): void {
    if (confirm('Voulez-vous vraiment supprimer ce module et tous ses cours ?')) {
      this.unitUpdateService.deleteUnit(unitId).subscribe({
        next: () => {
          this.units = this.units.filter(u => u.id !== unitId);
          this.navigationInformation.clearAllCache();
        },
        error: (err) => {
          console.error("Cannot delete unit", err);
          alert("Erreur lors de la suppression du module.");
        }
      });
    }
  }
}
