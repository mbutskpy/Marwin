from config import *
import logging
from keyboards import *
import sqlite3
from random import randint
from time import sleep

from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold

logging.basicConfig(level=logging.INFO)

# функции
# функция для счета всех ID (В дальнейшем для их уникальности)
def getIds():
    query = """ SELECT id FROM users """
    cursor.execute(query)
    rows = cursor.fetchall()

    l = []

    for row in rows:
        row = int(str(row).replace(",", "").replace("(", "").replace(")", "").replace("[", ""))
        l.append(row)
    return(l)

# Узнать индекс строки/числа в списке/строке
def getIndex(list: list, query):
    i = 0
    for x in list:
        if x == query:
            return(i)
        i += 1

# Найти как правильно поставить форму продукта (Чтобы все было читабельно)
def getCase(message, productP, productID, case):
    if case == "Pa":
        match getData(message.from_user.id, productP, 'toys')[-1]:
            case "1":
                productCase = products[productID]
            case "2" | "3" | "4":
                productCase = productsPa[productID]
            case "5" | "6" | "7" | "8" | "9" | "0":
                productCase = productsPaMany[productID]
        return productCase

# Найти значение в таблице
def getData(id, column, table='users'):
    query = f""" SELECT {column} FROM {table} WHERE id = {id}"""
    cursor.execute(query)
    rows = cursor.fetchall()
    row = ""
    for row in rows:
        row = str(row).replace(",", "").replace("(", "").replace(")", "").replace("[", "").replace("'", "")
    return(str(row))

# Если нет магазина, то выполняется следующая функция
async def NoShop(message: types.message):
    if message.from_user.id not in getIds():
        await message.answer(f'Попробуй себя в роли владельца магазина игрушек!', reply_markup=openM)


def event():
    chanse = randint(0, 99)
    if chanse < 30:
        return False
    else:
        return True

def get_row(result: int):
    slot_values = {
        1: ("бар", "бар", "бар"),
        2: ("виноград", "бар", "бар"),
        3: ("лимон", "бар", "бар"),
        4: ("семёрка", "бар", "бар"),
        5: ("бар", "виноград", "бар"),
        6: ("виноград", "виноград", "бар"),
        7: ("лимон", "виноград", "бар"),
        8: ("семёрка", "виноград", "бар"),
        9: ("бар", "лимон", "бар"),
        10: ("виноград", "лимон", "бар"),
        11: ("лимон", "лимон", "бар"),
        12: ("семёрка", "лимон", "бар"),
        13: ("бар", "семёрка", "бар"),
        14: ("виноград", "семёрка", "бар"),
        15: ("лимон", "семёрка", "бар"),
        16: ("семёрка", "семёрка", "бар"),
        17: ("бар", "бар", "виноград"),
        18: ("виноград", "бар", "виноград"),
        19: ("лимон", "бар", "виноград"),
        20: ("семёрка", "бар", "виноград"),
        21: ("бар", "виноград", "виноград"),
        22: ("виноград", "виноград", "виноград"),
        23: ("лимон", "виноград", "виноград"),
        24: ("семёрка", "виноград", "виноград"),
        25: ("бар", "лимон", "виноград"),
        26: ("виноград", "лимон", "виноград"),
        27: ("лимон", "лимон", "виноград"),
        28: ("семёрка", "лимон", "виноград"),
        29: ("бар", "семёрка", "виноград"),
        30: ("виноград", "семёрка", "виноград"),
        31: ("лимон", "семёрка", "виноград"),
        32: ("семёрка", "семёрка", "виноград"),
        33: ("бар", "бар", "лимон"),
        34: ("виноград", "бар", "лимон"),
        35: ("лимон", "бар", "лимон"),
        36: ("семёрка", "бар", "лимон"),
        37: ("бар", "виноград", "лимон"),
        38: ("виноград", "виноград", "лимон"),
        39: ("лимон", "виноград", "лимон"),
        40: ("семёрка", "виноград", "лимон"),
        41: ("бар", "лимон", "лимон"),
        42: ("виноград", "лимон", "лимон"),
        43: ("лимон", "лимон", "лимон"),
        44: ("семёрка", "лимон", "лимон"),
        45: ("бар", "семёрка", "лимон"),
        46: ("виноград", "семёрка", "лимон"),
        47: ("лимон", "семёрка", "лимон"),
        48: ("семёрка", "семёрка", "лимон"),
        49: ("бар", "бар", "семёрка"),
        50: ("виноград", "бар", "семёрка"),
        51: ("лимон", "бар", "семёрка"),
        52: ("семёрка", "бар", "семёрка"),
        53: ("бар", "виноград", "семёрка"),
        54: ("виноград", "виноград", "семёрка"),
        55: ("лимон", "виноград", "семёрка"),
        56: ("семёрка", "виноград", "семёрка"),
        57: ("бар", "лимон", "семёрка"),
        58: ("виноград", "лимон", "семёрка"),
        59: ("лимон", "лимон", "семёрка"),
        60: ("семёрка", "лимон", "семёрка"),
        61: ("бар", "семёрка", "семёрка"),
        62: ("виноград", "семёрка", "семёрка"),
        63: ("лимон", "семёрка", "семёрка"),
        64: ("семёрка", "семёрка", "семёрка"),
    }
    return str(', '.join(slot_values.get(result))).capitalize()

