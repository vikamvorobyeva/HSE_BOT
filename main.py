import pandas as pd
import io
import dataframe_image as dfi
import numpy as np
import plotly
import matplotlib.pyplot as plt
from scipy import stats as st
import asyncio
import logging
import sys
from os import getenv
from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram import F
from aiogram.types import Message, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.markdown import hbold
from aiogram.filters.command import Command
import seaborn as sns
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "6960205621:AAGYOcdopdHKMrBX_Lnwp3F9xhl8AetFvC0"

dp = Dispatcher()



df = pd.read_csv("Prices.csv")

compares = []
button1 = KeyboardButton(text="Info about DATA")
button2 = KeyboardButton(text="Show data")
button3 = KeyboardButton(text="Check hypothesis")
button4 = KeyboardButton(text="Addings to the DATA")
ex = KeyboardButton(text="Back to menu")
menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[button1, button2, button3, button4]])
b1 = KeyboardButton(text="Check 1")
b2 = KeyboardButton(text="Check 2")
b3 = KeyboardButton(text="Check 3")
hypos = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[b1, b2, b3], [ex]])
but1 = KeyboardButton(text="Graphic 1")
but2 = KeyboardButton(text="Graphic 2")
but3 = KeyboardButton(text="Graphic 3")
but4 = KeyboardButton(text="Graphic 4")
but5 = KeyboardButton(text="Graphic 5")
but6 = KeyboardButton(text="Other graphics")
datas = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[but1, but2, but3, but4, but5, but6], [ex]])
but6 = KeyboardButton(text="Graphic Fresh")
but7 = KeyboardButton(text="Graphic Canned")
but8 = KeyboardButton(text="Graphic Juice")
but9 = KeyboardButton(text="Graphic Dried")
but10 = KeyboardButton(text="Graphic Frozen")
grtypes = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[but6, but7, but8, but9, but10], [ex]])
bt1 = KeyboardButton(text="Form Fresh")
bt2 = KeyboardButton(text="Form Canned")
bt3 = KeyboardButton(text="Form Frozen")
bt4 = KeyboardButton(text="Form Dried")
bt5 = KeyboardButton(text="Form Juice")
forms =ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[bt1, bt2, bt3, bt4, bt5], [ex]])




@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    info = '''This project is made by Vorobeva Viktoriya group (231-2). 
This bot can make graphics connected to my DATA-set (Fruits and Vegetables Prices In USA In The Year 2020), can show some interesting statistics and check hypotisis. 

This dataset contains information about the 'Fruits and Vegetables Prices In USA In The Year 2020'. The dataset contains 8 columns and 156 rows.

The column description of the dataset is as follows:

1) Item: Name of the fruit or the vegetable.
2) Form: The form of the item, i.e., canned, fresh, juice, dried or frozen.
3) Retail Price: Average retail price of the item in the year.
4) Retail Price Unit: Average retail price's measurement unit.
5) Yield: Average yield of the item in the year.
6) Cup Equivalent Size: Comparison done with one edible cup of food.
7) Cup Equivalent Unit: Comparison's measurement unit.
8) Cup Equivalent Price: Price per edible cup equivalent (The Unit of Measurement for Federal Recommendations for Fruit and Vegetable Consumptions'''

    await message.answer(info)
    dfi.export(df.head(5), "start.png")
    photo = FSInputFile("start.png")
    await message.answer_photo(photo=photo, caption="Part of DataFrame", reply_markup=menu)


@dp.message(F.text.lower() == "back to menu")
async def back_to_menu(message: Message) -> None:
    await message.answer("Menu", reply_markup=menu)



@dp.message(F.text == "Info about DATA")
async def get_stats(message: Message) -> None:

    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    lines = [line.split() for line in s.splitlines()[3:-2]]
    info_df = pd.DataFrame(lines)
    dfi.export(info_df, "info.png")
    describe_df = df.describe()
    dfi.export(describe_df, "describe.png")
    photo1 = FSInputFile("info.png")
    await message.answer_photo(photo=photo1, caption="Info")
    photo2 = FSInputFile("describe.png")
    await message.answer_photo(photo=photo2, caption="Describe")


df_11 = df
a = df_11['CupEquivalentSize'].mean()
df_cup = [a] * 155
df_11.insert(loc=7, column='MeanCupEquivalentSize', value=df_cup)
df_diff1 = ((df_11['CupEquivalentSize'] - df_11['MeanCupEquivalentSize']) * (100 / df_11['MeanCupEquivalentSize']))
df_diff11 = df_diff1.round()
df_11.insert(loc=7, column='DifferenceIn%', value=df_diff11)
b = df_11['CupEquivalentPrice'].mean()
df_cup11 = [b] * 155
df_11.insert(loc=10, column='MeanCupEquivalentPrice', value=df_cup11)
df_diff2 = ((df_11['CupEquivalentPrice'] - df_11['MeanCupEquivalentPrice']) * (100 / df_11['MeanCupEquivalentPrice']))
df_diff22 = df_diff2.round()
df_11.insert(loc=10, column='DifferencePriceIn%', value=df_diff22)
df_usd = ['USD'] * 155
df_11.insert(loc=3, column='currency', value=df_usd)




