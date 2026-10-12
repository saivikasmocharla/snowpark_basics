# Snowpark Basics Notes

This document explains each part of the Snowpark example in `2_snowpark_test.py` and helps you understand the key Snowpark APIs, DataFrames, and operations.

---

## 1. What is Snowpark?

Snowpark is a library from Snowflake that lets you use Python to work with data in Snowflake.

Instead of writing only SQL in Snowflake, you can:
- create a session
- load data into a DataFrame
- filter, select, aggregate, and transform data
- run SQL queries from Python
- push most work to Snowflake engine for execution

This is useful because Python code can be more readable and easier to build than writing large SQL statements in some cases.

---

## 2. Imports used in the script

```python
import os
import snowflake.snowpark.functions
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
```

### `import os`
This imports the Python standard library module `os`.

It is used for operating system-related functionality such as reading environment variables, file paths, and system variables.

In this script, it is not used directly, but it is often used in real projects for:
- reading secret values
- reading environment config
- setting paths

### `import snowflake.snowpark.functions`
This imports the Snowpark functions module.

It includes many built-in functions that you can use in DataFrame operations, such as:
- `sum()`
- `avg()`
- `count()`
- `lit()`
- `when()`
- date functions and string functions

### `from snowflake.snowpark import Session`
This imports the `Session` class.

`Session` is the main entry point for connecting to Snowflake.

It represents the connection to the Snowflake account and lets you:
- run SQL queries
- read tables as DataFrames
- use Snowflake compute features
- access warehouse, database, and schema context

### `from snowflake.snowpark.functions import col`
This imports the `col` function.

`col("column_name")` is used to refer to a column in a DataFrame.

Example:

```python
col("C_NAME")
```

This means: use the `C_NAME` column from the DataFrame.

---

## 3. Connection parameters

```python
connection_parameters = {
    "account": "iivhvcb-dp48049",
    "user": "vikas",
    "password": "GlobeTrotter@1",
    "role": "ACCOUNTADMIN",
    "warehouse": "COMPUTE_WH",
    "database": "DEMO_DB",
    "schema": "PUBLIC"
}
```

This dictionary contains all required connection settings needed to connect to Snowflake.

### Key values explained

#### `account`
Your Snowflake account identifier.

For example:
- `xy12345.eu-central-1`
- `xy12345`

This identifies your Snowflake account.

#### `user`
The Snowflake username.

#### `password`
The password for the user.

#### `role`
The Snowflake role to use.

`ACCOUNTADMIN` is a powerful role used for administrative tasks.

#### `warehouse`
The virtual warehouse to use for compute.

`COMPUTE_WH` is a warehouse name. Snowpark uses it to run queries.

#### `database`
The default database to use.

Example: `DEMO_DB`

#### `schema`
The default schema in the database.

Example: `PUBLIC`

---

## 4. The `Session` object

```python
session = Session.builder.configs(connection_parameters).create()
```

This is the most important line in the script.

### What does it do?
It creates a connection to Snowflake using the login details from `connection_parameters`.

### `Session.builder`
This is a builder object used to configure the session.

### `.configs(connection_parameters)`
This attaches the connection parameters to the builder.

### `.create()`
This actually creates the connection to Snowflake and returns a `Session` object.

### What does the session allow?
The session can:
- run SQL
- access Snowflake tables
- read data into DataFrames
- execute DataFrame operations

---

## 5. Using SQL through the session

```python
session.sql("USE WAREHOUSE COMPUTE_WH").collect()
```

This runs a SQL statement in Snowflake through the session.

### `session.sql(...)`
This method accepts a SQL string and returns a DataFrame-like object for the result.

### `USE WAREHOUSE COMPUTE_WH`
This tells Snowflake to use the specified warehouse for the session.

### `.collect()`
This executes the query and fetches the results back to the client.

This is important because:
- `session.sql(...)` builds the query
- `collect()` triggers execution and returns results to Python

### Why is this needed?
Sometimes you need to change session context such as:
- warehouse selection
- database selection
- schema selection

In Snowpark, it is common to use SQL to configure the environment before working with DataFrames.

---

