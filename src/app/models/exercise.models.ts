//Type of a hint sent to the backend 
export interface Hint{
  id ?: number; 
  body: string;
  unlock_after_attempts: number;
  position: number;
}

export interface HintDisplay extends Hint {
  isRevealed: boolean; 
}

export interface Test {
  id ?: number;
  argv: string;
  expected_output: string;
  comment: string;
  position: number;
}

export interface TestDisplay extends Test {
  actualOutput?: string;  // Student output
  status: 'pending' | 'success' | 'failure'; 
} 

export interface File {
  id ?: number;
  name: string;
  content: string;
  extension: string;
  is_main: boolean;
  editable: boolean;
  position: number;
}

export interface Exercise {
  course_id: number;
  name: string;
  description: string;
  visibility: string;
  language: string; 
  difficulty: number;
  position: number;
  
  files: File[];
  tests: Test[];
  hints: Hint[];
}
//

export interface CodePayload {
  files: File[];
  language: string;
}

export interface TestRunPayload extends CodePayload{
  argv: string;
}


// Respond from the back

export interface ApiResponse<T> {
  status: boolean;
  message: string;
  data: T;
}

export interface RunResponse {
  stdout: string;
  stderr: string;
  exit_code: number;
}


// EDITOR CONFIGURATION 

export interface EditorConfig {
  canAddFiles: boolean;
  canDeleteFiles: boolean;
  canRenameFiles: boolean;
  canCompile: boolean;
  canTest: boolean; // Button "Test" to test the user code with the exercise test (written by the teacher)
  canEditStructure: boolean; // Allow to change main and editable for a file
  respectEditableFlag: boolean; // If true, files that are readonly will be in the editor
}

export const STUDENT_CONFIG: EditorConfig = {
  canAddFiles: false,
  canDeleteFiles: false,
  canRenameFiles: false,
  canCompile: false,
  canTest: true,
  canEditStructure: false,
  respectEditableFlag: true
};

export const TEACHER_CONFIG: EditorConfig = {
  canAddFiles: true,
  canDeleteFiles: true,
  canRenameFiles: true,
  canCompile: true,
  canTest: false,
  canEditStructure: true,
  respectEditableFlag: false
};


/*
     this.addFile(mainName, true, `#include <stdio.h>
#include <stdlib.h>
#include "fonction.h"

int main(char argc, char ** argv) {
    int a = atoi(argv[1]);
    int b = atoi(argv[2]);
    int c = addition(a, b);
    printf("%d", c);
    return 0;
}`);
      this.addFile("fonction.c", false, `#include <stdio.h>
#include "fonction.h"

int addition(int a, int b){
// <complete id=1>
   return a + b;
// </complete>
}
`);
      this.addFile("fonction.h", false, `#ifndef FONCTION_H
#define FONCTION_H

int addition(int a, int b);

#endif`);*/