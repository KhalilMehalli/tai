# Tai - Educational Coding Platform Frontend

An Angular 20 frontend application for an educational coding exercise platform. It enables "teachers" to create coding exercises and "students" to solve them with integrated code editing, testing, and progressive hints. User configuration is not implemented, every user can create, perform, and update exercises.


## Features

### For "Teachers"
- Create and edit coding exercises with multiple files
- Define test cases with expected outputs
- Add progressive hints that unlock after failed attempts
- Real-time code compilation and test verification
- Support for C, Java, and Python languages

### For "Students"
- Execute code against predefined test cases
- View detailed test results and error messages

## Technology Stack

| Technology | Version |
|------------|---------|
| Angular | 20.3.0 |
| TypeScript | 5.9.2 | 
| TailwindCSS | 4.1.16 |


## Installation-Start

I recommend using the docker-compose file located at the root of this repository to build the project. However, if you want to start only the frontend:
```bash
npm install
npm start
```

If you run only the frontend, don't forget to also start the backend.


## Docker

### Build and run Docker Image

```bash
docker build -t tai-frontend .

docker run -p 4200:80 tai-frontend
```


## Project Architecture

```
src/app/
├── pages/                          # Route-level container components
│   ├── dashboard/                  # Unit listing and creation
│   ├── unit-info/                  # Unit overview with courses
│   ├── exercise-run/               # Student exercise execution
│   └── exercise-create/            # Teacher exercise creation/editing
│
├── components/                     # Reusable UI components
│   ├── editor/                     # Code editor 
│   ├── console/                    # Output display
│   ├── tests/                      # Test creation (teacher)
│   ├── testsDisplay/               # Test results (student)
│   ├── hints/                      # Hint creation (teacher)
│   ├── hintsDisplay/               # Progressive hint display (student)
│   ├── side-bar/                   # Exercise navigation
│   └── course-display/             # Course listing
│
├── services/    
│   ├── exerciceTeacherService/     # Teacher API operations
│   ├── exerciseStudentService/     # Student API operations
│   ├── navigationInformation/      # Navigation state with caching
│   └── unitUpdateService/          # CUD (Create Update Delete) for units/courses
│
├── models/
│   ├── exercise.models.ts          # Core data models
│   └── main-templates.ts           # Main code templates per language
│
└── utils/                          # Shared utility functions
    └── utils.ts   

```
