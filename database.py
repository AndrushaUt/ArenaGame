import sqlalchemy as db
from sqlalchemy import and_

engine = db.create_engine('sqlite:///database_arena.db')
connection = engine.connect()
metadata = db.MetaData()

person = db.Table(
    'Person',
    metadata,
    db.Column('UserID', db.Text),
    db.Column('Nickname', db.Text),
    db.Column('Level', db.Integer),
    db.Column('HP', db.Integer),
    db.Column('CurHP', db.Integer),
    db.Column('Money', db.Integer),
    db.Column('Attack', db.Integer),
    db.Column('MagicAttack', db.Integer),
    db.Column('XP', db.Integer),
    db.Column('Armour', db.Integer),
    db.Column('MagicArmour', db.Integer),
    db.Column('LocationID', db.Text)
)

mobs = db.Table(
    'Mobs',
    metadata,
    db.Column('MobID', db.Text),
    db.Column('HP', db.Integer),
    db.Column('XP', db.Integer),
    db.Column('ReqLevel', db.Integer),
    db.Column('AttackType', db.Integer),
    db.Column('Attack', db.Integer),
    db.Column('Armour', db.Integer),
    db.Column('MagicArmour', db.Integer),
)

locations = db.Table(
    'Locations',
    metadata,
    db.Column('LocationID', db.Text),
    db.Column('LocationName', db.Text),
    db.Column('XCoord', db.Integer),
    db.Column('YCoord', db.Integer),
    db.Column('LocationType', db.Text),
)

items = db.Table(
    'Items',
    metadata,
    db.Column('ItemID', db.Text),
    db.Column('Cost', db.Integer),
    db.Column('CostToSale', db.Integer),
    db.Column('ItemType', db.Text),
    db.Column('HP', db.Integer),
    db.Column('Mana', db.Integer),
    db.Column('Attack', db.Integer),
    db.Column('MagicAttack', db.Integer),
    db.Column('Armour', db.Integer),
    db.Column('MagicArmour', db.Integer),
    db.Column('ReqLevel', db.Integer),
)

current_session = db.Table(
    'Session',
    metadata,
    db.Column('UserID', db.Text),
    db.Column('Nickname', db.Text)
)

market = db.Table(
    'Market',
    metadata,
    db.Column('LocationID', db.Text),
    db.Column('ItemID', db.Text)
)

inventory = db.Table(
    'Inventory',
    metadata,
    db.Column('UserID', db.Text),
    db.Column('Nickname', db.Text),
    db.Column('ItemID', db.Text),
    db.Column('quantity', db.Integer),
    db.Column('wear_indictor', db.BOOLEAN)
)

battle_session = db.Table(
    'Battle',
    metadata,
    db.Column('UserID', db.Text),
    db.Column('MobID', db.Text),
    db.Column('HP', db.Integer),
    db.Column('XP', db.Integer),
    db.Column('ReqLevel', db.Integer),
    db.Column('AttackType', db.Integer),
    db.Column('Attack', db.Integer),
    db.Column('Armour', db.Integer),
    db.Column('MagicArmour', db.Integer),
)

statistic = db.Table(
    "Statistics",
    metadata,
    db.Column('UserID', db.Text),
    db.Column('Nickname', db.Text),
    db.Column('AmountOfWins', db.Integer),
    db.Column('AmountOfLooses', db.Integer),
    db.Column('MaxLevel', db.Integer)
)
metadata.create_all(engine)


def GetOldSessions(user_id: str) -> list:
    get_old_sessions_query = db.select(person.columns.Nickname).where(
        person.columns.UserID == user_id)
    return connection.execute(get_old_sessions_query).fetchall()


def CloseSession(user_id: str):
    close_session_query = db.delete(current_session).where(
        current_session.columns.UserID == user_id)
    connection.execute(close_session_query)


def StartSession(user_id: str, nickname: str):
    start_session_query = db.insert(current_session).values({
        'UserID': user_id, 'Nickname': nickname
    })
    connection.execute(start_session_query)


def IsPersonExist(user_id: str, nickname: str) -> bool:
    query = db.select(person).where(and_(person.columns.UserID == user_id,
                                         person.columns.Nickname == nickname))
    persons = connection.execute(query).fetchall()
    if len(persons) == 0:
        return False
    return True