@dp.message(F.text.lower() == "addings to the data")
async def addings(message: Message) -> None:

    buffer = io.StringIO()
    df_11.info(buf=buffer)
    s = buffer.getvalue()
    lines = [line.split() for line in s.splitlines()[3:-2]]
    info_df_11 = pd.DataFrame(lines)
    dfi.export(info_df_11, "info.png")
    describe_df_11 = df_11.describe()
    dfi.export(describe_df_11, "describe.png")
    photo1 = FSInputFile("info.png")
    await message.answer_photo(photo=photo1, caption=" New Info")
    photo2 = FSInputFile("describe.png")
    await message.answer_photo(photo=photo2, caption="New Describe")
    info1 = ''' To the DATA I add 5 new columns( MeanCupEquivalentSize, DifferenceIn%, MeanCupEquivalentPrice, DifferencePriceIn%)
    1)MeanCupEquivalentSize - the average value of the column CupEquivalentSize
    2)DifferenceIn% - deviation from the average by CupEquivalentSize
    3)MeanCupEquivalentPrice - the average value of the column CupEquivalentPrice
    4)DifferencePriceIn% - deviation from the average by CupEquivalentPrice
    5)currency in USD
    '''
    await message.answer(info1)
    dfi.export(df_11.head(5), "start.png")
    photo = FSInputFile("start.png")
    await message.answer_photo(photo=photo, caption="Part of new DataFrame", reply_markup=menu)


def make_series(df: pd.DataFrame, column_name: str, grouping_name: str) -> pd.Series:
    return df.loc[df[column_name] == grouping_name, "RetailPrice"]

@dp.message(F.text.lower() == "show data")
async def show_data(message: Message) -> None:
    await message.answer("1) Proportion of Fresh, Canned, etc... Fruits and Vegetables\n2) Connection between different Forms and Retail price\n3) Comparison with one edible cup of food\n4) Comparison Cup equivalent price with its size\n5) interrelation (Difference to Price In %) and (Difference to Cup In %) and the same grapic but without Form Juice\n6) Compaering retail price with different Forms of fruits and vegetables", reply_markup=datas)


@dp.message(F.text.lower() == "check hypothesis")
async def check_hypo(message: Message) -> None:
    await message.answer("This hypothesis compare average retail price between two forms of fruits and vegetables.\nInput first form:", reply_markup=forms)

@dp.message(F.text.lower().split()[0] == "form")
async def add_to_check(message: Message) -> None:
    compares.append(message.text.split()[1])
    if len(compares) % 2 == 1:
        await message.answer("Input second form:", reply_markup=forms)
    else:
        ans = check_hypothesis(make_series(df, "Form", compares[-2]), make_series(df, "Form", compares[-1]))
        await message.answer(ans, reply_markup=menu)


@dp.message(F.text.lower() == "graphic 1")
async def print_gr1(message: Message) -> None:
    df_cross = pd.crosstab(index=df['Form'], columns='count')
    df_cross.groupby(['Form']).sum().plot(kind='pie', y='count', autopct='%1.0f%%',
                                          colors=['pink', 'turquoise', 'steelblue', 'purple', 'beige'],
                                          title='Proportion of fruits and vegetables (fresh, canned, etc)')
    plt.legend(bbox_to_anchor=(0.0, 0.17), loc='upper left', borderaxespad=0)
    plt.savefig("different_forms.png")
    plt.clf()
    photo = FSInputFile("different_forms.png")
    await message.answer_photo(photo=photo, reply_markup=datas)

@dp.message(F.text.lower() == "graphic 2")
async def print_gr2(message: Message) -> None:
    figsize = (12, 1.2 * len(df['Form'].unique()))
    plt.figure(figsize=figsize)
    sns.violinplot(df, x='RetailPrice', y='Form', inner='stick', palette='Dark2')
    sns.despine(top=True, right=True, bottom=True, left=True)
    plt.xlabel("RetailPrice, USD")
    plt.savefig("forms_from_retailprice.png")
    plt.clf()
    photo = FSInputFile("forms_from_retailprice.png")
    await message.answer_photo(photo=photo, reply_markup=datas)

@dp.message(F.text.lower() == "graphic 3")
async def print_gr3(message: Message) -> None:
    df.loc[df['Form'] == 'Fresh', 'CupEquivalentSize'].plot(kind='hist', alpha=0.7)
    df.loc[df['Form'] == 'Canned', 'CupEquivalentSize'].plot(kind='hist', alpha=0.7)
    df.loc[df['Form'] == 'Frozen', 'CupEquivalentSize'].plot(kind='hist', alpha=0.7)
    plt.legend(['Fresh', 'Canned', 'Frozen'])
    plt.title("Fresh, Canned and Frozen")
    plt.ylabel("Comparison With One Edible Cup of Food")
    plt.xlabel("Quantity")
    plt.savefig("cupsize.png")
    plt.clf()
    photo = FSInputFile("cupsize.png")
    await message.answer_photo(photo=photo, reply_markup=datas)


