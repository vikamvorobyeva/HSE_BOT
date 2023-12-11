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
#Импортируем все нужные библиотеки

TOKEN = "6960205621:AAGYOcdopdHKMrBX_Lnwp3F9xhl8AetFvC0"

dp = Dispatcher()
#Dispatcher — это класс, который играет центральную роль в управлении и обработке входящих событий


df = pd.read_csv("Prices.csv")
#Работа с БДшками

compares = []
button1 = KeyboardButton(text="Get stats")
button2 = KeyboardButton(text="Show data")
button3 = KeyboardButton(text="Check hypothesis")
ex = KeyboardButton(text="Back to menu")
menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[button1, button2, button3]])
b1 = KeyboardButton(text="Check 1")
b2 = KeyboardButton(text="Check 2")
b3 = KeyboardButton(text="Check 3")
hypos = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[b1, b2, b3], [ex]])
but1 = KeyboardButton(text="Graphic 1")
but2 = KeyboardButton(text="Graphic 2")
but3 = KeyboardButton(text="Graphic 3")
datas = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[but1, but2, but3], [ex]])
bt1 = KeyboardButton(text="Form Fresh")
bt2 = KeyboardButton(text="Form Canned")
bt3 = KeyboardButton(text="Form Frozen")
bt4 = KeyboardButton(text="Form Dried")
bt5 = KeyboardButton(text="Form Juice")
forms =ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[bt1, bt2, bt3, bt4, bt5], [ex]])

#Создал все кнопки, которые буду потом использовать


@dp.message(CommandStart()) #Пишем перед функциями где будем работать с входящими сообщениями @dp.message()
async def command_start_handler(message: Message) -> None:
    info = '''This dataset contains information about the 'Fruits and Vegetables Prices In USA In The Year 2020'. The dataset contains 8 columns and 156 rows.

The column description of the dataset is as follows:

1) Item: Name of the fruit or the vegetable.

2) Form: The form of the item, i.e., canned, fresh, juice, dried or frozen.

3) Retail Price: Average retail price of the item in the year.

4) Retail Price Unit: Average retail price's measurement unit.

5) Yield: Average yield of the item in the year.

6) Cup Equivalent Size: Comparison done with one edible cup of food.

7) Cup Equivalent Unit: Comparison's measurement unit.

8) Cup Equivalent Price: Price per edible cup equivalent (The Unit of Measurement for Federal Recommendations for Fruit and Vegetable Consumptio''' #info - описание содержания БДшки
    await message.answer(info)
    dfi.export(df.head(5), "start.png")
    #dfi - библа которая сохраняет DataFrame в виде картинки, можно указать путь
    photo = FSInputFile("start.png") #берет файл путь до которого ты указываешь
    await message.answer_photo(photo=photo, caption="Part of DataFrame", reply_markup=menu)
    #caption - подпись к фото
    #reply_markup - говорит какие кнопки использовать

@dp.message(F.text.lower() == "back to menu")
async def back_to_menu(message: Message) -> None:
    await message.answer("Menu", reply_markup=menu)
#создаю общую функцию для выхода в меню


@dp.message(F.text.lower() == "get stats")
async def get_stats(message: Message) -> None:
    #df.info() так просто не получится сохранить как картинку, так как у него тип данных не DataFrame
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    lines = [line.split() for line in s.splitlines()[3:-2]]#Обрезаем лишние строчки, которые мешают сделать dataFrame
    info_df = pd.DataFrame(lines) #Сохраняем в виде DataFrame
    dfi.export(info_df, "info.png")#Cохраняем как картинку
    describe_df = df.describe() #df.describe() в отличии от df.info() является DataFrame, поэтому сохраняем как раньше
    dfi.export(describe_df, "describe.png")
    photo1 = FSInputFile("info.png")
    await message.answer_photo(photo=photo1, caption="Info")
    photo2 = FSInputFile("describe.png")
    await message.answer_photo(photo=photo2, caption="Describe")

def make_series(df: pd.DataFrame, column_name: str, grouping_name: str) -> pd.Series:
    return df.loc[df[column_name] == grouping_name, "RetailPrice"]

@dp.message(F.text.lower() == "show data")
async def show_data(message: Message) -> None:
    await message.answer("1\n2\n3", reply_markup=datas)

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
    plt.savefig("different_forms.png")  # Строим графики из коллабы и сохраняем их с помощью savefig
    plt.clf()  # Обязательно не забыть очистить после этого график, так как они могут меняться друг из-за друга
    photo = FSInputFile("different_forms.png")
    await message.answer_photo(photo=photo, reply_markup=datas)

@dp.message(F.text.lower() == "graphic 2")
async def print_gr2(message: Message) -> None:
    figsize = (12, 1.2 * len(df['Form'].unique()))
    plt.figure(figsize=figsize)
    sns.violinplot(df, x='RetailPrice', y='Form', inner='stick', palette='Dark2')
    sns.despine(top=True, right=True, bottom=True, left=True)
    plt.xlabel("RetailPrice, USD")
    plt.savefig("forms_from_retailprice.png")  # Строим графики из коллабы и сохраняем их с помощью savefig
    plt.clf()  # Обязательно не забыть очистить после этого график, так как они могут меняться друг из-за друга
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
    plt.savefig("cupsize.png")  # Строим графики из коллабы и сохраняем их с помощью savefig
    plt.clf()  # Обязательно не забыть очистить после этого график, так как они могут меняться друг из-за друга
    photo = FSInputFile("cupsize.png")
    await message.answer_photo(photo=photo, reply_markup=datas)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API␣˓→calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)

def check_hypothesis(series_1: pd.Series, series_2: pd.Series, alpha=0.05) -> str:
    #Эту функцию мы писали на паре раньше
    series_1.dropna(inplace=True)
    series_2.dropna(inplace=True)
    std1 = series_1.std()
    std2 = series_2.std()
    result = st.ttest_ind(series_1, series_2, equal_var=(std1==std2))
    if result.pvalue < alpha:
        return "Можем отвергнуть гипотезу"
    else:
        return "Не можем отвергнуть гипотезу"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
