from html2image import Html2Image
from telegram import Update,ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import requests
from random import randint
from bs4 import BeautifulSoup as bs

async def start_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отввечает на выбранный пользователям номер"""
    reply = "Вы выбрали задание " + update.message.text + ". Отправляю вам задание... "
    rand_num = randint(1,3)
    if rand_num == 1: 
        r = requests.get("https://ege.sdamgia.ru/test?id=75953"+str(randint(387,401)))
        soup = bs(r.content, 'html.parser')
        items = soup.find_all('div', align='justify')
        items_answer = soup.find_all('div', class_='prob_view')
    elif rand_num == 2: 
        r = requests.get("https://ege.sdamgia.ru/test?id=73723"+str(randint(696,710)))
        soup = bs(r.content, 'html.parser')
        items = soup.find_all('div', align='justify')
        items_answer = soup.find_all('div', class_='prob_view')
    else:
        r = requests.get("https://ege.sdamgia.ru/test?id=748920"+str(randint(82,96)))
        soup = bs(r.content, 'html.parser')
        items = soup.find_all('div', align='justify')
        items_answer = soup.find_all('div', class_='prob_view')

    if update.message.text in ["№1","№2","№3","№4","№5","№6","№7","№8","№9","№10","№11","№12","№13","№14","№15","№16","№17","№18","№19"]:
        await update.message.reply_text(reply)
        # получение кода задания
        image_code = items[int(update.message.text[1:])-1]
        # получение ответа задания
        answer_num = items_answer[int(update.message.text[1:])-1].find('a').text
        r_answer = requests.get('https://math-ege.sdamgia.ru/problem?id='+answer_num)
        soup_answer = bs(r_answer.content, 'html.parser')
        if int(update.message.text[1:]) <= 12:
            items_answer_get = soup_answer.find('div', class_='answer')
            answer = items_answer_get.text

        if "http" not in image_code:
            image_code = str(image_code).replace('/get', 'https://ege.sdamgia.ru/get',1)
        html = image_code
        htmlimg = Html2Image(browser='edge')
        htmlimg.output_path = 'images'
        css = 'body{background-color:white!important; h1{color:black!important;}}'
        file = (400, 200)
        if update.message.text == "№19":
            file = (400, 400)
        if update.message.text == "№14" or update.message.text == "№9":
            file = (400, 270)
        if update.message.text == "№8" or  update.message.text == "№5":
            file = (400, 370)
        if  update.message.text == "№15" or update.message.text == "№6":
            file = (400,150)
        htmlimg.screenshot(
            html_str=html,
            css_str=css,
            save_as='my_image.png',
            size=file
        )
        image = open('images/my_image.png', 'rb')
        await update.message.reply_photo(image)
        if int(update.message.text[1:]) <= 12:
            print(answer_num)
            await update.message.reply_text(answer[:6]+"||" + " \\" +answer[7:]+"||",parse_mode='MarkdownV2')
    elif update.message.text == "№1488":
        await update.message.reply_text('ЧТООО ПАСХАЛКООО ВКЛЮЧАЕМ ВЕНТИЛЯТОРЫ!!!!!!!!!')
    else: await update.message.reply_text('Упс! Такого задания мы не нашли! Введите номер задания ещё раз: ')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Показывает клавиатуру с выбором номеров заданий"""
    reply_keyboard = [["№1", "№2", "№3", "№4", "№5"],
                       ["№6", "№7", "№8", "№9", "№10"],
                      ["№11", "№12", "№13", "№14", "№15"],
                     ["№16", "№17", "№18", "№19"]]
    await update.message.reply_text(
        "Добро пожаловать! Для начала выберите задание, \
            которое хотите отработать: ",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True,
        input_field_placeholder="Выберите номер задания: "
        ))

def main():
    """Старт бота"""
    application = Application.builder().token("TOKEN").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start_reply))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()