def get_casino_point(result: int):
    if result in (1, 22, 43):
        return 3
    elif result in (6, 11, 16, 17, 27, 32, 33, 38, 48, 49, 54, 59):
        return 2
    elif result == 64:
        return 5
    else:
        return -1

def get_casino_result_text(result: int, bid: int):
    result_2 = get_casino_point(result=result)
    prize = bid * result_2
    combination_text = get_row(result)

    if result_2 > 0:
        sticker = "CAACAgIAAxkBAAEKPLBk-Jtk29IweguNxsI5Owd5ZKMipwACQAADr8ZRGldV33CiNs2qMAQ"
        text = f'{hbold("Крот Перри")}:  Поздравляю! Ваша комбинация: {hbold(combination_text)}, Вы выиграли целых: {prize} рублей! Приходите к нам еще!'
    else:
        sticker = "CAACAgIAAxkBAAEKPK5k-Jsni0hvxThIRkzQ4RX5aTLiNwACPgADr8ZRGiaKo_SrpcJQMAQ"
        text = f'{hbold("Крот Перри")}:  К сожалению вы проиграли. Ваша комбинация: {hbold(combination_text)}, Не расстраивайтесь и приходите к нам еще!'
    return [sticker, text]


# Регистрация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Рег БД
db = sqlite3.connect("db/db.db")
cursor = db.cursor()

products = ["набор LEGO дом", "набор LEGO майнкрафт", "Монополия", "UNO", "Имаджинариум", "Манчкин", "Акула плюшевая", "Авокадо плюшевое", "Покемон конструктор"] # Все игрушки (и. п.)
productsP = ["LegoHouse", "LegoMine", "Monopoly", "UNO", "Imaginarium", "Manchkin", "Shark", "Avokado", "Pokemon"] # Как записаны игрушки в БД
productsPa =  ["набора LEGO дом", "набора LEGO майнкрафт", "Монополии", "UNO", "Имаджинариума", "Манчкина", "Акулы плюшевой", "Авокадо плюшевого", "Покемон конструктора"] # Все игрушки (р. п.)
productsPaMany =  ["наборов LEGO дом", "наборов LEGO майнкрафт", "Монополий", "UNO", "Имаджинариумов", "Манчкинов", "Акул плюшевых", "Авокадо плюшевых", "Покемон конструкторов"] # Все игрушки (р. п., мн.ч.)
productsAc = ["набор LEGO дом", "набор LEGO майнкрафт", "Монополию", "UNO", "Имаджинариум", "Манчкин", "Акулу плюшевую", "Авокадо плюшевое", "Покемон конструктор"] # Все игрушки (в. п.)

res = ["коробка", "пластик", "бумага", "ткань", "холофайбер"]
resP = ["box", "plastic", "paper", "textile", "holofiber"]
resAc = ["коробку", "пластик", "бумагу", "ткань", "холофайбер"]

# При запуске бота
@dp.message_handler(commands="start")
async def start(message: types.Message):
    if message.from_user.id not in getIds():
        await NoShop(message)
    else:
        if credit(message.from_user.id):
            commands = int(getData(message.from_user.id, "commands"))
            query = f" UPDATE users SET commands = {commands + 1} WHERE id={message.from_user.id} "
            cursor.execute(query)
            db.commit()
            if commands == 6:
                await debt(message.from_user.id)
        await info(message)

# Открытие магазина
@dp.callback_query_handler(text="open")
async def open(callback: types.CallbackQuery):
    query1 = f"INSERT INTO users (id) VALUES ({callback.from_user.id})"
    cursor.execute(query1)
    db.commit()
    query2 = f"INSERT INTO toys (id) VALUES ({callback.from_user.id})"
    cursor.execute(query2)
    db.commit()
    query3 = f"INSERT INTO offer (id) VALUES ({callback.from_user.id})"
    cursor.execute(query3)
    db.commit()
    query3 = f"INSERT INTO res (id) VALUES ({callback.from_user.id})"
    cursor.execute(query3)
    db.commit()

    await bot.send_message(callback.message.chat.id, f"Поздравляем, Вы открыли магазин игрушек!", reply_markup=learnM)
    await bot.delete_message(callback.message.chat.id, callback.message.message_id)

