from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from main import getData, getCase, getIndex, productsP, products, res, resP
openB = InlineKeyboardButton('Открыть франшизу магазина игрушек "Марвин"', callback_data="open")

openM = InlineKeyboardMarkup()
openM.add(openB)

learnB = InlineKeyboardButton('Пройти обучение', url="https://telegra.ph/Igrovoj-bot-Marvin-obuchenie-07-24-2")

learnM = InlineKeyboardMarkup()
learnM.add(learnB)

def sell(message, productP, productID):
    sellB = InlineKeyboardButton(f"У Вас есть {getData(message.from_user.id, productP, 'toys')} {getCase(message, productP, productID, 'Pa')}", callback_data="sellF")
    sellM = InlineKeyboardMarkup()
    sellM.add(sellB)
    return sellM

productBs1 = []
productBs2 = []
productBs3 = []
productBs4 = []
receptsB = InlineKeyboardButton("Рецепты", callback_data="recepts")
craftM = InlineKeyboardMarkup(row_width=2)
i = 0
for k in products:
    i += 1
    productP = productsP[getIndex(products, k)]
    productB = InlineKeyboardButton(k, callback_data=productP)
    if i <= 2:
        productBs1.append(productB)
    elif i <= 5:
        productBs2.append(productB)
    elif i <= 7:
        productBs3.append(productB)
    else:
        productBs4.append(productB)

craftM.row(*productBs1)
craftM.row(*productBs2)
craftM.row(*productBs3)
craftM.row(*productBs4)
craftM.add(receptsB)


resBs1 = []
resBs2 = []
shopM = InlineKeyboardMarkup(row_width=2)
iR = 0
for k in res:
    iR += 1
    resP1 = resP[getIndex(res, k)]
    resB = InlineKeyboardButton(k, callback_data=resP1)
    if iR <= 2:
        resBs1.append(resB)
    elif iR <= 5:
        resBs2.append(resB)
shopM.row(*resBs1)
shopM.row(*resBs2)

r100B = InlineKeyboardButton('100 рублей', callback_data="100r")

r200B = InlineKeyboardButton('200 рублей', callback_data="200r")

r500B = InlineKeyboardButton('500 рублей', callback_data="500r")

casinoM = InlineKeyboardMarkup()
casinoM.add(r100B, r200B, r500B)

r100 = InlineKeyboardButton('100 рублей', callback_data="100rC")

r200 = InlineKeyboardButton('200 рублей', callback_data="200rC")

r500 = InlineKeyboardButton('500 рублей', callback_data="500rC")

creditM = InlineKeyboardMarkup()
creditM.add(r100, r200, r500)


def Givecredit(credit_money):
    credit_money = int(credit_money * 0.15 + credit_money)
    GivecreditB = InlineKeyboardButton(f'Отдать кредит в размере {credit_money} рублей', callback_data="giveCredit")
    GivecreditM = InlineKeyboardMarkup()
    GivecreditM.add(GivecreditB)
    return GivecreditM