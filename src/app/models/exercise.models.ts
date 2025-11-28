//Type of a hint sent to the backend 
export interface HintCreate { 
  body: string;
  unlock_after_attempts: number;
  position: number;
}

export interface TestCaseCreate {
  argv: string;
  expected_output: string;
  comment: string;
  position: number;
}

export interface FileCreate {
  name: string;
  content: string;
  extension: string;
  is_main: boolean;
  editable: boolean;
  position: number;
}

export interface ExerciseCreatePayload {
  course_id: number;
  name: string;
  description: string;
  visibility: string;
  language: string; 
  difficulty: number;
  position: number;
  
  files: FileCreate[];
  tests: TestCaseCreate[];
  hints: HintCreate[];
}

export interface ApiResponse<T> {
  status: boolean;
  message: string;
  data: T;
}