def credit(id):
    commands = getData(id, "commands")
    if commands == "None":
        return False
    else:
        return True

async def debt(id):
    money = int(getData(id, "money"))
    credit_money = int(getData(id, "credit")) * 0.25 + int(getData(id, "credit"))
    query = f" UPDATE users SET commands = NULL, credit = NULL, money = {money - credit_money} WHERE id={id} "
    cursor.execute(query)
    db.commit()

    await bot.send_sticker(id, "CAACAgIAAxkBAAEKQuNk_ZUnCpJTV1R4XQzwdTx153Fq1AACTgADWbv8JQ3rz9n50HgqMAQ")
    await bot.send_message(id, f"{hbold('Кот Альберт')}: Я предупреждал, но ты меня не слушаешь! Ты использовал 7 команд, и не отдал долг! Ты теперь уходишь в минус! Даю совет, бери еще кредит, и закупайся материалами. Делай игрушки и продавай их! Тогда получишь денег и уйдешь хотя бы в ноль! До свидания, я пошел к другим задолженникам.", "HTML")

# информация о магазине
@dp.message_handler(commands="info")
async def info(message: types.Message):
    id = message.from_user.id
    if id not in getIds():
        await NoShop(message)
    else:
        if credit(id):
            commands = int(getData(id, "commands"))
            query = f" UPDATE users SET commands = {commands + 1} WHERE id={id} "
            cursor.execute(query)
            db.commit()
            if commands == 6:
                await debt(id)
        priceK = ""
        match getData(id, 'money')[-1]:
            case "1":
                priceK = "рубль"
            case "2" | "3" | "4":
                priceK = "рубля"
            case "5" | "6" | "7" | "8" | "9" | "0":
                 priceK = "рублей"
        creditT = ""
        if getData(id, "credit") != "None":
            creditT = ("Информация о кредите:\n"
                        f"  Кол-во денег взятых в кредит {getData(id, 'credit')}\n"
                        f"  Кол-во использованных команд: {getData(id, 'commands')}\n")
        
        await message.answer("Ваш магазин:\n"
                            f"Баланс: {getData(id, 'money')} {priceK}\n"
                            f"Кол-во выполненных заказов: {getData(id, 'offers')}\n"
                            f"{creditT}"
                            f"Ресурсы в наличии:\n"
                                f"  Коробки: {getData(id, 'box', 'res')}\n"
                                f"  Пластик: {getData(id, 'plastic', 'res')}\n"
                                f"  Бумага: {getData(id, 'paper', 'res')}\n"
                                f"  Ткань: {getData(id, 'textile', 'res')}\n"
                                f"  Холофайбер: {getData(id, 'holofiber', 'res')}\n"
                            f"Игрушки в наличи:\n"
                                f"  Набор LEGO дом: {getData(id, 'LegoHouse', 'toys')},\n"
                                f"  набор LEGO майнкрафт: {getData(id, 'LegoMine', 'toys')},\n"
                                f"  Монополия: {getData(id, 'Monopoly', 'toys')},\n"
                                f"  UNO: {getData(id, 'UNO', 'toys')},\n"
                                f"  Имаджинариум: {getData(id, 'Imaginarium', 'toys')},\n"
                                f"  Манчкин: {getData(id, 'Manchkin', 'toys')},\n"
                                f"  Акула плюшевая: {getData(id, 'Shark', 'toys')},\n"
                                f"  Авокадо плюшевое: {getData(id, 'Avokado', 'toys')},\n"
                                f"  Покемон конструктор: {getData(id, 'Pokemon', 'toys')}")