@dp.message(F.text.lower() == "graphic 4")
async def print_gr4(message: Message) -> None:
    df_pricess = df[df['Form'].isin(['Fresh', 'Canned', 'Frozen'])]
    df_pricess.plot.scatter(x='CupEquivalentSize', y='CupEquivalentPrice', s=10, c='turquoise')
    plt.savefig("cupsize.png")
    plt.clf()
    photo = FSInputFile("cupsize.png")
    await message.answer_photo(photo=photo, reply_markup=datas)

@dp.message(F.text.lower() == "graphic 5")
async def print_gr5(message: Message) -> None:
    df_11.plot(kind='scatter', x='DifferenceIn%', y='DifferencePriceIn%', s=5, alpha=.8, c='purple')
    plt.gca().spines[['top', 'right', ]].set_visible(False)
    plt.xlabel("interrelation (Difference to Price In %) and (Difference to Cup In %)")
    plt.savefig("cupsize.png")
    plt.clf()
    photo = FSInputFile("cupsize.png")
    await message.answer_photo(photo=photo, reply_markup=datas)
    df_without_juice = df[df.Form != "Juice"]
    df_without_juice.plot(kind='scatter', x='DifferenceIn%', y='DifferencePriceIn%', s=5, alpha=.8, c='red')
    plt.gca().spines[['top', 'right', ]].set_visible(False)
    plt.xlabel("interrelation (Difference to Price In %) and (Difference to Cup In %) without form Juice")
    plt.savefig("cupsize.png")
    plt.clf()
    photo = FSInputFile("cupsize.png")
    await message.answer_photo(photo=photo, reply_markup=datas)

@dp.message(F.text.lower() == "other graphics")
async def other_graphics(message: Message) -> None:
    await message.answer("Choose a form:", reply_markup=grtypes)

@dp.message(F.text.lower() == "graphic fresh")
async def print_gr6(message: Message) -> None:
    df_fresh = df[df['Form'].str.contains('Fresh')]
    df_fresh['RetailPrice'].plot(kind='line', figsize=(8, 4), title='RetailPrice')
    plt.gca().spines[['top', 'right']].set_visible(False)
    plt.ylabel("Fresh")
    plt.savefig("cupsize.png")
    plt.clf()
    photo = FSInputFile("cupsize.png")
    await message.answer_photo(photo=photo, reply_markup=datas)


@dp.message(F.text.lower() == "graphic canned")
async def print_gr7(message: Message) -> None:
    df_canned = df[df['Form'].str.contains('Canned')]
    df_canned['RetailPrice'].plot(kind='line', figsize=(8, 4), title='RetailPrice')
    plt.gca().spines[['top', 'right']].set_visible(False)
    plt.ylabel("Canned")
    plt.savefig("cupsize.png")
    plt.clf()
    photo = FSInputFile("cupsize.png")
    await message.answer_photo(photo=photo, reply_markup=datas)

@dp.message(F.text.lower() == "graphic juice")
async def print_gr8(message: Message) -> None:
    df_juice = df[df['Form'].str.contains('Juice')]
    df_juice['RetailPrice'].plot(kind='line', figsize=(8, 4), title='RetailPrice')
    plt.gca().spines[['top', 'right']].set_visible(False)
    plt.ylabel("Juice")
    plt.savefig("cupsize.png")
    plt.clf()
    photo = FSInputFile("cupsize.png")
    await message.answer_photo(photo=photo, reply_markup=datas)

@dp.message(F.text.lower() == "graphic dried")
async def print_gr9(message: Message) -> None:
    df_dried = df[df['Form'].str.contains('Dried')]
    df_dried['RetailPrice'].plot(kind='line', figsize=(8, 4), title='RetailPrice')
    plt.gca().spines[['top', 'right']].set_visible(False)
    plt.ylabel("Dried")
    plt.savefig("cupsize.png")
    plt.clf()
    photo = FSInputFile("cupsize.png")
    await message.answer_photo(photo=photo, reply_markup=datas)


@dp.message(F.text.lower() == "graphic Frozen")
async def print_gr10(message: Message) -> None:
    df_frozen = df[df['Form'].str.contains('Frozen')]
    df_frozen['RetailPrice'].plot(kind='line', figsize=(8, 4), title='RetailPrice')
    plt.gca().spines[['top', 'right']].set_visible(False)
    plt.ylabel("Frozen")
    plt.savefig("cupsize.png")
    plt.clf()
    photo = FSInputFile("cupsize.png")
    await message.answer_photo(photo=photo, reply_markup=datas)


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)

def check_hypothesis(series_1: pd.Series, series_2: pd.Series, alpha=0.05) -> str:

    series_1.dropna(inplace=True)
    series_2.dropna(inplace=True)
    std1 = series_1.std()
    std2 = series_2.std()
    result = st.ttest_ind(series_1, series_2, equal_var=(std1==std2))
    if result.pvalue < alpha:
        return "We can reject the hypothesis"
    else:
        return "We cannot reject the hypothesis"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