## 6. DataFrame in Snowpark

A DataFrame is a structured table-like object.

It stores data in a columnar format and supports operations like:
- filter
- select
- join
- groupBy
- sort
- agg
- show
- count
- describe

In this example, the DataFrame is created from a Snowflake table.

---

## 7. Reading a Snowflake table into a DataFrame

```python
df_customer_info = session.table("SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER")
```

### `session.table(...)`
This method reads an existing table from Snowflake and creates a Snowpark DataFrame.

### `SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER`
This is the fully qualified table name:
- database: `SNOWFLAKE_SAMPLE_DATA`
- schema: `TPCH_SF1`
- table: `CUSTOMER`

So the code loads the `CUSTOMER` table into a DataFrame called `df_customer_info`.

### Why is this useful?
You can now work with the table using DataFrame API instead of writing raw SQL for every step.

---

## 8. `filter()` operation

```python
df_customer_filter = df_customer_info.filter(col("C_MKTSEGMENT") == 'HOUSEHOLD')
```

### What does this do?
It filters rows where the column `C_MKTSEGMENT` equals `'HOUSEHOLD'`.

### `df_customer_info`
This is the source DataFrame.

### `.filter(...)`
This method applies a condition and keeps only matching rows.

### `col("C_MKTSEGMENT")`
This represents the `C_MKTSEGMENT` column.

### `== 'HOUSEHOLD'`
This is the filter condition.

### Important idea
Snowpark DataFrame expressions are lazy by default. This means the filter is defined, but not executed until an action is triggered, such as:
- `show()`
- `count()`
- `collect()`

---

## 9. `select()` operation

```python
df_customer_select = df_customer_info.select(col("C_NAME"), col("C_ADDRESS"))
```

### What does it do?
It chooses only selected columns from the DataFrame.

### Selected columns:
- `C_NAME`
- `C_ADDRESS`

### Output
A new DataFrame with only these columns.

### Why is this useful?
It reduces the amount of data and keeps only the fields you need.

---

## 10. `show()`

```python
df_customer_select.show()
```

### What does `show()` do?
It displays the DataFrame content in the console.

This is one of the most common ways to inspect data during development.

### Example output conceptually
You can see rows with values in `C_NAME` and `C_ADDRESS`.

### Why is it important?
It helps validate whether the transformations are working.

---

## 11. `count()`

```python
df_customer_select.count()
```

### What does it do?
It returns the number of rows in the DataFrame.

### Why is it useful?
You can measure the size of filtered data or selected data.

### Example:
If there are 150,000 rows, the count will return that integer.

---

## 12. `describe()`

```python
df_customer_select.describe().sort("SUMMARY").show()
```

### `describe()`
This gives summary statistics for the DataFrame columns.

For numeric columns, it usually shows metrics such as:
- count
- mean
- stddev
- min
- max

For string columns, it may show general data profile info depending on the column type.

### `.sort("SUMMARY")`
This sorts the summary rows by the `SUMMARY` column.

This makes the output more readable.

### `.show()`
Finally, the result is displayed on screen.

### Why is this valuable?
It gives a quick statistical overview of the DataFrame.

---

## 13. DataFrame execution model

Snowpark uses a lazy execution model.

This means:
- defining a DataFrame does not immediately execute the operation
- operations are built into a query plan
- execution happens when an action method is called

### Examples of actions
- `show()`
- `count()`
- `collect()`
- `to_pandas()`
- `write.save_as_table()`

### Examples of transformations
- `filter()`
- `select()`
- `sort()`
- `with_column_renamed()`
- `join()`

This is a very important concept in Snowpark and Spark-like DataFrame APIs.

---

## 14. Step-by-step explanation of the code

Here is the full code again:

```python
import os
import snowflake.snowpark.functions
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col


connection_parameters = {"account":"iivhvcb-dp48049",
"user":"vikas",
"password": "GlobeTrotter@1",
"role":"ACCOUNTADMIN",
"warehouse":"COMPUTE_WH",
"database":"DEMO_DB",
"schema":"PUBLIC"
}


session = Session.builder.configs(connection_parameters).create()
session.sql("USE WAREHOUSE COMPUTE_WH").collect()


df_customer_info = session.table("SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER")
df_customer_filter = df_customer_info.filter(col("C_MKTSEGMENT") == 'HOUSEHOLD')
df_customer_select = df_customer_info.select(col("C_NAME"), col("C_ADDRESS"))
df_customer_select.show()
df_customer_select.count()


df_customer_select.describe().sort("SUMMARY").show()
```

### Step 1: Create session
This connects to Snowflake.

### Step 2: Use warehouse
This tells Snowflake which warehouse to use for compute.

### Step 3: Load CUSTOMER table
The full table is loaded into a DataFrame.

### Step 4: Filter by market segment
It keeps only rows where `C_MKTSEGMENT = 'HOUSEHOLD'`.

### Step 5: Select two columns
It keeps only `C_NAME` and `C_ADDRESS`.

### Step 6: Display rows
`show()` prints the selected records.

### Step 7: Count data
`count()` returns how many rows are in `df_customer_select`.

### Step 8: Get summary stats
`describe()` shows data distribution summary and then `sort("SUMMARY")` organizes the output.

---

## 15. Important Snowpark API concepts

### `Session`
Represents a connection to Snowflake.

### `DataFrame`
Represents table-like data in Snowpark.

### `Column`
Represents a DataFrame column and can be used in expressions.

### `functions.col()`
Used to reference a column by name.

### `Table`
A Snowflake table loaded into a DataFrame.

### `show()`
Displays rows.

### `count()`
Counts rows.

### `select()`
Chooses specific columns.

### `filter()`
Keeps rows matching a condition.

### `sort()`
Orders rows or summary entries.

### `describe()`
Shows summary statistics.

### `collect()`
Pulls data back to the local client from Snowflake.

---

## 16. Difference between SQL and DataFrame API

### SQL style
```sql
SELECT C_NAME, C_ADDRESS
FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER
WHERE C_MKTSEGMENT = 'HOUSEHOLD';
```

### Snowpark DataFrame style
```python
df_customer_info = session.table("SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.CUSTOMER")
df_customer_select = df_customer_info.filter(col("C_MKTSEGMENT") == 'HOUSEHOLD') \
    .select(col("C_NAME"), col("C_ADDRESS"))
```

Both approaches can achieve the same result.

The DataFrame API is more Pythonic and easier to chain in code.

---

## 17. Why DataFrame API is powerful

Snowpark lets you combine:
- Python logic
- SQL-like operations
- Snowflake execution engine

This means you can write code that is easy to read and still leverage Snowflake performance.

---

## 18. Beginner tips

1. Start with `session.table(...)` to load a table
2. Use `select()` to choose columns
3. Use `filter()` to narrow rows
4. Use `show()` to inspect the result
5. Use `count()` to verify size
6. Use `describe()` to summarize values
7. Always remember: DataFrame operations are often lazy until an action is called

---

## 19. Real-world use case

This code is a common pattern in Snowpark:
- connect to Snowflake
- set warehouse context
- load table into DataFrame
- filter rows
- select columns
- analyze or display data

This is exactly how many data engineering tasks begin in Snowflake.

---

## 20. Summary

The script demonstrates the core Snowpark workflow:

1. Create a `Session`
2. Set warehouse context
3. Read a table using `session.table()`
4. Use DataFrame operations like `filter()` and `select()`
5. Inspect results using `show()` and `count()`
6. Summarize data with `describe()`

This is the foundation of Snowpark programming.

---

## 21. Quick cheat sheet

```python
# Create session
session = Session.builder.configs(connection_parameters).create()

# Run SQL
session.sql("SELECT 1").collect()

# Load table
customer_df = session.table("DATABASE.SCHEMA.TABLE")

# Filter rows
filtered_df = customer_df.filter(col("COL1") == "VALUE")

# Select columns
selected_df = filtered_df.select(col("COL1"), col("COL2"))

# Show data
selected_df.show()

# Count rows
selected_df.count()

# Describe data
selected_df.describe().show()
```

This cheat sheet helps you remember the most important Snowpark APIs.