# Прийти на кассу
@dp.message_handler(commands="store")
async def shop(message: types.Message):
    if message.from_user.id not in getIds():
        await NoShop(message)
    else:
        if credit(message.from_user.id):
            commands = int(getData(message.from_user.id, "commands"))
            query = f" UPDATE users SET commands = {commands + 1} WHERE id={message.from_user.id} "
            cursor.execute(query)
            db.commit()
            if commands == 6:
                await debt(message.from_user.id)
        # Выбор заказчика, цены, продукта
        buyerN = randint(1, 3)
        price = randint(25, 30)
        productID = randint(0, 8)
        buyer = ""
        buyerS = ""
        var = ""
        priceK = ""
        varN = randint(1, 3)

        # Если ты только начал, приходит поставщик
        if getData(message.from_user.id, "offers") == "0":
            buyerN = 4
            price = 0
            varN = 4
            productID = 2
            query1 = f" UPDATE toys SET LegoHouse = 30, LegoMine = 30, Monopoly = 30, UNO = 30, Imaginarium = 30, Manchkin = 30, Shark = 30, Avokado = 30, Pokemon = 30 WHERE id={message.from_user.id} "
            cursor.execute(query1)
            db.commit()
            query2 = f" UPDATE res SET box = 50, plastic = 50, paper = 50, textile = 50, holofiber = 50 WHERE id={message.from_user.id} "
            cursor.execute(query2)
            db.commit()
        # запись заказа в БД (чтобы покупатель ждал, пока ему не дадут заказ)
        if getData(message.from_user.id, "buyer", "offer") == "None":
            query = f" UPDATE offer SET buyer = '{buyerN}', price = {price}, product = {productID} WHERE id={message.from_user.id} "
            cursor.execute(query)
            db.commit()
        # Если пользователь приходит во 2 раз, чтобы покупатель, цена, товар остались прежними
        else:
            buyerN = int(getData(message.from_user.id, 'buyer', 'offer'))
            price = int(getData(message.from_user.id, 'price', 'offer'))
            productID = int(getData(message.from_user.id, 'product', 'offer'))
        priceBold = hbold(price)
        #  Выбор продавца зная его ID
        match buyerN:
            case 1:
                buyer = "Медведь Брус"
                buyerS = "CAACAgIAAxkBAAEJzNxkvoYkRJs7a9tsTSV6IB4Zf4WRpQACHQADO3EfIqmCmmAwV9EZLwQ"
            case 2:
                buyer = "Лис Фред"
                buyerS = "CAACAgIAAxkBAAEJzNZkvoVBsBr4ZhxShZfByeVpPtNV1wACxgoAAhf-gUojb09iakYCMC8E"
            case 3:
                buyer = "Лягушенок Пепе"
                buyerS = "CAACAgIAAxkBAAEJzN5kvojdVdYRb08NyuX9gCNKB4sddAACdhoAAnO4KEliRUylvMokHC8E"
            case 4:
                buyer = "Таинственный сыч Пол"
                buyerS = "CAACAgIAAxkBAAEJ1Qhkwsq4dgw69zPo2wH3vw2rfJ1zMwACIwADwZxgDJDk7nBqLVflLwQ"
        productP = productsP[productID]
        # Выбор формы слова "рубль"
        match str(price)[-1]:
            case "1":
                priceK = "рубль"
            case "2" | "3" | "4":
                priceK = "рубля"
            case "5" | "6" | "7" | "8" | "9" | "0":
                priceK = "рублей"
        # Выбор вариации запроса
        varK = hbold(productsAc[productID])
        match varN:
            case 1:
                var = f"Можно у вас купить {varK} за {priceBold} {priceK}?"
            case 2:
                var = f"Пожалуйста, дайте мне {varK}, а я вам дам {priceBold} {priceK}"
            case 3:
                var = f"Я хочу {varK} за {priceBold} {priceK}"
            case 4:
                var = f"Здравствуй, я поставщик Марвина. В честь твоего открытия даю тебе всех игрушек по 30 штук, а материалов по 50. Кстати, по традиции я должен у тебя что-то заказать. Дай мне {hbold('Монополию')}"
        
        await message.answer_sticker(buyerS)
        await message.answer(f"К вам в магазин пришел {hbold(buyer)}", parse_mode="HTML")
        await message.answer(f"{hbold(buyer)}: {var}", parse_mode="HTML", reply_markup=sell(message, productP, productID))

@dp.message_handler(commands="shop")
async def shop(message: types.Message):
    if credit(message.from_user.id):
            commands = int(getData(message.from_user.id, "commands"))
            query = f" UPDATE users SET commands = {commands + 1} WHERE id={message.from_user.id} "
            cursor.execute(query)
            db.commit()
            if commands == 6:
                await debt(message.from_user.id)
    await message.answer_sticker("CAACAgIAAxkBAAEJ2upkxjB1ly9dsoVongqI8PefJjDg-QACSAEAAiI3jgT92_aVA0dULi8E")
    await message.answer(f"{hbold('Тукан Хэл')}: Привет! Ты хочешь у меня что-то купить? Не стесняйся, подходи! Тут самый большой выбор ресурсов в городе! Все по 15 рублей!", reply_markup=shopM, parse_mode="HTML")

