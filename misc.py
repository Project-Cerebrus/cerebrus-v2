
import random

from discord.errors import NotFound

levels = {
    "1": 0,
    "2": 1500,
    "3": 9000,
    "4": 22500,
    "5": 42000,
    "6": 67500,
    "7": 99000,
    "8": 136500,
    "9": 180000,
    "10": 229500,
    "11": 285000,
    "12": 346500,
    "13": 414000,
    "14": 487500,
    "15": 567000,
    "16": 697410,
    "17": 857814,
    "18": 1055112,
    "19": 1297787,
    "20": 1596278,
    "21": 1931497,
    "22": 2298481,
    "23": 2689223,
    "24": 3092606,
    "25": 3494645,
    "26": 3879056,
    "27": 4228171,
    "28": 4608707,
    "29": 5023490,
    "30": 5475604,
}


def hex_to_rgb(hex_):
    hex_ = hex_.lstrip("#")
    return tuple(int(hex_[i : i + 2], 16) for i in (0, 2, 4))


def xptolevel(xp):
    for point in list(levels.values()):
        if xp == point:
            return list(levels.keys())[list(levels.values()).index(point)]
        elif xp < point:
            return list(levels.keys())[list(levels.values()).index(point) - 1]
        elif xp > list(levels.values())[-1]:
            return list(levels.keys())[-1]


def xptonextlevel(xp):
    level = xptolevel(xp)
    if level == list(levels.keys())[-1]:
        return "Infinity"
    else:
        nextxp = levels[str(int(level) + 1)]
        return str(nextxp - xp)


def calcchance(
    sword, shield, dungeon, level, luck, returnsuccess=False, booster=False, bonus=0
):
    if returnsuccess is False:
        val1 = sword + shield + 75 - dungeon * 10
        val2 = sword + shield + 75 - dungeon * 2
        val1 = round(val1 * luck) if val1 >= 0 else round(val1 / luck)
        val2 = round(val2 * luck) if val2 >= 0 else round(val2 / luck)
        return (val1, val2, level)
    else:
        randomn = random.randint(0, 100)
        success = (
            sword
            + shield
            + 75
            - (dungeon * (random.randint(2, 10)))
            + random.choice([level, -level])
            + bonus
        )
        if success >= 0:
            success = round(success * luck)
        else:
            success = round(success / luck)
        if booster:
            success += 25
        return randomn <= success


async def lookup(bot, userid, return_none=False):
    userid = int(userid)
    member = await bot.get_user_global(userid)
    if member:
        return str(member)
    else:
        try:
            member = await bot.fetch_user(userid)
        except NotFound:
            if return_none:
                return None
            else:
                return "None"
        else:
            return str(member)
