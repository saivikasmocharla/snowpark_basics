# Snowflake Connection Setup Guide

This guide covers the complete setup needed to connect to Snowflake from VS Code using Python and Snowpark.

---

## 1. Install VS Code

1. Download VS Code from:
   https://code.visualstudio.com/
2. Install it on your Windows machine.
3. Open VS Code after installation.

---

## 2. Install Python

1. Download Python from:
   https://www.python.org/downloads/windows/
2. During installation, check the option:
   - Add Python to PATH
3. Finish the installation.
4. Verify Python is available:

```powershell
py --version
```

If it prints a version number, Python is installed correctly.

---

## 3. Open the Project Folder in VS Code

Create a folder such as:

```powershell
D:\Snowpark\snowpark_basics
```

Then open that folder in VS Code:
- File → Open Folder

---

## 4. Install Snowpark

Open the VS Code terminal and run:

```powershell
py -m pip install snowflake-snowpark-python
```

Verify the package is available:

```powershell
py -c "import snowflake.snowpark; print('Snowpark installed successfully')"
```

---

## 5. Create the Snowflake Connection Script

Create a file named `1_Connection_test.py` with the following content:

```python
import os
import snowflake.snowpark.functions
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

connection_parameters = {
    "account": "your_account_name",
    "user": "your_user_name",
    "password": "your_password",
    "role": "ACCOUNTADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "DEMO_DB",
    "schema": "PUBLIC"
}

test_session = Session.builder.configs(connection_parameters).create()

print(test_session.sql("select current_warehouse(), current_database(), current_schema()").collect())

session = Session.builder.configs(connection_parameters).create()
```

Replace the values with your actual Snowflake credentials and account details.

---

## 6. Run the Script

In the VS Code terminal, use:

```powershell
cd "D:\Snowpark\snowpark_basics"
& "C:\Users\HP\AppData\Local\Programs\Python\Python313\python.exe" "D:\Snowpark\snowpark_basics\1_Connection_test.py"
```

If your Python launcher works correctly, this also works:

```powershell
py 1_Connection_test.py
```

---

## 7. Expected Output

If the connection works, the script should print something similar to:

```python
[Row(CURRENT_WAREHOUSE()='COMPUTE_WH', CURRENT_DATABASE()='DEMO_DB', CURRENT_SCHEMA()='PUBLIC')]
```

This confirms that Snowflake connection succeeded and the session is active.

---

## 8. Common Issues and Fixes

### Problem: `ModuleNotFoundError: No module named 'snowflake'`

Fix:

```powershell
py -m pip install snowflake-snowpark-python
```

---

### Problem: `Python was not found`

Use the Python launcher:

```powershell
py --version
```

Then run:

```powershell
py 1_Connection_test.py
```

---

### Problem: Snowflake account is invalid

Check the `account` value in Snowflake.

Typical format:

```python
"account": "xy12345.eu-central-1"
```

or sometimes:

```python
"account": "xy12345"
```

---

### Problem: Wrong username/password

Verify your Snowflake login credentials.

---

### Problem: Warehouse or database not found

Make sure the warehouse, database, and schema exist and that your role has access to them.

---

## 9. Best Practice

Avoid storing credentials directly in code for real projects. Use environment variables instead.

Example:

```python
import os

password = os.getenv("SNOWFLAKE_PASSWORD")
```

---

## 10. Final Checklist

Before you start, make sure all of these are ready:

- VS Code installed
- Python installed
- Project folder created
- Snowpark package installed
- Snowflake account details known
- Role, warehouse, database, and schema confirmed
- Script executed successfully

---

## 11. Summary

The minimum required steps to connect to Snowflake are:

1. Install VS Code
2. Install Python
3. Open the project folder in VS Code
4. Install Snowpark
5. Create the connection script
6. Add valid Snowflake credentials
7. Run the script
8. Confirm the current warehouse, database, and schema are returned

This is the basic working flow for connecting to Snowflake from a local Python environment.