# Когда заказ выполнен/нет на складе предмета, начинается эта функция
@dp.callback_query_handler(text="sellF")
async def sellF(callback: types.CallbackQuery):
    productID = int(getData(callback.from_user.id, 'product', 'offer'))
    product = products[productID]
    if int(getData(callback.from_user.id, productsP[productID], "toys")) >= 1:
        buyerN = int(getData(callback.from_user.id, 'buyer', 'offer'))
        buyer = ""
        buyerS = ""
        price = int(getData(callback.from_user.id, 'price', 'offer'))
        match buyerN:
            case 1:
                buyer = "Медведь Брус"
                buyerS = "CAACAgIAAxkBAAEJ1Gxkwotd5x396y99V0QKuBZTRF244AACGQADO3EfIq1YxrN77D_JLwQ"
            case 2:
                buyer = "Лис Фред"
                buyerS = "CAACAgIAAxkBAAEJ1HVkwoz3Zl4wtApRQznoKZEkR6lV8gAClw0AAoOQeUqKysE-Ow0_uS8E"
            case 3:
                buyer = "Лягушенок Пепе"
                buyerS = "CAACAgIAAxkBAAEJ1Hdkwo0YIgky9A-HJMfMAAHmP-Liaj8AAnIXAALQYvFIKvQVHCNEEmEvBA"
            case 4:
                buyer = "Таинственный сыч Пол"
                buyerS = "CAACAgIAAxkBAAEJ1Qhkwsq4dgw69zPo2wH3vw2rfJ1zMwACIwADwZxgDJDk7nBqLVflLwQ"
        match str(price)[-1]:
            case "1":
                priceK = "рубль"
            case "2" | "3" | "4":
                priceK = "рубля"
            case "5" | "6" | "7" | "8" | "9" | "0":
                priceK = "рублей"
        # Удаление заказа из БД
        query1 = f" UPDATE offer SET buyer = NULL, price = NULL, product = NULL WHERE id={callback.from_user.id} "
        cursor.execute(query1)
        db.commit()
        # начисление денег, +1 выполненный заказ
        query2 = f" UPDATE users SET money = {int(getData(callback.from_user.id, 'money')) + price}, offers = {int(getData(callback.from_user.id, 'offers')) + 1} WHERE id={callback.from_user.id} "
        cursor.execute(query2)
        db.commit()
        # Забрать игрушку
        query3 = f" UPDATE toys SET {productsP[productID]} = {int(getData(callback.from_user.id, productsP[productID], 'toys')) - 1} WHERE id={callback.from_user.id} "
        cursor.execute(query3)
        db.commit()
        # Уведомление пользователя о том, что его заказ купили
        await bot.send_sticker(callback.from_user.id, buyerS)
        await bot.send_message(callback.from_user.id, f"{buyer} купил у Вас {product} заплатив {price} {priceK}")
        await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        await bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        await bot.delete_message(callback.message.chat.id, callback.message.message_id - 2)
    else:
        # Уведомление пользователя о том, что у него нет игрушки
        await callback.answer(f"У Вас нет {productsPa[productID]} :(", True)

# Скрафтить (сделать) игрушку
@dp.message_handler(commands="craft")
async def craft(message: types.Message):
    if credit(message.from_user.id):
            commands = int(getData(message.from_user.id, "commands"))
            query = f" UPDATE users SET commands = {commands + 1} WHERE id={message.from_user.id} "
            cursor.execute(query)
            db.commit()
            if commands == 6:
                await debt(message.from_user.id)
    await message.answer_sticker("CAACAgIAAxkBAAEKWKNlCxL0KmnnKmFL7BtWE7adErIBnAACDgADr8ZRGrdbgux-ASf3MAQ")
    await message.answer(f"{hbold('Хомяк Фома')}: Здравствуй! С тебя ресурсы, с меня игрушки. Что приобрести хочешь?", reply_markup=craftM, parse_mode="HTML")

@dp.callback_query_handler(text="recepts")
async def recepts(callback: types.CallbackQuery):
    await bot.send_sticker(callback.from_user.id, "CAACAgIAAxkBAAEKWLxlCyTno3skdnAbzVPxP786_eYMAwACBQADr8ZRGpWJICJ8NGY0MAQ")
    await bot.send_message(callback.message.chat.id, f"{hbold('Хомяк Фома')}:\n"
                           f"{hbold('Конструкторы и LEGO')}: 1 коробка, 8 пластика\n"
                           f"{hbold('Настольные игры')}: 1 коробка, 7 бумаги\n"
                           f"{hbold('Мягкие игрушки')}: 9 ткани, 6 холофайбера", parse_mode="HTML")

