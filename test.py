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
