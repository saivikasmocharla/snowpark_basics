# Reading a Snowflake Table with Snowpark: Simple, Complete Notes

These notes explain the Python example in [`6_Read_from_table.py`](./6_Read_from_table.py) from the beginning. They are written so that someone who has never used Snowflake, Snowpark, or Python can follow along.

The example connects Python to Snowflake, reads tables, filters rows, chooses columns, displays results, and drops rows with missing values.

> **Important:** The Python file contains a password directly in its source code. Do not copy or share that password. If it is a real password, change it in Snowflake and store the replacement somewhere secure, such as an environment variable or a secrets manager. Never commit real credentials to Git.

---

## 1. The big picture

Imagine that Snowflake is a large, remote filing cabinet containing tables of data. A table is like a spreadsheet:

- A **column** is a kind of information, such as a customer's name.
- A **row** is one record, such as one customer.
- A **cell** is one value where a row and column meet.

Snowpark is a Python library that lets Python ask Snowflake to work with that data.

The example follows this general path:

1. Import the Snowpark tools that the script needs.
2. Supply connection settings.
3. Open a connection to Snowflake.
4. Read a table into a Snowpark DataFrame.
5. Ask for rows or columns.
6. Display results.

The script does not download an entire table into an ordinary Python list. A Snowpark DataFrame is an object that represents data and the work to do with it. Snowflake does much of the data processing on its own servers.

---

## 2. Words used in this example

### Snowflake

Snowflake is a cloud data platform. It stores data and runs queries using computing resources called warehouses.

### Snowpark

Snowpark is Snowflake's Python library for working with Snowflake data using Python code.

### Session

A **session** is the connection between this Python program and Snowflake. The program uses it to read tables and run SQL.

### DataFrame

A **DataFrame** is an object describing a set of rows and columns. It is not the same as a normal Python list. In this example, `test`, `test2`, `test3`, and `test4` refer to DataFrames at different points.

### SQL

SQL is a language for asking a database to read or change data. The example uses a SQL `SELECT` statement to read rows.

### `NULL` or missing value

`NULL` means that a value is missing or unknown in a database cell. It is not the same thing as the text `"NULL"` or the number `0`.

---

## 3. Imports: bringing tools into the program

At the beginning of the Python file:

```python
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import time

from snowflake.snowpark.types import IntegerType, StringType, StructField, StructType, DateType
```

An **import** makes code from a library available to this file.

### `from snowflake.snowpark import Session`

This imports `Session`, the Snowpark class used to create a connection to Snowflake.

### `from snowflake.snowpark.functions import col`

This imports the `col` function. It lets the code refer to a DataFrame column by name.

For example:

```python
col("C_NATIONKEY")
```

means “refer to the column named `C_NATIONKEY`.”

### `import time`

This imports Python's standard `time` module. It can be used for tasks such as waiting for a number of seconds. This example does not use it.

### The Snowpark type imports

`IntegerType`, `StringType`, `StructField`, `StructType`, and `DateType` are tools for describing data types and table schemas. This example does not use them either.

Unused imports do not perform any useful work in this script. They may be leftovers from another example.

---

## 4. Connection settings

The script defines a dictionary called `connection_parameters`. In the actual Python file, it contains the account, user, password, role, warehouse, database, and schema settings.

A **dictionary** stores information as key-value pairs. For example, a key called `"warehouse"` is paired with the name of a warehouse.

The settings mean:

| Setting | Simple meaning |
| --- | --- |
| `account` | Which Snowflake account to connect to. |
| `user` | Which Snowflake user is connecting. |
| `password` | The user's secret sign-in password. Keep it private. |
| `role` | The Snowflake role used for permissions. A role controls what the user can access or do. |
| `warehouse` | The Snowflake compute resource that runs queries. |
| `database` | The database to use as the default context. |
| `schema` | The schema to use as the default context. A schema is a named group of database objects, such as tables. |

The script's dictionary is only configuration: defining it does not connect to Snowflake yet.

### Keep credentials safe

Putting a real password in a source file is unsafe because the password can be exposed when the file is shared, uploaded, or committed to Git. In a real project, read secrets from a protected environment variable or secrets manager instead. Do not paste the password into notes, examples, screenshots, or chat.

---

## 5. Creating the Snowflake session

```python
session = Session.builder.configs(connection_parameters).create()
```

This line asks Snowpark to create a session using the settings in `connection_parameters`.

Step by step:

1. `Session` is the Snowpark class imported earlier.
2. `Session.builder` starts setting up a new session.
3. `.configs(connection_parameters)` supplies the connection settings.
4. `.create()` attempts to connect and creates the session.
5. `session =` saves the new session in a Python variable named `session`.