# Крафт конструкторов и LEGO
@dp.callback_query_handler(text=["LegoHouse", "LegoMine", "Pokemon"])
async def craftConstruct(callback: types.CallbackQuery):
    if int(getData(callback.from_user.id, "box", "res")) >= 1 and int(getData(callback.from_user.id, "plastic", "res")) >= 8:
        # Забрать материалы
        query1 = f" UPDATE res SET box = {int(getData(callback.from_user.id, 'box', 'res')) - 1}, plastic = {int(getData(callback.from_user.id, 'plastic', 'res')) - 8} WHERE id={callback.from_user.id} "
        cursor.execute(query1)
        db.commit()
        if event():
            # Отдать игрушку
            query2 = f" UPDATE toys SET {callback.data} = {int(getData(callback.from_user.id, callback.data, 'toys')) + 1} WHERE id={callback.from_user.id} "
            cursor.execute(query2)
            db.commit()
            # Уведомление пользователя о том, что он успешно сделал игрушку
            productID = getIndex(productsP, callback.data)
            await bot.send_sticker(callback.from_user.id, "CAACAgIAAxkBAAEKWKVlCxMAActdesIOUDuBi8iyqrWrSVUAAgYAA6_GURqezu74W6n9-jAE")
            await bot.send_message(callback.from_user.id, f"{hbold('Хомяк Фома')}: Я тебе сделал {productsAc[productID]}. Держи!", "HTML")
        else:
            await bot.send_sticker(callback.from_user.id, "CAACAgIAAxkBAAEKWLNlCxWfoQhAhrxvUivk-DT_rQABoYwAAggAA6_GURqn8hvy_oHklzAE")
            await bot.send_message(callback.from_user.id, f"{hbold('Хомяк Фома')}: Ты мне ресурсы бракованные дал. У меня не получилось ничего сделать", "HTML")
    else:
        # Уведомление пользователя о том, что у него нет игрушки
        await bot.send_sticker(callback.from_user.id, "CAACAgIAAxkBAAEKWKdlCxME_K2aFw6BlRZ5ijNKVsx_CAACAQADr8ZRGhLj3-N0EyK_MAQ")
        await bot.send_message(callback.from_user.id, f"{hbold('Хомяк Фома')}: Мне ресурсы нужны, чтобы игрушки делать. У Хэла купи их. (/shop)", "HTML")

# Крафт настольных игр
@dp.callback_query_handler(text=["Monopoly", "UNO", "Imaginarium", "Manchkin"])
async def craftGames(callback: types.CallbackQuery):
    if int(getData(callback.from_user.id, "box", "res")) >= 1 and int(getData(callback.from_user.id, "paper", "res")) >= 7:
        # Забрать материалы
        query1 = f" UPDATE res SET box = {int(getData(callback.from_user.id, 'box', 'res')) - 1}, paper = {int(getData(callback.from_user.id, 'holofiber', 'res')) - 7} WHERE id={callback.from_user.id} "
        cursor.execute(query1)
        db.commit()
        if event():
            # Отдать игрушку
            query2 = f" UPDATE toys SET {callback.data} = {int(getData(callback.from_user.id, callback.data, 'toys')) + 1} WHERE id={callback.from_user.id} "
            cursor.execute(query2)
            db.commit()
            # Уведомление пользователя о том, что он успешно сделал игрушку
            productID = getIndex(productsP, callback.data)
            await bot.send_sticker(callback.from_user.id, "CAACAgIAAxkBAAEKWKVlCxMAActdesIOUDuBi8iyqrWrSVUAAgYAA6_GURqezu74W6n9-jAE")
            await bot.send_message(callback.from_user.id, f"{hbold('Хомяк Фома')}: Я тебе сделал {productsAc[productID]}. Держи!", "HTML")
        else:
            await bot.send_sticker(callback.from_user.id, "CAACAgIAAxkBAAEKWLNlCxWfoQhAhrxvUivk-DT_rQABoYwAAggAA6_GURqn8hvy_oHklzAE")
            await bot.send_message(callback.from_user.id, f"{hbold('Хомяк Фома')}: Ты мне ресурсы бракованные дал. У меня не получилось ничего сделать", "HTML")
    else:
        # Уведомление пользователя о том, что у него нет игрушки
        await bot.send_sticker(callback.from_user.id, "CAACAgIAAxkBAAEKWKdlCxME_K2aFw6BlRZ5ijNKVsx_CAACAQADr8ZRGhLj3-N0EyK_MAQ")
        await bot.send_message(callback.from_user.id, f"{hbold('Хомяк Фома')}: Мне ресурсы нужны, чтобы игрушки делать. У Хэла купи их. (/shop)", "HTML")

