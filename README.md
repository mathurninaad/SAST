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
password = "admin123"
os.system("rm -rf /")
query = "SELECT * FROM users WHERE id = 1"
unused_var = 42
```

### Output

```bash
Issue on line: 4 [Dangerous Function]. Function name: os.system
Issue on line: 3 [Unused variable]. variable name: password
Issue on line: 5 [Unused variable]. variable name: query
Issue on line: 6 [Unused variable]. variable name: unused_var
Issue on line: 3 [Possibility of Hardcoded password]. variable Name: password
Issue on line: 5. [Possible SQL injection]
```