def CreatePersonage(user_id: str, nickname: str):
    connection.execute(db.insert(person).values([
        {'UserID': user_id, 'Nickname': nickname, 'Level': 1, 'HP': 100,
         'Attack': 100,
         'CurHP': 100, 'Money': 100, 'MagicAttack': 100, 'XP': 100,
         'Armour': 100,
         'MagicArmour': 100, 'LocationID': '1'}
    ]))
    StartSession(user_id, nickname)


def GetCityName(user_id: str) -> str:
    nickname = GetNickname(user_id)
    location_id = connection.execute(
        db.select(person.columns.LocationID).where(and_(
            person.columns.UserID == user_id,
            person.columns.Nickname == nickname
        ))
    ).fetchone()[0]
    location_name = connection.execute(
        db.select(locations.columns.LocationName).where(
            locations.columns.LocationID == location_id)
    ).fetchone()[0]
    return location_name


def GetNickname(user_id: str) -> str:
    nickname = \
        connection.execute(db.select(current_session.columns.Nickname).where(
            current_session.columns.UserID == user_id)).fetchone()[0]
    return nickname


def GetMoney(user_id: str) -> int:
    nickname = GetNickname(user_id)
    money = connection.execute(db.select(person.columns.Money).where(
        and_(person.columns.UserID == user_id,
             person.columns.Nickname == nickname))).fetchone()[0]
    return money


def GetItemsInMarket(user_id: str) -> list:
    nickname = GetNickname(user_id)
    personage = connection.execute(db.select(person).where(
        and_(person.columns.UserID == user_id,
             person.columns.Nickname == nickname))).fetchone()
    print(nickname)
    location_id = \
        connection.execute(db.select(person.columns.LocationID).where(
            and_(person.columns.UserID == user_id,
                 person.columns.Nickname == nickname))).fetchone()[0]
    items_in_market = connection.execute(
        db.select(market.columns.ItemID).where(
            market.columns.LocationID == location_id)).fetchall()
    output = []
    print(items_in_market)
    for item in items_in_market:
        item_data = connection.execute(db.select(items).where(
            items.columns.ItemID == item[0])).fetchone()
        print(item_data[1], GetMoney(user_id))
        if item_data[1] <= GetMoney(user_id) and personage[2] >= item_data[-1]:
            output.append(item_data)
    print(output)
    return output


def MakeTransaction(user_id: str, money: int) -> int:
    nickname = GetNickname(user_id)
    current_money = GetMoney(user_id) + money
    connection.execute(db.update(person).where(
        and_(person.columns.UserID == user_id,
             person.columns.Nickname == nickname)).values(Money=current_money))
    return current_money


def TransferToInventory(user_id: str, item_id: str):
    nickname = GetNickname(user_id)
    quantity = connection.execute(db.select(inventory.columns.quantity).where(
        and_(inventory.columns.UserID == user_id,
             inventory.columns.Nickname == nickname,
             inventory.columns.ItemID == item_id))).fetchone()
    if quantity is None:
        connection.execute(db.insert(inventory).values({
            'UserID': user_id, 'Nickname': nickname, 'ItemID': item_id,
            'quantity': 1, 'wear_indictor': False
        }))
    else:
        connection.execute(db.update(inventory).where(
            and_(inventory.columns.UserID == user_id,
                 inventory.columns.Nickname == nickname,
                 inventory.columns.ItemID == item_id)).values({
            'quantity': quantity[0] + 1
        }))


def AllAvailableLocation(user_id: str) -> list:
    output = []
    nickname = GetNickname(user_id)
    location_id = \
        connection.execute(db.select(person.columns.LocationID).where(and_(
            person.columns.UserID == user_id,
            person.columns.Nickname == nickname
        ))).fetchone()[0]
    print(location_id)
    location = connection.execute(db.select(locations).where(
        locations.columns.LocationID == location_id)).fetchone()
    x, y = location[2], location[3]
    for loc in connection.execute(db.select(locations).where(
            locations.columns.LocationID != location_id)).fetchall():
        other_x, other_y = loc[2], loc[3]
        if ((x - other_x) ** 2 + (y - other_y) ** 2) ** .5 <= 10:
            output.append((loc[1], int(((x - other_x) ** 2 + (
                    y - other_y) ** 2) ** .5), loc[4],))
    return output


def GetLocationId(city_name: str) -> str:
    location_id = \
        connection.execute(db.select(locations.columns.LocationID).where(
            locations.columns.LocationName == city_name)).fetchone()[0]
    return location_id