# Крафт мягких игрушек
@dp.callback_query_handler(text=["Shark", "Avokado"])
async def craftToys(callback: types.CallbackQuery):
    if int(getData(callback.from_user.id, "textile", "res")) >= 9 and int(getData(callback.from_user.id, "holofiber", "res")) >= 6:
        # Забрать материалы
        query1 = f" UPDATE res SET textile = {int(getData(callback.from_user.id, 'textile', 'res')) - 9}, holofiber = {int(getData(callback.from_user.id, 'holofiber', 'res')) - 6} WHERE id={callback.from_user.id} "
        cursor.execute(query1)
        db.commit()
        if event():
            # Отдать игрушку
            query2 = f" UPDATE toys SET {callback.data} = {int(getData(callback.from_user.id, callback.data, 'toys')) + 1} WHERE id={callback.from_user.id} "
            cursor.execute(query2)
            db.commit()
            # Уведомление пользователя о том, что он успешно сделал игрушку
            productID = getIndex(productsP, callback.data)
            await bot.send_sticker(callback.from_user.id, "CAACAgIAAxkBAAEKWKVlCxMAActdesIOUDuBi8iyqrWrSVUAAgYAA6_GURqezu74W6n9-jAE")
            await bot.send_message(callback.from_user.id, f"{hbold('Хомяк Фома')}: Я тебе сделал {productsAc[productID]}. Держи!", "HTML")
        else:
            await bot.send_sticker(callback.from_user.id, "CAACAgIAAxkBAAEKWLNlCxWfoQhAhrxvUivk-DT_rQABoYwAAggAA6_GURqn8hvy_oHklzAE")
            await bot.send_message(callback.from_user.id, f"{hbold('Хомяк Фома')}: Ты мне ресурсы бракованные дал. У меня не получилось ничего сделать", "HTML")
    else:
        # Уведомление пользователя о том, что у него нет игрушки
        await bot.send_sticker(callback.from_user.id, "CAACAgIAAxkBAAEKWKdlCxME_K2aFw6BlRZ5ijNKVsx_CAACAQADr8ZRGhLj3-N0EyK_MAQ")
        await bot.send_message(callback.from_user.id, f"{hbold('Хомяк Фома')}: Мне ресурсы нужны, чтобы игрушки делать. У Хэла купи их. (/shop)", "HTML")


# Покупка ресурсов
@dp.callback_query_handler(text=["box", "paper", "plastic", "textile", "holofiber"])
async def buy(callback: types.CallbackQuery):
    if int(getData(callback.from_user.id, "money")) >= 20:
        # Отдать ресурс
        query1 = f" UPDATE res SET {callback.data} = {int(getData(callback.from_user.id, callback.data, 'res')) + 1} WHERE id={callback.from_user.id} "
        cursor.execute(query1)
        db.commit()
        # Забрать деньги
        query2 = f" UPDATE users SET money = {int(getData(callback.from_user.id, 'money')) - 15}"
        cursor.execute(query2)
        db.commit()
        # Уведомление пользователя о том, что он успешно сделал игрушку
        resID= getIndex(resP, callback.data)
        await bot.send_message(callback.from_user.id, f"Вы купили {resAc[resID]}!")
    else:
        # Уведомление пользователя о том, что у него нет игрушки
        await callback.answer(f"У Вас не хватает денег :(", True)


@dp.message_handler(commands='bank')
async def bank(message: types.Message):
    if getData(message.from_user.id, "commands") == "None":
        if credit(message.from_user.id):
            commands = int(getData(message.from_user.id, "commands"))
            query = f" UPDATE users SET commands = {commands + 1} WHERE id={message.from_user.id} "
            cursor.execute(query)
            db.commit()
            if commands == 6:
                await debt(message.from_user.id)
        await message.answer_sticker('CAACAgIAAxkBAAEKQjlk_LBeTl28mZOwbbC5SmkpQpp71QACSgADWbv8JZ3yyYHsNyFgMAQ')
        await message.answer(f"{hbold('Кот Альберт')}: Привет! Пришел кредит брать? Очередной бедолага, который все деньги у Перри потерял? Или обанкротился на игрушках? А может берешь кредит, чтобы погасить другой? Ладно, не расстраивайся, у нас всего лишь 15% лишних отдавать надо. Запомни: ты должен воспользоваться 7 командами перед тем, как отдашь кредит (/bank тоже считается), не успеешь - уйшдешь в минус, да еще и прогоришь не в 15%, а в 25%! Используй команды с умом! Сколько возьмешь?", "HTML", reply_markup=creditM)
    else:
        credit_money = int(getData(message.from_user.id, "credit"))
        await message.answer_sticker('CAACAgIAAxkBAAEKQjlk_LBeTl28mZOwbbC5SmkpQpp71QACSgADWbv8JZ3yyYHsNyFgMAQ')
        await message.answer(f"{hbold('Кот Альберт')}: Такс, ты у нас {message.from_user.full_name}. Кредит отдавать пришел? ", "HTML", reply_markup=Givecredit(credit_money))
    
