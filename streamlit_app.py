import streamlit as st
from snowflake.snowpark.functions import col
import snowflake.connector

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Accessing Snowflake credentials from secrets
snowflake_credentials = st.secrets["connections"]["snowflake"]

# Establishing connection to Snowflake
conn = snowflake.connector.connect(
    account=snowflake_credentials["BNYSQPU-ID92342"],
    user=snowflake_credentials["SALUNKHEAKANKSHA23"],
    password=snowflake_credentials["HariOm@23"],
     role=snowflake_credentials["ACCOUNTADMIN"],
    warehouse=snowflake_credentials["COMPUTE_WH"],
    database=snowflake_credentials["SMOOTHIES"],
    schema=snowflake_credentials["PUBLIC"],
    client_session_keep_alive=snowflake_credentials["client_session_keep_alive"]
)

session = conn.cursor()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ', '.join(ingredients_list)

    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders (ingredients, name_on_order)
    VALUES ('{ingredients_string}', '{name_on_order}')
    """

    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.execute(my_insert_stmt)
        st.success(f'Your Smoothie is ordered, {name_on_order}!', icon="✅")
