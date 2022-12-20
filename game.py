from create_bot import bot, dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types
from database import *
from buttons import *
from asyncio import sleep
from random import choice

class FSMContinueGame(StatesGroup):
    choose_session = State()


class FSMNewGame(StatesGroup):
    create_person = State()


class FSMGame(StatesGroup):
    game = State()
    market = State()
    choose_item_to_buy = State()
    choose_item_to_sell = State()
    choose_location = State()
    moving = State()
    redress = State()
    battle_preparation = State()
    battle = State()


def Convert(status: bool)->str:
    if status:
        return "надета"
    return "можно надеть"

@dp.message_handler(Text("Получить статистику"))
async def statistica(message: types.Message):
    stata = GetStat(str(message.from_user.id))
    await message.answer("Статистика ваших персонажей")
    for st in stata:
        await message.answer(f"Имя: {st[1]}\nКоличество побед: {st[2]}\nКоличество проигрышей: {st[3]}\nУровень: {st[4]}",reply_markup=kb_start)

@dp.message_handler(Text('Продолжить игру'))
async def ContinueGame(message: types.Message):
    sessions = GetOldSessions(str(message.from_user.id))
    if len(sessions) == 0:
        await message.answer("Пока нету игровых сессий, но давайте начнем "
                             "новую игру!", reply_markup=kb_start)
    else:
        await message.answer("Выберите своего персонажа",
                             reply_markup=CreateButtons(
                                 sessions))
        await FSMContinueGame.choose_session.set()


