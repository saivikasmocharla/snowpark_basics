from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import time

from snowflake.snowpark.types import IntegerType, StringType, StructField, StructType, DateType

# Replace the below connection_parameters with your respective snowflake account,user name and password
connection_parameters = {"account":"iivhvcb-dp48049",
"user":"vikas",
"password": "GlobeTrotter@1",
"role":"ACCOUNTADMIN",
"warehouse":"COMPUTE_WH",
"database":"DEMO_DB",
"schema":"PUBLIC"
}

session = Session.builder.configs(connection_parameters).create()
session.sql("use warehouse compute_wh").collect()

schema = StructType([StructField("one", IntegerType()),
StructField("two",  IntegerType()),
StructField("three",  IntegerType()),
StructField("four",  DateType())])

test = session.create_dataframe([[1, 2, 3, '2022-01-26'],[1, 2, 3, '2022-01-26'],[1, 2, 3, '2022-01-26'],[1, 2, 3, '2022-01-26']], schema=["a","b","c","d"])
test.show()

test = session.create_dataframe([[1, 2, 3, '2022-01-26'],[1, 2, 3, '2022-01-26'],[1, 2, 3, '2022-01-26'],[1, 2, 3, '2022-01-26']], schema=schema)
test.show()



data = [
    ("C101", "M101", "apollo hospital", 5000),
    ("C102", "M102", "city care", 12000),
    ("C103", "M103", "medplus", -500),
    ("C104", "M101", "apollo hospital", 8000),
    ("C105", "M104", "city care", 15000)
]

df = session.create_dataframe(
    data,
    schema=[
        "CLAIM_ID",
        "MEMBER_ID",
        "PROVIDER_NAME",
        "CLAIM_AMOUNT"
    ]
)

df.show()


df.print_schema()

print(df.schema.names)

print(df.count())

#==============================


from snowflake.snowpark.types import (
    StructType,
    StructField,
    StringType,
    IntegerType
)

schema = StructType([
    StructField("CLAIM_ID", StringType()),
    StructField("MEMBER_ID", StringType()),
    StructField("PROVIDER_NAME", StringType()),
    StructField("CLAIM_AMOUNT", IntegerType())
])

df_explicit = session.create_dataframe(
    data,
    schema=schema
)

df_explicit.print_schema()
df_explicit.show()

#-
from snowflake.snowpark.functions import (
    col,
    upper,
    trim
)

clean_df = (
    df
    .with_column(
        "PROVIDER_NAME",
        upper(trim(col("PROVIDER_NAME")))
    )
    # Add a filter to exclude invalid claims
)

clean_df.show()


from snowflake.snowpark.functions import when

final_df = clean_df.with_column(
    "CLAIM_CATEGORY",
    when(
        col("CLAIM_AMOUNT") >= 10000,
        "HIGH"
    ).otherwise("NORMAL")
)

final_df.select(
    "CLAIM_ID",
    "CLAIM_AMOUNT",
    "CLAIM_CATEGORY"
).show()