def SetNewLocation(user_id: str, location_id: str):
    nickname = GetNickname(user_id)
    connection.execute(db.update(person).where(
        and_(person.columns.UserID == user_id,
             person.columns.Nickname == nickname)).values(
        LocationID=location_id))


def GetItemsInInventory(user_id: str) -> list:
    nickname = GetNickname(user_id)
    items_in_inventory = connection.execute(db.select(inventory).where(
        and_(inventory.columns.UserID == user_id,
             inventory.columns.Nickname == nickname))).fetchall()
    return items_in_inventory


def GetItem(item_id: str) -> tuple:
    item_data = connection.execute(
        db.select(items).where(items.columns.ItemID == item_id)).fetchone()
    return item_data


def GetTypeOfLocation(user_id: str) -> str:
    nickname = GetNickname(user_id)
    location_id = connection.execute(
        db.select(person.columns.LocationID).where(
            and_(person.columns.UserID == user_id,
                 person.columns.Nickname == nickname))).fetchone()[0]
    location_type = connection.execute(
        db.select(locations.columns.LocationType).where(
            locations.columns.LocationID == location_id)).fetchone()[0]
    return location_type


def TransferFromInventory(user_id: str, item_id: str):
    nickname = GetNickname(user_id)
    quantity = connection.execute(db.select(inventory.columns.quantity).where(
        and_(inventory.columns.UserID == user_id,
             inventory.columns.Nickname == nickname,
             inventory.columns.ItemID == item_id))).fetchone()
    if quantity[0] == 1:
        connection.execute(db.delete(inventory).where(
            and_(inventory.columns.UserID == user_id,
                 inventory.columns.Nickname == nickname,
                 inventory.columns.ItemID == item_id)))
    else:
        connection.execute(db.update(inventory).where(
            and_(inventory.columns.UserID == user_id,
                 inventory.columns.Nickname == nickname,
                 inventory.columns.ItemID == item_id)).values({
            'quantity': quantity[0] - 1
        }))


def GetDressedOnItems(user_id: str) -> list:
    nickname = GetNickname(user_id)
    dressed_items = connection.execute(db.select(inventory).where(
        and_(inventory.columns.UserID == user_id,
             inventory.columns.Nickname == nickname,
             inventory.columns.wear_indictor == True))).fetchall()
    return dressed_items


def DressOn(user_id: str, item_id: str, item_type: str):
    nickname = GetNickname(user_id)
    dressed_items = connection.execute(
        db.select(inventory.columns.ItemID).where(
            and_(inventory.columns.UserID == user_id,
                 inventory.columns.Nickname == nickname,
                 inventory.columns.ItemID != item_id,
                 inventory.columns.wear_indictor == True))).fetchall()
    personage = connection.execute(db.select(person).where(
        and_(person.columns.UserID == user_id,
             person.columns.Nickname == nickname))).fetchone()
    for item in dressed_items:
        item_data = GetItem(item[0])
        if item_data[3] == item_type:
            connection.execute(db.update(inventory).where(
                and_(inventory.columns.UserID == user_id,
                     inventory.columns.Nickname == nickname,
                     inventory.columns.ItemID == item[0],
                     inventory.columns.wear_indictor == True)).values(
                wear_indictor=False))
            connection.execute(db.update(person).where(
                and_(person.columns.UserID == user_id,
                     person.columns.Nickname == nickname)).values({
                "HP": personage[3] - item_data[4],
                "Attack": personage[6] - item_data[6],
                "MagicAttack": personage[7] - item_data[7],
                "Armour": personage[8] - item_data[7],
                "MagicArmour": personage[9] - item_data[8]
            }))
            break
    personage = connection.execute(db.select(person).where(
        and_(person.columns.UserID == user_id,
             person.columns.Nickname == nickname))).fetchone()
    connection.execute(db.update(inventory).where(
        and_(inventory.columns.UserID == user_id,
             inventory.columns.Nickname == nickname,
             inventory.columns.ItemID == item_id,
             inventory.columns.wear_indictor == False)).values(
        wear_indictor=True))
    item_data = GetItem(item_id)
    connection.execute(db.update(person).where(
        and_(person.columns.UserID == user_id,
             person.columns.Nickname == nickname)).values({
        "HP": personage[3] + item_data[4],
        "Attack": personage[6] + item_data[6],
        "MagicAttack": personage[7] + item_data[7],
        "Armour": personage[8] + item_data[7],
        "MagicArmour": personage[9] + item_data[8]
    }))


