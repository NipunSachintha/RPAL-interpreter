# RPAL Interpreter

## Overview

This project is a Python-based interpreter for the **Right-reference Pedagogic Algorithmic Language (RPAL)**. It is built to process RPAL source code in four main stages:

### 💡 Key Components

- 🔤 **Lexical Analyzer**: Converts RPAL source code into a sequence of tokens (keywords, identifiers, literals, etc.).
- 🌳 **Parser**: Builds an **Abstract Syntax Tree (AST)** from the token stream, representing the program's structure.
- 🔁 **Standardizer**: Transforms the AST into a **Standardized AST (SAST)** format to ease execution.
- ⚙️ **CSE Machine**: Executes the standardized tree using a **Control Stack Environment (CSE)** model to simulate runtime behavior.

---

## 🔧 How to Use

### ✅ Using the `Makefile`

You can run and manage the project easily via `make` commands.

#### Printing Final Output
To run the RPAL program and print the final output, use the run target. You need to specify the path to the input file using the file variable
```
make run file=path/to/your/input.txt
```
Example:
```
make run file=inputs/t1.txt
```

#### Printing  Abstract Syntax Tree(AST)
To print the Abstract Syntax Tree (AST) with the output, use the ast target.
```
make ast file=path/to/your/input.txt
```

#### Printing Standardized Abstract Syntax Tree(SAST)
To print the standardized Abstract Syntax Tree (ST) with the output, use the st target.
```
make st file=path/to/your/input.txt
```


### 🐍 Run with Python Directly

You can also use `python` directly to execute the interpreter or inspect intermediate outputs.

You can also run the scripts directly using the python command with the appropriate switches.

#### Printing Final Output
```
python myrpal.py path/to/your/input.txt
```

#### Printing Abstract Syntax Tree(AST)
```
python myrpal.py -ast path/to/your/input.txt 
```

#### Printing Standardized Abstract Syntax Tree(SAST)
```
python myrpal.py -st path/to/your/input.txt 
```


## Cleaning Up
To remove all `__pycache__` directories and Python cache files in your repository, you can use the `make clean` command.



---

## 📁 Project Structure

| File/Folder       | Description                                       |
|------------------|---------------------------------------------------|
| `myrpal.py`       | Main driver for RPAL interpretation               |
| `lexer.py`        | Lexical analysis logic                            |
| `parser.py`       | AST construction from token stream                |
| `standardizer.py` | AST to ST transformation logic                  |
| `cse_machine.py`  | Execution engine for evaluating SAST              |
| `Makefile`        | Automates running and cleaning tasks              |

---

