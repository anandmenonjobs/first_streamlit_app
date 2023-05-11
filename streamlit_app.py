
import streamlit
import snowflake.connector
import requests
import pandas
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')
   
streamlit.header('Breakfast Favorites')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),["Avocado","Strawberries"])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
#import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#streamlit.text(fruityvice_response.json())
# convert the raw json
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# display it 
streamlit.dataframe(fruityvice_normalized)

def get_fruityvice_data(this_fruity_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruity_choice)
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   return fruityvice_normalized

try:

   fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
   if not fruit_choice:
      streamlit.error('Please select a fruit to get information')
   else:
      #streamlit.write('The user entered ', fruit_choice)
      #fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
      #fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
      #streamlit.dataframe(fruityvice_normalized)
      fruityvice_response = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(fruityvice_response)
except URLError as e:
   streamlit.error()

streamlit.stop()
#import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.text("Fruit load list contains:")
streamlit.dataframe(my_data_row)

fruit_choice_second = streamlit.text_input('What fruit would you like to add?','Jackfruit')
streamlit.write('Thanks for adding ', fruit_choice_second)

my_cur.execute("insert into fruit_load_list values('from streamlit')")