def DressOff(user_id: str, item_id: str):
    nickname = GetNickname(user_id)
    personage = connection.execute(db.select(person).where(
        and_(person.columns.UserID == user_id,
             person.columns.Nickname == nickname))).fetchone()
    connection.execute(db.update(inventory).where(
        and_(inventory.columns.UserID == user_id,
             inventory.columns.Nickname == nickname,
             inventory.columns.ItemID == item_id,
             inventory.columns.wear_indictor == True)).values(
        wear_indictor=False))
    item_data = GetItem(item_id)
    connection.execute(db.update(person).where(
        and_(person.columns.UserID == user_id,
             person.columns.Nickname == nickname)).values({
        "HP": personage[3] - item_data[4],
        "Attack": personage[6] - item_data[6],
        "MagicAttack": personage[7] - item_data[7],
        "Armour": personage[8] - item_data[7],
        "MagicArmour": personage[9] - item_data[8]
    }))


def GetMobPossibleLevel(user_id: str)->list:
    nickname = GetNickname(user_id)
    level = connection.execute(db.select(person.columns.Level).where(
        and_(person.columns.UserID == user_id,
             person.columns.Nickname == nickname))).fetchone()[0]
    available_mobs = connection.execute(db.select(mobs).where(mobs.columns.ReqLevel <= level)).fetchall()
    return available_mobs


def GetArmorMob(user_id:str)->int:
    armor = connection.execute(db.select(battle_session.columns.Armour).where(battle_session.columns.UserID == user_id)).fetchone()[0]
    return armor

def GetMagicArmorMob(user_id:str)->int:
    magic_armor = connection.execute(db.select(battle_session.columns.MagicArmour).where(battle_session.columns.UserID == user_id)).fetchone()[0]
    return magic_armor

def Attack(user_id:str, damage:int):
    mob = connection.execute(db.select(battle_session).where(battle_session.columns.UserID == user_id)).fetchone()
    print(mob[2])
    connection.execute(db.update(battle_session).where(battle_session.columns.UserID == user_id).values(HP=(mob[2]-damage)))


def GetPhysAttack(user_id: str)->int:
    nickname = GetNickname(user_id)
    attack = connection.execute(db.select(person.columns.Attack).where(and_(person.columns.UserID == user_id, person.columns.Nickname == nickname))).fetchone()[0]
    return attack


def GetMagicAttack(user_id: str)->int:
    nickname = GetNickname(user_id)
    attack = connection.execute(db.select(person.columns.MagicAttack).where(and_(person.columns.UserID == user_id, person.columns.Nickname == nickname))).fetchone()[0]
    return attack


def GetHPMob(user_id:str)->int:
    hp = connection.execute(
        db.select(battle_session.columns.HP).where(
            battle_session.columns.UserID == user_id)).fetchone()[0]
    return hp


def GetTypeAttackMob(user_id:str)->str:
    type = connection.execute(
        db.select(battle_session.columns.AttackType).where(
            battle_session.columns.UserID == user_id)).fetchone()[0]
    return type


def GetArmour(user_id: str)->int:
    nickname = GetNickname(user_id)
    armour = connection.execute(db.select(person.columns.Armour).where(and_(person.columns.UserID == user_id, person.columns.Nickname == nickname))).fetchone()[0]
    return armour


def GetMagicArmour(user_id: str)->int:
    nickname = GetNickname(user_id)
    magic_armour = connection.execute(db.select(person.columns.MagicArmour).where(and_(person.columns.UserID == user_id, person.columns.Nickname == nickname))).fetchone()[0]
    return magic_armour


def GetAttackMob(user_id:str)->int:
    attack = connection.execute(db.select(battle_session.columns.Attack).where(battle_session.columns.UserID == user_id)).fetchone()[0]
    return attack

def AttackMob(user_id:str, damage:int):
    nickname = GetNickname(user_id)
    pers = connection.execute(db.select(person).where(and_(person.columns.UserID == user_id,person.columns.Nickname == nickname))).fetchone()
    connection.execute(db.update(person).where(and_(person.columns.UserID == user_id,person.columns.Nickname == nickname)).values(HP=(pers[3]-damage)))


