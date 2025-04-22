# Python SAST Detection Tool

Simple yet powerful Static Application Security Testing (SAST) tool built for Python developers. It scans Python code for potential vulnerabilities such as:
  - **Hardcoded passwords**  
  - **Unused variables**  
  - **Dangerous OS function calls** (`os.system`, `eval`, `exec`, etc.)  
  - **Possible SQL injection** strings
---

## Usage

1. Clone or download this repository.

2. Run the script from the command line:

```bash
python main.py [filename].py
(or)
chmod +x main.py
./main.py [filename].py
```
---

## Example
Given the following Python file test.py:

```python
import os
import subprocess
import sqlite3

password123 = "secret"  # hardcoded password
unused_var = 42         # unused variable

conn = sqlite3.connect(":memory:")
cursor = conn.cursor()

def example():
    passwrd = "12345"  # hardcoded password
    user = "admin"
    cursor.execute("SELECT * FROM users WHERE name = '" + user + "'")  # unsafe SQL

    result = subprocess.call("ls -la", shell=True)  # dangerous function
    another_unused = 100  # unused variable
    print("Executed.")

example()
```

### Output

```bash
Issue on line: 14 [Dangerous Function]. Function name: cursor.execute
Issue on line: 16 [Dangerous Function]. Function name: subprocess.call
Issue on line: 5 [Unused variable]. variable name: password123
Issue on line: 6 [Unused variable]. variable name: unused_var
Issue on line: 12 [Unused variable]. variable name: passwrd
Issue on line: 16 [Unused variable]. variable name: result
Issue on line: 17 [Unused variable]. variable name: another_unused
Issue on line: 5 [Possibility of Hardcoded password]. variable Name: password123
Issue on line: 12 [Possibility of Hardcoded password]. variable Name: passwrd
Issue on line: 14. [Unsafe SQL query in 'execute']
```
