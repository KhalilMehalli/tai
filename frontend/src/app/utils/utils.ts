
 //Validates that a required string field is not empty.
 //Error message if invalid, null if valid
export function validateRequiredString(value: string | undefined, fieldName: string): string | null {
  if (!value || value.trim() === '') {
    return `${fieldName} est obligatoire.`;
  }
  return null;
}

export function validateDifficulty(difficulty: number): string | null {
  if (difficulty < 1 || difficulty > 5) {
    return 'Le niveau de difficulte doit etre entre 1 et 5.';
  }
  return null;
}

//Error message if invalid, null if valid
export function validateEntityForm(entity: {
  name?: string;
  description?: string;
  difficulty?: number;
}): string | null {
  const nameError = validateRequiredString(entity.name, 'Le nom');
  if (nameError) return nameError;

  const descError = validateRequiredString(entity.description, 'La description');
  if (descError) return descError;

  if (entity.difficulty !== undefined) {
    const diffError = validateDifficulty(entity.difficulty);
    if (diffError) return diffError;
  }

  return null;
}


// Appends a new line to the console text with proper formatting.
export function appendConsoleMessage(currentText: string, message: string): string {
  const line = String(message);
  return currentText ? `${currentText}\n>${line}` : `>${line}`;
}



