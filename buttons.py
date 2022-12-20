from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_start = ReplyKeyboardMarkup(resize_keyboard=True)
btn_continue = KeyboardButton('Продолжить игру')
btn_new = KeyboardButton('Новая игра')
kb_start.add(btn_continue, btn_new,KeyboardButton("Получить статистику"))

kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
kb_cancel.add(KeyboardButton('Отмена'))

kb_game_city = ReplyKeyboardMarkup(resize_keyboard=True)
btn_enter_market = KeyboardButton("Зайти в магазин")
btn_get_stat = KeyboardButton('Получить информацию')
btn_redress = KeyboardButton('Переодеться')
btn_travell = KeyboardButton("Переместиться")
btn_info_about_inventary = KeyboardButton("Получить информацию об инвентаре")
btn_end_game = KeyboardButton("Закончить игру")
kb_game_city.add(btn_enter_market, btn_get_stat,btn_info_about_inventary, btn_redress, btn_travell, btn_end_game)

kb_market = ReplyKeyboardMarkup(resize_keyboard=True)
btn_buy = KeyboardButton("Купить предметы")
btn_sell = KeyboardButton("Продать предметы")
kb_market.add(btn_buy,btn_sell,KeyboardButton('Выйти из магазина'))

kb_game_dangeon = ReplyKeyboardMarkup(resize_keyboard=True)
btn_battle = KeyboardButton("В бой")
kb_game_dangeon.add(btn_get_stat, btn_info_about_inventary,btn_travell,btn_battle,btn_end_game)

kb_battle_preparation = ReplyKeyboardMarkup(resize_keyboard=True)
btn_drink = KeyboardButton("Выпить зелье")
btn_start = KeyboardButton("Начать")
kb_battle_preparation.add(btn_drink,btn_start)

kb_attack = ReplyKeyboardMarkup(resize_keyboard=True)
btn_phys = KeyboardButton("Физическая атака")
btn_magic = KeyboardButton("Магическая атака")
kb_attack.add(btn_phys, btn_magic)


def CreateButtons(text: list) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for t in text:
        kb.add(KeyboardButton(t[0]))
    kb.add(KeyboardButton('Отмена'))
    return kb