If the credentials, network access, account, role, or other settings are wrong, session creation can fail. This line needs a working Snowflake connection to succeed.

---

## 6. Reading and displaying the shared sample table

```python
test = session.table("SNOWFLAKE_SAMPLE_DATA.TPCH_SF1000.CUSTOMER")
test.show()
```

### The table name

The table name has three parts:

```text
database.schema.table
```

For this example:

- Database: `SNOWFLAKE_SAMPLE_DATA`
- Schema: `TPCH_SF1000`
- Table: `CUSTOMER`

This is called a **fully qualified table name** because it identifies the database, schema, and table.

### `session.table(...)`

`session.table(...)` tells Snowpark to refer to the named Snowflake table. The resulting DataFrame is assigned to `test`.

### `test.show()`

`show()` asks Snowflake to produce rows and displays them in the output. It is useful for inspecting a small preview of a table.

This does not mean the whole table has been printed. Large tables may contain far more rows than should be displayed at once.

---

## 7. Reading a table in the user's database

```python
test = session.table("DEMO_DB.PUBLIC.CUSTOMER")
type(test)
t = test.cache_result()
```

### Reading `DEMO_DB.PUBLIC.CUSTOMER`

This reads a different table:

- Database: `DEMO_DB`
- Schema: `PUBLIC`
- Table: `CUSTOMER`

The new DataFrame is again stored in `test`. This replaces the earlier Python value of `test` (the shared sample table). It does **not** delete or change either Snowflake table.

### `type(test)`

Python's `type(...)` function tells you what kind of object a value is. Here, it asks for the type of `test`, which is a Snowpark DataFrame.

In an interactive notebook or Python prompt, the environment may display the result of an expression by itself. In an ordinary `.py` script, this line calculates the type but does not print it. To display it in a script, write:

```python
print(type(test))
```

### `test.cache_result()`

`cache_result()` asks Snowpark to cache the current query result and returns a DataFrame representing that cached result. The returned DataFrame is assigned to `t`.

The original variable `test` is not replaced by this line. Afterward, `test` refers to the original DataFrame, while `t` refers to the cached result.

Caching can be useful when the same result will be reused. It may use Snowflake storage resources, so it is not automatically needed for every query.

---

## 8. Running a SQL query

```python
test = session.sql(
    "select * from SNOWFLAKE_SAMPLE_DATA.TPCH_SF1000.CUSTOMER WHERE C_NATIONKEY='23'"
)
type(test)
test.show()
```

The actual source puts the SQL on one long line. The line break above is only for readability; the SQL is the same.

### `session.sql(...)`

`session.sql(...)` sends a SQL statement through the current Snowpark session and gives back a DataFrame representing its results.

### Understanding the SQL

```sql
select * from SNOWFLAKE_SAMPLE_DATA.TPCH_SF1000.CUSTOMER
where C_NATIONKEY = '23'
```

- `SELECT` means “read data.”
- `*` means “include every column.”
- `FROM` names the table to read.
- `WHERE` limits which rows are returned.
- `C_NATIONKEY` is the column used for the condition.
- `= '23'` asks for rows whose nation key equals `23`.

The result is assigned to `test`, replacing the previous value of `test`. The DataFrame now represents only rows matching the SQL query.

The script again calls `type(test)`. As explained above, an ordinary script will not display that value unless it uses `print(...)`.

Finally, `test.show()` displays some of the query's result rows.

---

## 9. Filtering rows and selecting columns

```python
test3 = test.filter(col("C_NATIONKEY") == "23").select("C_NAME")
type(test3)
test3.show()
```

This builds another DataFrame from `test`.

### `filter(...)`: choose rows

`filter(...)` keeps only rows that satisfy a condition. Here the condition is:

```python
col("C_NATIONKEY") == "23"
```

It refers to the `C_NATIONKEY` column and checks whether its value equals `"23"`.

The SQL query immediately above already filtered `test` to this same nation key. Therefore, this second filter repeats the same restriction. It is redundant for this exact script, although it demonstrates the Snowpark `filter()` method.

### `select(...)`: choose columns

`.select("C_NAME")` keeps only the `C_NAME` column in the resulting DataFrame.

So `test3` contains customer names from the rows that pass the filter. It no longer contains `C_NATIONKEY` or `C_ACCTBAL`.

### Displaying `test3`

`type(test3)` calculates the object's type but does not display it in a normal script. `test3.show()` displays a preview of the result.

---

## 10. A column-selection error in the current example