def GetHP(user_id: str)->int:
    nickname = GetNickname(user_id)
    hp = connection.execute(db.select(person.columns.HP).where(and_(person.columns.UserID == user_id, person.columns.Nickname == nickname))).fetchone()[0]
    return hp


def TransferToBattleSession(user_id: str, mob:tuple):
    connection.execute(db.insert(battle_session).values([
        {"UserID":user_id,"MobID": mob[0], 'HP': mob[1], 'XP': mob[2], 'ReqLevel': mob[3],
    "AttackType": mob[4], 'Attack': mob[5], 'Armour': mob[6],
    'MagicArmour': mob[7]}
    ]))


def Win(user_id:str):
    nickname = GetNickname(user_id)
    pers = connection.execute(db.select(person).where(
        and_(person.columns.UserID == user_id,
             person.columns.Nickname == nickname))).fetchone()
    mob = connection.execute(db.select(battle_session).where(battle_session.columns.UserID == user_id)).fetchone()
    connection.execute(db.update(person).where(
        and_(person.columns.UserID == user_id,
             person.columns.Nickname == nickname)).values({
        'XP': pers[8]+mob[3], 'Money':pers[5]+2*mob[3]
    }))
    pers = connection.execute(db.select(person).where(
        and_(person.columns.UserID == user_id,
             person.columns.Nickname == nickname))).fetchone()
    stat_for_user = connection.execute(db.select(statistic).where(
        and_(statistic.columns.UserID == user_id,
             statistic.columns.Nickname == nickname))).fetchone()
    if pers[8]>=100:
        connection.execute(db.update(person).where(
            and_(person.columns.UserID == user_id,
                 person.columns.Nickname == nickname)).values({
            'XP': pers[8]-100, 'Level': pers[2] + 1
        }))
        connection.execute(db.update(statistic).where(
            and_(statistic.columns.UserID == user_id,
                 statistic.columns.Nickname == nickname)).values({
            'MaxLevel': stat_for_user[-1]+1
        }))
    connection.execute(db.update(statistic).where(
        and_(statistic.columns.UserID == user_id,
             statistic.columns.Nickname == nickname)).values({
        'AmountOfWins': stat_for_user[2] + 1
    }))
    connection.execute(db.delete(battle_session).where(
        battle_session.columns.UserID == user_id))


def Loose(user_id: str):
    nickname = GetNickname(user_id)
    pers = connection.execute(db.select(person).where(
        and_(person.columns.UserID == user_id,
             person.columns.Nickname == nickname))).fetchone()
    mob = connection.execute(db.select(battle_session).where(
        battle_session.columns.UserID == user_id)).fetchone()
    connection.execute(db.update(person).where(
        and_(person.columns.UserID == user_id,
             person.columns.Nickname == nickname)).values({
        'Money': pers[5] + mob[3]
    }))
    stat_for_user = connection.execute(db.select(statistic).where(
        and_(statistic.columns.UserID == user_id,
             statistic.columns.Nickname == nickname))).fetchone()
    connection.execute(db.update(statistic).where(
        and_(statistic.columns.UserID == user_id,
             statistic.columns.Nickname == nickname)).values({
        'AmountOfLooses': stat_for_user[2] + 1
    }))
    connection.execute(db.delete(battle_session).where(
        battle_session.columns.UserID == user_id))
    SetNewLocation(user_id,'1')

def NewPersonToStatistic(user_id: str):
    nickname = GetNickname(user_id)
    connection.execute(db.insert(statistic).values({
        "UserID":user_id, "Nickname":nickname,"AmountOfWins":0, "AmountOfLooses":0,"MaxLevel":1
    }))

def Recover(user_id: str):
    nickname = GetNickname(user_id)
    connection.execute(db.update(person).where(
        and_(person.columns.UserID == user_id,
             person.columns.Nickname == nickname)).values(HP=100))

def Delete():
    connection.execute(db.delete(battle_session))
    connection.execute(db.delete(current_session))

def GetStat(user_id: str):
    stat = connection.execute(db.select(statistic).where(statistic.columns.UserID == user_id)).fetchall()
    return stat


def GetLevel(user_id: str)->int:
    nickname = GetNickname(user_id)
    level = connection.execute(db.select(person.columns.Level).where(and_(person.columns.UserID == user_id, person.columns.Nickname == nickname))).fetchone()[0]
    return level