# Покупка ресурсов
@dp.callback_query_handler(text=["giveCredit"])
async def buy(callback: types.CallbackQuery):
    money = int(getData(callback.from_user.id, "money"))
    credit_money = int(getData(callback.from_user.id, "credit")) * 0.15 + int(getData(callback.from_user.id, "credit"))
    if money >= credit_money:
        query = f" UPDATE users SET commands = NULL, credit = NULL, money = {money - credit_money} WHERE id={callback.from_user.id} "
        cursor.execute(query)
        db.commit()
        await bot.send_sticker(callback.from_user.id,'CAACAgIAAxkBAAEKQuVk_ZUzcqk2pw8QJ6LOrRvjRx3BYwACQgADWbv8Jd7Bb6A7P1vRMAQ')
        await bot.send_message(callback.from_user.id, f"{hbold('Кот Альберт')}: Отлично! Приятно с Вами иметь дело!", "HTML")
    else:
        await bot.send_sticker(callback.from_user.id, "CAACAgIAAxkBAAEKSVhlAarWUyKHUt6R6TQhlMwubr-1QgACPQADWbv8JZ0Sd-63akBlMAQ")
        await bot.send_message(callback.from_user.id, f"{hbold('Кот Альберт')}: Ха-Ха. Извини, мне смешно просто. Ты сказал, что сейчас дашь деньги, а их у тебя нет! Ладно тебе. Ищи деньги и возвращайся.", "HTML")


@dp.message_handler(commands='casino')
async def casino(message: types.Message):
    if credit(message.from_user.id):
            commands = int(getData(message.from_user.id, "commands"))
            query = f" UPDATE users SET commands = {commands + 1} WHERE id={message.from_user.id} "
            cursor.execute(query)
            db.commit()
            if commands == 6:
                await debt(message.from_user.id)
    await message.answer_sticker("CAACAgIAAxkBAAEKOpZk90bdyXB_N24I2ET8d8o8fiaW8gACTAADr8ZRGjrfxZE8LKM_MAQ")
    await message.answer(f"{hbold('Крот Перри')}: Здравствуй! Я работник казино! Раз ты пришел сюда, то ты азартный игрок! Ладно, хватит бессмысленных разгворов! Сколько денег вывалишь?", "HTML", reply_markup=casinoM)


@dp.callback_query_handler()
async def casinoGameOrCredit(callback: types.CallbackQuery):
    if callback.data[-1] == "C":
        money = int(getData(callback.from_user.id, "money"))
        credit_money = int(callback.data.replace("rC", ""))
        await bot.send_sticker(callback.message.chat.id, "CAACAgIAAxkBAAEKQuVk_ZUzcqk2pw8QJ6LOrRvjRx3BYwACQgADWbv8Jd7Bb6A7P1vRMAQ")
        await bot.send_message(callback.message.chat.id, f"{hbold('Кот Альберт')}: Все, вижу, Вы взяли {credit_money} рублей. У Вас 7 команд.", "HTML")
        query = f" UPDATE users SET commands = 0, money = {money + credit_money}, credit = {credit_money} WHERE id={callback.from_user.id}"
        cursor.execute(query)
        db.commit()
    else:
        bid = int((callback.data).replace('r', ''))
        if int(getData(callback.from_user.id, "money")) >= bid:
            result = await bot.send_dice(callback.message.chat.id, emoji="🎰")
            result_text = get_casino_result_text(result.dice.value, bid)
            point = get_casino_point(result.dice.value)
            sleep(3)
            await bot.send_sticker(callback.message.chat.id, result_text[0])
            await bot.send_message(callback.message.chat.id, result_text[1], "HTML")
            new_money = bid * point
            bid_if_win = 0
            if point > 0:
                bid_if_win = bid
            query = f" UPDATE users SET money = {int(getData(callback.from_user.id, 'money')) + new_money - bid_if_win} WHERE id={callback.from_user.id} "
            cursor.execute(query)
            db.commit()
        else:
            await bot.send_sticker(callback.message.chat.id, 'CAACAgIAAxkBAAEKQUlk_G040ndAcA5zi8pIdiUrDpPXEwACVAADr8ZRGpZSYx-oAwNGMAQ')
            await bot.send_message(callback.from_user.id, f"{hbold('Крот Перри')}: Ты меня обмануть пытаешься? Я же вижу, что денег у тебя нет! Проваливай!", "HTML")

# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)