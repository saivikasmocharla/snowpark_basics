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

test = session.table("SNOWFLAKE_SAMPLE_DATA.TPCH_SF1000.CUSTOMER")
test.show()

test = session.table("DEMO_DB.PUBLIC.CUSTOMER")
type(test)
t = test.cache_result()

test = session.sql("select * from SNOWFLAKE_SAMPLE_DATA.TPCH_SF1000.CUSTOMER WHERE C_NATIONKEY='23'")
type(test)
test.show()

test3 = test.filter(col("C_NATIONKEY")=='23').select("C_NAME")
type(test3)
test3.show()


test4 = test3.select("C_NATIONKEY","c_acctbal")
test4.show()
type(test4)

test2 = test.na.drop()
test2.show()

type(test2)