```python
test4 = test3.select("C_NATIONKEY", "c_acctbal")
test4.show()
type(test4)
```

This section is inconsistent with the earlier code:

1. The earlier `.select("C_NAME")` made `test3` contain only `C_NAME`.
2. This code then asks `test3` for `C_NATIONKEY` and `c_acctbal`.
3. Those columns are not present in `test3`.

As written, selecting those missing columns will cause an error. To keep all three columns, select them when creating `test3`:

```python
test3 = (
    test.filter(col("C_NATIONKEY") == "23")
    .select("C_NAME", "C_NATIONKEY", "C_ACCTBAL")
)

test4 = test3.select("C_NATIONKEY", "C_ACCTBAL")
test4.show()
```

In this corrected example, `test3` contains all three columns, so `test4` can select two of them.

Column names are generally case-insensitive in Snowflake when they are unquoted, but using the same capitalization as the table's column names makes the code easier to read.

---

## 11. Dropping rows that contain missing values

```python
test2 = test.na.drop()
test2.show()
type(test2)
```

### `test.na`

`na` provides DataFrame operations related to missing values.

### `.drop()`

`.drop()` returns a DataFrame with rows containing `NULL` values removed. With the default behavior, a row is dropped if it contains a missing value in any column.

The result is saved in `test2`. This does not edit or delete rows in the original Snowflake table. It only creates a DataFrame representing the cleaned result.

### `test2.show()` and `type(test2)`

`show()` displays the resulting rows. `type(test2)` checks its Python object type; use `print(type(test2))` if the type should appear when running the file as a script.

One detail: at this point, `test` refers to the SQL-filtered DataFrame, not the earlier `DEMO_DB.PUBLIC.CUSTOMER` DataFrame, because `test` was reassigned. Therefore, `test2` drops missing-value rows from the SQL query result.

---

## 12. Why does the name `test` keep changing?

In Python, assigning a new value to an existing variable name replaces its previous value:

```python
test = first_dataframe
test = second_dataframe
```

After the second line, `test` refers to `second_dataframe`. The first DataFrame has not been deleted from Snowflake, but this variable name no longer points to it.

This example reuses `test` several times. Clearer names can make a longer script easier to understand, for example:

```python
sample_customer_df = session.table("SNOWFLAKE_SAMPLE_DATA.TPCH_SF1000.CUSTOMER")
demo_customer_df = session.table("DEMO_DB.PUBLIC.CUSTOMER")
filtered_customer_df = session.sql("...")
```

The suffix `_df` is a common shorthand for “DataFrame.” It is optional.

---

## 13. What happens when the script runs?

The Python interpreter reads the file from top to bottom:

1. It imports the libraries.
2. It creates the settings dictionary.
3. It tries to connect to Snowflake.
4. It creates DataFrames for the requested tables and queries.
5. Calls such as `show()` request and display results.
6. A step that refers to a missing table, inaccessible object, invalid credential, or missing DataFrame column can stop the script with an error.

Most Snowpark DataFrame operations describe a query rather than immediately processing every row in Python. An action such as `show()` requests results, and Snowflake performs the data work.

---

## 14. Requirements for running this example

Before running the Python file, make sure:

1. Python is installed and selected in your editor.
2. The Snowflake Snowpark Python package is installed in that Python environment.
3. The connection settings are valid and safely provided.
4. The account can be reached from your computer.
5. The user, role, warehouse, database, schema, and tables exist and the role has the required permissions.
6. The shared sample database is available to the account if you want to read its table.
7. The `test4` column-selection mismatch described above is corrected if that line is meant to run.

This guide explains the code; it does not connect to Snowflake or prove that the account, credentials, tables, or permissions are valid.

---

## 15. Short glossary

| Word | Meaning |
| --- | --- |
| Account | The Snowflake environment to which the program connects. |
| Column | One category of information in a table. |
| DataFrame | A Snowpark object representing rows, columns, and query operations. |
| Database | A container that holds schemas and other objects. |
| Dictionary | A Python structure that stores key-value pairs. |
| Filter | Keep only rows matching a condition. |
| Import | Make code from a library available in a Python file. |
| `NULL` | A missing or unknown database value. |
| Role | A Snowflake identity that determines permissions. |
| Schema | A named group of database objects, such as tables. |
| Select | Choose which columns to include. |
| Session | The connection between the Python program and Snowflake. |
| Show | Request and display a preview of DataFrame rows. |
| Warehouse | Snowflake compute resources used to run queries. |

## In one sentence

This example uses a Snowpark session to connect to Snowflake, create DataFrames from tables and SQL, inspect them, filter rows, choose columns, and remove rows with missing values.