@dp.message_handler(state=FSMContinueGame.choose_session)
async def ChoosePerson(message: types.Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await state.finish()
        await message.answer("Процесс выбора персонажа отменен",
                             reply_markup=kb_start)
    elif (message.text,) not in GetOldSessions(str(message.from_user.id)):
        await message.answer("Это не ваш персонаж! Выберете своего!",
                             reply_markup=CreateButtons(
                                 GetOldSessions(str(message.from_user.id))))
    else:

        await state.finish()
        StartSession(str(message.from_user.id), message.text)
        await FSMGame.game.set()
        location_type = GetTypeOfLocation(str(message.from_user.id))
        if location_type == 'город':
            await message.answer(
                f"Вы продолжаете играть за {message.text}. Хорошей игры!",
                reply_markup=kb_game_city)
        else:
            await message.answer(
                f"Вы продолжаете играть за {message.text}. Хорошей игры!",
                reply_markup=kb_game_dangeon)


@dp.message_handler(Text('Новая игра'))
async def NewGame(message: types.Message):
    await message.answer('Придумайте имя своему персонажу!',
                         reply_markup=kb_cancel)
    await FSMNewGame.create_person.set()


@dp.message_handler(state=FSMNewGame.create_person)
async def CreatePerson(message: types.Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await state.finish()
        await message.answer("Процесс создания персонажа отменен",
                             reply_markup=kb_start)
    elif IsPersonExist(str(message.from_user.id), message.text):
        await message.answer(
            "У вас уже есть такой персонаж. Придумайте новое имя",
            reply_markup=kb_cancel)
    else:
        CreatePersonage(str(message.from_user.id), message.text)
        NewPersonToStatistic(str(message.from_user.id))
        await state.finish()
        await FSMGame.game.set()
        await message.answer(
            f"Персонаж успешно создан!\nТеперь вы играете за {message.text}. Хорошей игры!",
            reply_markup=kb_game_city)


@dp.message_handler(Text("Зайти в магазин"), state=FSMGame.game)
async def GoToMarket(message: types.Message):
    # items_in_market = GetItemsInMarket(str(message.from_user.id))
    # print(items_in_market)
    await FSMGame.market.set()
    await message.answer(f"У вас {GetMoney(str(message.from_user.id))} рупий")
    await message.answer("Что вы хотите сделать",
                         reply_markup=kb_market)


@dp.message_handler(Text("Продать предметы"), state=FSMGame.market)
async def ChooseItemToSell(message: types.Message):
    items_in_inventory = GetItemsInInventory(str(message.from_user.id))
    if len(items_in_inventory) == 0:
        await message.answer(
            "Пока нету предметов в инвентаре,поэтому нечего продавать,но вы можете их купить в любом городе",
            reply_markup=kb_game_city)
        await FSMGame.game.set()
        return
    counter = 1
    for it in items_in_inventory:
        if not it[-1]:
            item = GetItem(it[2])
            await message.answer(
                f"{counter}. Имя предмета: {item[0]}\nЦена: {item[1]}\nЦена Продажи: {item[2]}\nТип предмета: {item[3]}\nДоп HP: {item[4]}\nДоп Mana: {item[5]}\nДоп Атака: {item[6]}\nДоп Магическая атака: {item[7]}\nДоп Брон: {item[8]}\nДоп Магическая броня: {item[9]}\nНеобходимый уровень: {item[10]}\nКоличество: {it[3]}", )
        counter += 1
    await message.answer("Напишите номер товара, который вы хотите продать",
                         reply_markup=kb_cancel)
    await FSMGame.choose_item_to_sell.set()


@dp.message_handler(state=FSMGame.choose_item_to_sell)
async def Sell(message: types.Message):
    if message.text.lower() == 'отмена':
        await message.answer("Процесс покупки отменен",
                             reply_markup=kb_game_city)
        await FSMGame.game.set()
        return
    num: int
    items_in_inventory = GetItemsInInventory(str(message.from_user.id))
    try:
        num = int(message.text)
    except ValueError:
        await message.answer("Вы ввели неправильный формат номера")
        counter = 1
        for it in items_in_inventory:
            item = GetItem(it[2])
            await message.answer(
                f"{counter}. Имя предмета: {item[0]}\nЦена: {item[1]}\nЦена Продажи: {item[2]}\nТип предмета: {item[3]}\nДоп HP: {item[4]}\nДоп Mana: {item[5]}\nДоп Атака: {item[6]}\nДоп Магическая атака: {item[7]}\nДоп Брон: {item[8]}\nДоп Магическая броня: {item[9]}\nНеобходимый уровень: {item[10]}\nКоличество: {it[3]}", )
            counter += 1
        await message.answer(
            "Напишите номер товара, который вы хотите продать",
            reply_markup=kb_cancel)
        return
    if num - 1 >= len(items_in_inventory):
        await message.answer("Вы ввели неправильный номер")
        counter = 1
        for it in items_in_inventory:
            item = GetItem(it[2])
            await message.answer(
                f"{counter}. Имя предмета: {item[0]}\nЦена: {item[1]}\nЦена Продажи: {item[2]}\nТип предмета: {item[3]}\nДоп HP: {item[4]}\nДоп Mana: {item[5]}\nДоп Атака: {item[6]}\nДоп Магическая атака: {item[7]}\nДоп Брон: {item[8]}\nДоп Магическая броня: {item[9]}\nНеобходимый уровень: {item[10]}\nКоличество: {it[3]}", )
            counter += 1
        await message.answer(
            "Напишите номер товара, который вы хотите продать",
            reply_markup=kb_cancel)
        return
    sold_item = GetItem(items_in_inventory[num - 1][2])
    await message.answer(
        f"Вы продали {items_in_inventory[num - 1][2]}\nУ вас осталось {MakeTransaction(str(message.from_user.id), sold_item[2])}",
        reply_markup=kb_game_city)
    TransferFromInventory(str(message.from_user.id), sold_item[0])
    await FSMGame.game.set()


@dp.message_handler(Text("Купить предметы"), state=FSMGame.market)
async def ChooseItemToBuy(message: types.Message, state: FSMContext):
    items_in_market = GetItemsInMarket(str(message.from_user.id))
    counter = 1
    for item in items_in_market:
        await message.answer(
            f"{counter}. Имя предмета: {item[0]}\nЦена: {item[1]}\nЦена Продажи: {item[2]}\nТип предмета: {item[3]}\nДоп HP: {item[4]}\nДоп Mana: {item[5]}\nДоп Атака: {item[6]}\nДоп Магическая атака: {item[7]}\nДоп Брон: {item[8]}\nДоп Магическая броня: {item[9]}\nНеобходимый уровень: {item[10]}", )
        counter += 1
    await message.answer("Напишите номер товара, который вы хотите купить",
                         reply_markup=kb_cancel)
    await FSMGame.choose_item_to_buy.set()


@dp.message_handler(state=FSMGame.choose_item_to_buy)
async def Buy(message: types.Message, state: FSMContext):
    if message.text.lower() == 'отмена':
        await message.answer("Процесс покупки отменен",
                             reply_markup=kb_game_city)
        await FSMGame.game.set()
        return
    num: int
    items_in_market = GetItemsInMarket(str(message.from_user.id))
    try:
        num = int(message.text)
    except ValueError:
        await message.answer("Вы ввели неправильный формат номера")
        counter = 1
        for item in items_in_market:
            await message.answer(
                f"{counter}. Имя предмета: {item[0]}\nЦена: {item[1]}\nЦена Продажи: {item[2]}\nТип предмета: {item[3]}\nДоп HP: {item[4]}\nДоп Mana: {item[5]}\nДоп Атака: {item[6]}\nДоп Магическая атака: {item[7]}\nДоп Брон: {item[8]}\nДоп Магическая броня: {item[9]}\nНеобходимый уровень: {item[10]}", )
            counter += 1
        await message.answer("Напишите номер товара, который вы хотите купить",
                             reply_markup=kb_cancel)
        return
    if num - 1 >= len(items_in_market):
        await message.answer("Вы ввели неправильный номер")
        counter = 1
        for item in items_in_market:
            await message.answer(
                f"{counter}. Имя предмета: {item[0]}\nЦена: {item[1]}\nЦена Продажи: {item[2]}\nТип предмета: {item[3]}\nДоп HP: {item[4]}\nДоп Mana: {item[5]}\nДоп Атака: {item[6]}\nДоп Магическая атака: {item[7]}\nДоп Брон: {item[8]}\nДоп Магическая броня: {item[9]}\nНеобходимый уровень: {item[10]}", )
            counter += 1
        await message.answer("Напишите номер товара, который вы хотите купить",
                             reply_markup=kb_cancel)
        return
    await message.answer(
        f"Вы купили {items_in_market[num - 1][0]}\nУ вас осталось {MakeTransaction(str(message.from_user.id), -items_in_market[num - 1][1])}",
        reply_markup=kb_game_city)
    TransferToInventory(str(message.from_user.id), items_in_market[num - 1][0])
    await FSMGame.game.set()


@dp.message_handler(Text("Выйти из магазина"), state=FSMGame.market)
async def ChooseGood(message: types.Message, state: FSMContext):
    await state.finish()
    await FSMGame.game.set()
    await message.answer("Вы вышли из магазина", reply_markup=kb_game_city)


@dp.message_handler(Text("Переместиться"), state=FSMGame.game)
async def ChooseLocation(message: types.Message):
    locations = AllAvailableLocation(str(message.from_user.id))
    text = "Доступные локации:\n"
    counter = 1
    for loc in locations:
        text += f"{counter}. {loc[2]} {loc[0]} время в пути {loc[1]} сек\n"
        counter += 1
    await message.answer(text)
    await message.answer("Напишите номер локации", reply_markup=kb_cancel)
    await FSMGame.choose_location.set()


@dp.message_handler(state=FSMGame.choose_location)
async def move(message: types.Message, state: FSMContext):
    locations = AllAvailableLocation(str(message.from_user.id))
    if message.text.lower() == 'отмена':
        await FSMGame.game.set()
        await message.answer("Процесс перехода в другую локациюю отменен",
                             reply_markup=kb_game_city)
    else:
        num: int
        try:
            num = int(message.text)
        except ValueError:
            text = "Доступные локации:\n"
            counter = 1
            for loc in locations:
                text += f"{counter}. {loc[2]} {loc[0]} время в пути {loc[1]} сек\n"
            await message.answer("Вы ввели неправильный формат")
            await message.answer(text, reply_markup=kb_cancel)
            return
        if num - 1 >= len(locations):
            text = "Доступные локации:\n"
            counter = 1
            for loc in locations:
                text += f"{counter}. {loc[2]} {loc[0]} время в пути {loc[1]} сек\n"
            await message.answer("Вы ввели неверный номер")
            await message.answer(text, reply_markup=kb_cancel)
            return
        location_id = GetLocationId(locations[num - 1][0])
        SetNewLocation(str(message.from_user.id), location_id)
        print(locations[num - 1][0])
        await message.answer(
            f"Вы перемещаетесь в {locations[num - 1][0]}. Время в пути {locations[num - 1][1]} сек ")
        await FSMGame.moving.set()
        await sleep(locations[num - 1][1])
        await FSMGame.game.set()
        if locations[num - 1][2] == 'город':
            Recover(str(message.from_user.id))
            await message.answer(f"Вы переместились в {locations[num - 1][0]}",
                                 reply_markup=kb_game_city)
            await message.answer("Здоровье восстановлено до 100 HP",reply_markup=kb_game_city)
        else:
            await message.answer(f"Вы переместились в {locations[num - 1][0]}",
                                 reply_markup=kb_game_dangeon)


@dp.message_handler(Text("Получить информацию об инвентаре"),
                    state=FSMGame.game)
async def GetInfoAboutInventory(message: types.Message):
    items_in_inventory = GetItemsInInventory(str(message.from_user.id))
    location_type = GetTypeOfLocation(str(message.from_user.id))
    if len(items_in_inventory) == 0:
        if location_type == 'город':
            await message.answer(
                "Пока нету предметов в инвентаре, но вы можете их купить в любом городе",
                reply_markup=kb_game_city)
        else:
            await message.answer(
                "Пока нету предметов в инвентаре, но вы можете их купить в любом городе",
                reply_markup=kb_game_dangeon)
    else:
        await message.answer("Ваш инвентарь")
        for item in items_in_inventory:
            if not item[-1]:
                item_data = GetItem(item[2])
                if location_type == 'город':
                    await message.answer(
                        f"Имя предмета: {item_data[0]}\nЦена: {item_data[1]}\nЦена Продажи: {item_data[2]}\nТип предмета: {item_data[3]}\nДоп HP: {item_data[4]}\nДоп Mana: {item_data[5]}\nДоп Атака: {item_data[6]}\nДоп Магическая атака: {item_data[7]}\nДоп Брон: {item_data[8]}\nДоп Магическая броня: {item_data[9]}\nНеобходимый уровень: {item_data[10]}\nКоличество: {item[3]}",
                        reply_markup=kb_game_city)
                else:
                    await message.answer(
                        f"Имя предмета: {item_data[0]}\nЦена: {item_data[1]}\nЦена Продажи: {item_data[2]}\nТип предмета: {item_data[3]}\nДоп HP: {item_data[4]}\nДоп Mana: {item_data[5]}\nДоп Атака: {item_data[6]}\nДоп Магическая атака: {item_data[7]}\nДоп Брон: {item_data[8]}\nДоп Магическая броня: {item_data[9]}\nНеобходимый уровень: {item_data[10]}\nКоличество: {item[3]}",
                        reply_markup=kb_game_dangeon)
        dressed_items = GetDressedOnItems(str(message.from_user.id))
        if len(dressed_items) == 0:
            if location_type == 'город':
                await message.answer(
                    "На вас пока не надеты никакие предметы, но вы можете их надеть",
                    reply_markup=kb_game_city)
            else:
                await message.answer(
                    "На вас пока не надеты никакие предметы, но вы можете их надеть",
                    reply_markup=kb_game_dangeon)
        else:
            await message.answer("Надетые на вас предметы")
            for item in dressed_items:
                item_data = GetItem(item[2])
                if location_type == 'город':
                    await message.answer(
                        f"Имя предмета: {item_data[0]}\nЦена: {item_data[1]}\nЦена Продажи: {item_data[2]}\nТип предмета: {item_data[3]}\nДоп HP: {item_data[4]}\nДоп Mana: {item_data[5]}\nДоп Атака: {item_data[6]}\nДоп Магическая атака: {item_data[7]}\nДоп Брон: {item_data[8]}\nДоп Магическая броня: {item_data[9]}\nНеобходимый уровень: {item_data[10]}\nКоличество: {item[3]}",
                        reply_markup=kb_game_city)
                else:
                    await message.answer(
                        f"Имя предмета: {item_data[0]}\nЦена: {item_data[1]}\nЦена Продажи: {item_data[2]}\nТип предмета: {item_data[3]}\nДоп HP: {item_data[4]}\nДоп Mana: {item_data[5]}\nДоп Атака: {item_data[6]}\nДоп Магическая атака: {item_data[7]}\nДоп Брон: {item_data[8]}\nДоп Магическая броня: {item_data[9]}\nНеобходимый уровень: {item_data[10]}\nКоличество: {item[3]}",
                        reply_markup=kb_game_dangeon)


@dp.message_handler(state=FSMGame.moving)
async def CollectDuringMove(message: types.Message):
    pass


@dp.message_handler(Text("Переодеться"),state=FSMGame.game)
async def ChooseItems(message: types.Message):
    items_in_inventory = GetItemsInInventory(str(message.from_user.id))
    if len(items_in_inventory) == 0:
        await message.answer(
            "Пока нету предметов в инвентаре, но вы можете их купить в любом городе",
            reply_markup=kb_game_city)
        return
    counter = 1
    for item in items_in_inventory:
        item_data = GetItem(item[2])
        await message.answer(
            f"{counter}. Имя предмета: {item_data[0]}\nТип предмета: {item_data[3]}\nДоп HP: {item_data[4]}\nДоп Mana: {item_data[5]}\nДоп Атака: {item_data[6]}\nДоп Магическая атака: {item_data[7]}\nДоп Бронь: {item_data[8]}\nДоп Магическая броня: {item_data[9]}\nСтатус ношения: {Convert(item[4])}")
        counter+=1
    await message.answer("Какой предмет вы хотите надеть? Напишите номер. Если вы хотите надеть предмет, тип которого уже надета, то та вещь автоматически снимется")
    await FSMGame.redress.set()


@dp.message_handler(state=FSMGame.redress)
async def Redress(message: types.Message):
    items_in_inventory = GetItemsInInventory(str(message.from_user.id))
    if message.text.lower() == 'отмена':
        await FSMGame.game.set()
        await message.answer("Процесс передевания отменен",
                             reply_markup=kb_game_city)
        return
    num: int
    try:
        num = int(message.text)
    except ValueError:
        await message.answer("Вы ввели неправильный формат")
        counter = 1
        for item in items_in_inventory:
            item_data = GetItem(item[2])
            await message.answer(
                f"{counter}. Имя предмета: {item_data[0]}\nТип предмета: {item_data[3]}\nДоп HP: {item_data[4]}\nДоп Mana: {item_data[5]}\nДоп Атака: {item_data[6]}\nДоп Магическая атака: {item_data[7]}\nДоп Бронь: {item_data[8]}\nДоп Магическая броня: {item_data[9]}\nСтатус ношения: {Convert(item[4])}")
            counter += 1
        await message.answer(
            "Какой предмет вы хотите надеть? Напишите номер. Если вы хотите надеть предмет, тип которого уже надета, то та вещь автоматически снимется")
        return
    if num - 1 >= len(items_in_inventory):
        await message.answer("Вы ввели неверный номер")
        counter = 1
        for item in items_in_inventory:
            item_data = GetItem(item[2])
            await message.answer(
                f"{counter}. Имя предмета: {item_data[0]}\nТип предмета: {item_data[3]}\nДоп HP: {item_data[4]}\nДоп Mana: {item_data[5]}\nДоп Атака: {item_data[6]}\nДоп Магическая атака: {item_data[7]}\nДоп Бронь: {item_data[8]}\nДоп Магическая броня: {item_data[9]}\nСтатус ношения: {Convert(item[4])}")
            counter += 1
        await message.answer(
            "Какой предмет вы хотите надеть? Напишите номер. Если вы хотите надеть предмет, тип которого уже надета, то та вещь автоматически снимется")
        return
    if not items_in_inventory[num - 1][-1]:
        DressOn(str(message.from_user.id),items_in_inventory[num - 1][2],GetItem(items_in_inventory[num - 1][2])[3])
    else:
        DressOff(str(message.from_user.id),items_in_inventory[num - 1][2])
    await FSMGame.game.set()
    await message.answer("Переодет",reply_markup=kb_game_city)


@dp.message_handler(Text("Получить информацию"),state=FSMGame.game)
async def GetInfo(message: types.Message):
    await message.answer(f"Сейчас вы находитесь в {GetTypeOfLocation(str(message.from_user.id))} {GetCityName(str(message.from_user.id))}")
    await message.answer(f"Сейчас у вас {GetMoney(str(message.from_user.id))} рупий")
    await message.answer(f"Ваш уровень: {GetLevel(str(message.from_user.id))}")


@dp.message_handler(Text("В бой"),state=FSMGame.game)
async def prepare(message: types.Message):
    random_mob = choice(GetMobPossibleLevel(str(message.from_user.id)))
    await message.answer(f"Информация о мобе\nИмя: {random_mob[0]}\nHP: {random_mob[1]}\nПолучите XP: {random_mob[2]}\nПолучите рупий: {2*random_mob[2]}\nТип атаки: {random_mob[4]}\nСила атаки: {random_mob[5]}\nБроня: {random_mob[6]}\nМагическая броня: {random_mob[7]}\n")
    await message.answer("Приготовьтесь",reply_markup=kb_battle_preparation)
    TransferToBattleSession(str(message.from_user.id),random_mob)
    await FSMGame.battle_preparation.set()


@dp.message_handler(Text("Начать"),state=FSMGame.battle_preparation)
async def StartBattle(message: types.Message):
    await message.answer("Удачи!")
    await FSMGame.battle.set()
    await message.answer("Выберете тип атаки",reply_markup=kb_attack)


@dp.message_handler(state=FSMGame.battle)
async def Battle(message: types.Message):
    damage = 0
    if message.text == "Физическая атака":
        armor_mob = GetArmorMob(str(message.from_user.id))
        Attack(str(message.from_user.id),max(0, GetPhysAttack(str(message.from_user.id))-armor_mob))
        damage = max(0, GetPhysAttack(str(message.from_user.id))-armor_mob)
    else:
        armor_mob = GetMagicArmorMob(str(message.from_user.id))
        Attack(str(message.from_user.id),
               max(0, GetMagicAttack(str(message.from_user.id)) - armor_mob))
        damage = max(0, GetMagicAttack(str(message.from_user.id)) - armor_mob)
    await message.answer(f"Вы нанесли {damage}. У противника осталось {max(0,GetHPMob(str(message.from_user.id)))} HP")
    if GetHPMob(str(message.from_user.id))<=0:
        await message.answer("Вы победили", reply_markup=kb_game_dangeon)
        Win(str(message.from_user.id))
        await FSMGame.game.set()
        return
    if GetTypeAttackMob(str(message.from_user.id)) == 'физический':
        user_armor = GetArmour(str(message.from_user.id))
        mob_attack = GetAttackMob(str(message.from_user.id))
        AttackMob(str(message.from_user.id),max(0,mob_attack-user_armor))
        damage = max(0,mob_attack-user_armor)
    else:
        user_armor = GetMagicArmour(str(message.from_user.id))
        mob_attack = GetAttackMob(str(message.from_user.id))
        AttackMob(str(message.from_user.id), max(0, mob_attack - user_armor))
        damage = max(0,mob_attack-user_armor)
    await message.answer(
        f"Вам нанесли {damage}. У вас осталось {max(0,GetHP(str(message.from_user.id)))} HP")
    if GetHP(str(message.from_user.id))<=0:
        Loose(str(message.from_user.id))
        await message.answer("Вы проиграли")
        Recover(str(message.from_user.id))
        await message.answer("Вы возращены в первоначальный город!\n Ваше здоровье восстановлено до 100",reply_markup=kb_game_city)
        await FSMGame.game.set()
        return
    await message.answer("Выберете тип атаки", reply_markup=kb_attack)


@dp.message_handler(Text("Выпить зелье"),state=FSMGame.battle_preparation)
async def drink(message: types.Message):
    await message.answer("Пока не завезли",reply_markup=kb_battle_preparation)