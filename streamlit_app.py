# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!\
  """)
from snowflake.snowpark.functions import col, when_matched
from snowflake.snowpark import Session
cnx=st.connection("snowflake")
session = cnx.session()
og_dataset = session.table("smoothies.public.orders")
editable_df = pd.DataFrame([
    {"ORDER_UID": "123", "ORDER_FILLED": "Yes"},
    {"ORDER_UID": "456", "ORDER_FILLED": "No"}
])
edited_dataset = session.create_dataframe(editable_df)

og_dataset.merge(
    edited_dataset,
    og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'],
    [
        when_matched().update({
            'ORDER_FILLED': edited_dataset['ORDER_FILLED']
        })
    ]
)


name_on_order = st.text_input("Name on Smoothie!:")
st.write("The name on your Smoothie will be:", name_on_order)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('fruit_name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients:'
                                 , my_dataframe
                                 , max_selections=5)

if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    st.write(ingredients_string)
    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    st.write(my_insert_stmt)
    #st.stop()
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
