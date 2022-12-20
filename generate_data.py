from database import db, connection, items, person, locations, market,mobs


def GenerateItems():
    items_to_generate = [
        {'ItemID': 'деревянный меч', 'Cost': 50, 'CostToSale': 25,
         'ItemType': 'оружие', 'HP': 0, 'Mana': 0, 'Attack': 30,
         'MagicAttack': 0,
         'Armour': 0, 'MagicArmour': 0, 'ReqLevel': 1},
        {'ItemID': 'медный меч', 'Cost': 85, 'CostToSale': 50,
         'ItemType': 'оружие', 'HP': 0, 'Mana': 0, 'Attack': 45,
         'MagicAttack': 0,
         'Armour': 0, 'MagicArmour': 0, 'ReqLevel': 1},
        {'ItemID': 'кольчуга', 'Cost': 250, 'CostToSale': 125,
         'ItemType': 'грудь', 'HP': 10, 'Mana': 0, 'Attack': 0,
         'MagicAttack': 0,
         'Armour': 30, 'MagicArmour': 0, 'ReqLevel': 2},
        {'ItemID': 'шлем', 'Cost': 200, 'CostToSale': 100,
         'ItemType': 'голова', 'HP': 0, 'Mana': 0, 'Attack': 0,
         'MagicAttack': 0,
         'Armour': 20, 'MagicArmour': 0, 'ReqLevel': 2},
        {'ItemID': 'булава', 'Cost': 400, 'CostToSale': 250,
         'ItemType': 'оружие', 'HP': 0, 'Mana': 0, 'Attack': 150,
         'MagicAttack': 0,
         'Armour': 0, 'MagicArmour': 0, 'ReqLevel': 4},
        {'ItemID': 'меч джедая', 'Cost': 1000, 'CostToSale': 700,
         'ItemType': 'оружие', 'HP': 0, 'Mana': 0, 'Attack': 0,
         'MagicAttack': 200,
         'Armour': 0, 'MagicArmour': 0, 'ReqLevel': 7},
        {'ItemID': 'щит Йоды', 'Cost': 700, 'CostToSale': 450,
         'ItemType': 'грудь', 'HP': 0, 'Mana': 0, 'Attack': 0,
         'MagicAttack': 0,
         'Armour': 0, 'MagicArmour': 150, 'ReqLevel': 6},
    ]
    connection.execute(db.insert(items).values(items_to_generate))


def GenerateMob():
    items_to_generate = [
        {"MobID": 'Элементаль хаоса', 'HP': 375, 'XP': 40, 'ReqLevel': 2,
         "AttackType": 'магический', 'Attack': 40, 'Armour': 30,
         'MagicArmour': 30},
        {"MobID": 'Викинг', 'HP': 250, 'XP': 30, 'ReqLevel': 1,
         "AttackType": 'физический', 'Attack': 35, 'Armour': 50,
         'MagicArmour': 10},
        {"MobID": 'Драгоноид', 'HP': 600, 'XP': 100, 'ReqLevel': 5,
         "AttackType": 'магический', 'Attack': 300, 'Armour': 100,
         'MagicArmour': 150},
        {"MobID": 'Хасбик', 'HP': 420, 'XP': 75, 'ReqLevel': 3,
        "AttackType": 'физический', 'Attack': 150, 'Armour': 75,
        'MagicArmour': 20},
    ]
    connection.execute(db.insert(mobs).values(items_to_generate))


def GenerateLocation():
    items_to_generate = [
        {'LocationID': '1', 'LocationName': 'Хилл-Вэлли', 'XCoord': 0,
         'YCoord': 0,
         'LocationType': 'город'},
        {'LocationID': '2', 'LocationName': 'Бальбек', 'XCoord': 1,
         'YCoord': 1,
         'LocationType': 'город'},
        {'LocationID': '3', 'LocationName': 'Куахог', 'XCoord': 4,
         'YCoord': 4,
         'LocationType': 'подземелье'},
        {'LocationID': '4', 'LocationName': 'Арглтон', 'XCoord': 15,
         'YCoord': 15,
         'LocationType': 'город'},
        {'LocationID': '5', 'LocationName': 'Ктоград', 'XCoord': 7,
         'YCoord': 7,
         'LocationType': 'подземелье'},
        {'LocationID': '6', 'LocationName': 'Лапута', 'XCoord': 8,
         'YCoord': 10,
         'LocationType': 'подземелье'},
    ]
    connection.execute(db.insert(locations).values(items_to_generate))


def GenerateMarket():
    items_to_generate = [
        {'LocationID': "1", "ItemID": "медный меч"},
        {'LocationID': "1", "ItemID": "деревянный меч"},
        {'LocationID': "2", "ItemID": "кольчуга"},
        {'LocationID': "2", "ItemID": "шлем"},
        {'LocationID': "2", "ItemID": "булава"},
        {'LocationID': "5", "ItemID": "меч джедая"},
        {'LocationID': "5", "ItemID": "щит Йоды"},
    ]
    connection.execute(db.insert(market).values(items_to_generate))


def Generate():
    # connection.execute(db.insert(person).values([
    #     {'UserID': "123", 'Nickname': 'Andrusha', 'Level': 1, 'HP': 100,
    #      'Attack': 100,
    #      'CurHP': 100, 'Money': 100, 'MagicAttack': 100, 'XP': 100,
    #      'Armour': 100,
    #      'MagicArmour': 100, 'LocationID': '100'}
    # ]))
    # GenerateItems()
    GenerateMarket()
    # GenerateMob()
    pass


Generate()  # для генерация всего, при пересоздании бд
