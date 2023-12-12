import streamlit as st
import pandas as pd
from PIL import Image
from io import BytesIO
import requests


if __name__ == "__main__":
    data = pd.read_csv(r'streamlit/salaries.csv')
    st.title("Example of DataFrame on Streamlit")
    st.header("Example of DataFrame on Streamlit")
    st.subheader("Describe")
    st.write('''This project is made by Vorobeva Viktoriya group (231-2). \nThis bot can make graphics connected to my DATA-set (Fruits and Vegetables Prices In USA In The Year 2020), can show some interesting statistics and check hypotisis. \nThis dataset contains information about the 'Fruits and Vegetables Prices In USA In The Year 2020'. The dataset contains 8 columns and 156 rows.\nThe column description of the dataset is as follows:\n1) Item: Name of the fruit or the vegetable.\n2) Form: The form of the item, i.e., canned, fresh, juice, dried or frozen.\n3) Retail Price: Average retail price of the item in the year.\n4) Retail Price Unit: Average retail price's measurement unit.\n5) Yield: Average yield of the item in the year.\n6) Cup Equivalent Size: Comparison done with one edible cup of food.\n7) Cup Equivalent Unit: Comparison's measurement unit.\n8) Cup Equivalent Price: Price per edible cup equivalent (The Unit of Measurement for Federal Recommendations for Fruit and Vegetable Consumptions''')
    st.dataframe(data.head())
    st.subheader("Graphics")
    choose = st.selectbox("Graphics: ", ['interrelation (Difference to Price In %) and (Difference to Cup In %)  without Form Juice', 'describe', ' Proportion of Fresh, Canned, etc... Fruits and Vegetables','Connection between different Forms and Retail price',1111 ' interrelation (Difference to Price In %) and (Difference to Cup In %)  without Form Juice',' Graphic Fresh',' Graphic Canned',  ' Graphic Juice',  ' Graphic Dried',' Graphic Frozen', ])
    if choose == 'interrelation (Difference to Price In %) and (Difference to Cup In %)  without Form Juice':
        response = requests.get(https://raw.githubusercontent.com/vikamvorobyeva/HSE_BOT/main/cupsize.png)
        img =
    if choose == 'describe':
        response = requests.get(https://raw.githubusercontent.com/vikamvorobyeva/HSE_BOT/main/describe.png)
        img =
    if choose == ' Proportion of Fresh, Canned, etc... Fruits and Vegetables':
        response = requests.get(https://raw.githubusercontent.com/vikamvorobyeva/HSE_BOT/main/different_forms.png)
        img =
    if choose == 'Connection between different Forms and Retail price':
        response = requests.get(https://raw.githubusercontent.com/vikamvorobyeva/HSE_BOT/main/forms_from_retailprice.png)
        img =
    if choose == 'interrelation (Difference to Price In %) and (Difference to Cup In %) without Form Juice':
        response = requests.get()
        img =
    if choose == 'Graphic Fresh':
        response = requests.get()
        img =
    if choose == 'Graphic Canned':
        response = requests.get()
        img =
    if choose == 'Graphic Juice':
        response = requests.get()
        img =
    if choose == 'Graphic Dried':
        response = requests.get()
        img =
    if choose == 'Graphic Frozen':
        response = requests.get()
        img =
