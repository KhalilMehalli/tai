import { Component, EventEmitter, Output, Input, SimpleChanges} from '@angular/core';
import { FormsModule } from '@angular/forms';
import { File, EditorConfig, TEACHER_CONFIG } from '../../models/exercise.models';

const LANGUAGE_EXTENSIONS: Record<string, string> = {
  c: 'c',
};

@Component({
  selector: 'app-editor',
  imports: [ FormsModule],
  templateUrl: './editor.html',
  styleUrl: './editor.css',
})

export class Editor {
  @Output() filesChange = new EventEmitter<File[]>();
  @Output() compile = new EventEmitter<void>();
  @Output() studentSend = new EventEmitter<void>();
  @Output() consoleMessage = new EventEmitter<string>();


  @Input() language: string = "";
  @Input() inputFiles: File[]  = [];
  @Input() options: EditorConfig = TEACHER_CONFIG;


  files: File[] = [];

  private tempIdCounter = -1;
  activeFileId: number | null = null;

  private getDefaultExtension(): string {
    return LANGUAGE_EXTENSIONS[this.language] ?? 'txt';
  }


  // Similar to a constructor, but runs whenever inputs change
  ngOnChanges(changes: SimpleChanges): void {
    // If the editor receives files, display them
    if (changes['inputFiles'] ) {
      console.log(this.inputFiles);
       this.rebuildFilesFromInput();
    }
    // Only allow the teacher to have an open file when creating a new exercise,
    // as they won't receive initial files but can add new ones.
    if (this.files.length === 0 && this.options.canAddFiles && !changes['inputFiles']) {
       this.addFile("main." + this.getDefaultExtension(), true);
    }
  }

  private rebuildFilesFromInput(): void {
    // Reset the editor (in case for the futurrr)
    this.files = [];

    const newFiles = this.inputFiles.map(file => ({
        ...file,  
        id: file.id ?? this.generateTempId()
      }));

    // Add the files in the list of this editor
    this.files= newFiles;

    this.setActiveFile(this.files[0]);
  }

  // Files created in the editor have a negative ID. 
  // This allows the editor to distinguish between locally created files 
  // and those received from the backend (preserving their IDs).
  private generateTempId(): number {
    return this.tempIdCounter--;
  }

  addFile(newName?: string , isMain = false, content=""): void {
    if (!this.options.canAddFiles) {
      this.consoleMessage.emit(`Ajout de fichier non autorisé :).`);
      return;
    }

    // If newName is null or undefined, used default name else use name
    const nameToUse = newName ?? `file${Math.abs(this.tempIdCounter + 1)}.${this.getDefaultExtension()}`;
    const { name, extension } = this.parseFileName(nameToUse);

    const newFile: File = {
      id : this.generateTempId(),
      name: name,
      content: content,
      extension: extension,     
      is_main: isMain,
      editable: true,
      position: this.files.length
    };

    this.files.push(newFile);
    this.activeFileId = newFile.id!;
    this.emitFiles();
    this.consoleMessage.emit(`Fichier "${newFile.name}" créé.`);
  }

  setActiveFile(file: File): void {
    if (file.id !== undefined) {
      this.activeFileId = file.id;
    }
  }

  get activeFile(): File | undefined {
    return this.files.find(f => f.id === this.activeFileId);
  }

  onContentChange(newContent: string): void {
    // Saves the new content (text) written by the user.
    // Checks if they have the right and if the file is editable.
    if (!this.activeFile) return;

    
    if (this.options.respectEditableFlag && !this.activeFile.editable) {
      this.consoleMessage.emit(`Modification de ce fichier non autorisée.`);
      return;
    }

    this.activeFile.content = newContent;
    this.emitFiles();
  }

  private parseFileName(fullName: string): { name: string; extension: string } {
    // Assumes the input 'fullName' has already been trimmed 
    const lastDot = fullName.lastIndexOf('.');

    // No dot found, dot is at the very beginning or dot is at the very end 
    // return the name with no file extension.
    if (lastDot <= 0 || lastDot === fullName.length - 1) {
      return { name: fullName, extension: '' };
    }

    const name = fullName.slice(0, lastDot); 
    const extension = fullName.slice(lastDot + 1); 

    return { name, extension };
}

  onNameChange(file: File, newName: string): void {
    if (!this.options.canRenameFiles) {
      return;
    }

    const trimmed = newName.trim();
    if (!trimmed) return; // If the name is empty, do nothing

    const { name, extension } = this.parseFileName(trimmed);

    file.name = name;
    file.extension = extension || this.getDefaultExtension();
    this.emitFiles();
  }

  deleteFile(file: File): void {
    if (!this.options.canDeleteFiles) {
      this.consoleMessage.emit(`Suppression de fichier non autorisée.`);
      return;
    }

    if (this.files.length === 1) {
      this.consoleMessage.emit(`Impossible de supprimer le dernier fichier.`);
      return;
    }

    this.files = this.files.filter(f => f.id !== file.id);

    // Re calculate the position of the remaining files
    this.files.forEach((f, index) => (f.position = index));

    if (this.activeFileId === file.id) {
      this.activeFileId = this.files[0]?.id ?? null;
    }

    this.emitFiles();
    this.consoleMessage.emit(`Fichier "${file.name}" supprimé.`);
  }

  // clic on the checkbox Main
  onMainChange(file: File, checked: boolean): void {
    if (!this.options.canEditStructure) {
      this.consoleMessage.emit(`Impossible de designer ce fichier comme main.`);
      return;
    }

    if (checked) {
      // Only one main possible
      this.files.forEach(f => (f.is_main = f.id === file.id));
    } else {
      file.is_main = false;
    }
    this.emitFiles();
  }

  onEditableChange(file: File, checked: boolean): void {
      if (!this.options.canEditStructure) {
      this.consoleMessage.emit(`Impossible de designer ce fichier comme editable.`);
      return;
    }
    file.editable = checked;
    this.emitFiles();
  }

  // Ask the parent composant to send all the file to the backend to compile it
  onCompile(): void {
    if (!this.options.canCompile) {
      this.consoleMessage.emit(`Impossible de compiler.`);
      return;
    }
    this.emitFiles();
    this.compile.emit();

  }

    // Ask the parent composant to send all the file to the backend to run it for the student
  onStudentSend(): void {
    if (!this.options.canTest) {
      this.consoleMessage.emit(`Impossible d'envoyer.`);
      return;
    }
    this.emitFiles();
    this.studentSend.emit();

  }

  private emitFiles(): void {
    // Send the list of files conforming to the backend type to the parent component 
    const payload: File[] = this.files.map((f, index) => ({
      name: f.name,
      content: f.content,
      extension: f.extension,
      is_main: f.is_main,
      editable: f.editable,
      position: index,

      // If the file comes from the backend (ID > 0), keep the ID.
      // If the file was created in the editor (ID < 0), do not send the ID (the DB assign one).
      ...(f.id && f.id > 0 ? { id: f.id } : {})
    }));

    this.consoleMessage.emit(JSON.stringify(payload));
    this.filesChange.emit(payload);
  }
}