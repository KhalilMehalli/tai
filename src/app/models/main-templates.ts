export const CODE_TEMPLATES: Record<string, string> = {
  c: `#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    printf("Hello World!\\n");
    return 0;
}`,

  java: `public class Main {
    public static void main(String[] args) {
        System.out.println("Hello World!");
    }
}`,

  python: `import sys

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()`
};


export const MAIN_FILENAMES: Record<string, string> = {
    c: 'main.c',
    java: 'Main.java', 
    python: 'main.py'
};