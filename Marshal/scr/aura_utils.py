from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *

###Expect args:
#0: duration
#1: auraBonus
#2: auraEnum

###Aura enum pattern:
#0 - 60: Marshal Minor Auras
#61 - 99: Marshal Major Auras
#100 - 150: reserved for Dragon Shaman Auras (PHB II)
auraDict = {
0: "None",
1: "Minor Aura Accurate Strike",
2: "Minor Aura Art of War",
3: "Minor Aura Demand Fortitude",
4: "Minor Aura Determined Caster",
5: "Minor Aura Force of Will",
6: "Minor Aura Master of Opportunity",
7: "Minor Aura Master of Tactics",
8: "Minor Aura Motivate Charisma",
9: "Minor Aura Motivate Constitution",
10: "Minor Aura Motivate Dexterity",
11: "Minor Aura Motivate Intelligence",
12: "Minor Aura Motivate Strength",
13: "Minor Aura Motivate Wisdom",
14: "Minor Aura Over the Top",
15: "Minor Aura Watchful Eye",
61: "Major Aura Hardy Soldiers",
62: "Major Aura Motivate Ardor",
63: "Major Aura Motivate Attack",
64: "Major Aura Motivate Care",
65: "Major Aura Motivate Urgency",
66: "Major Aura Resilient Troops",
67: "Major Aura Steady Hand"
}

def getAuraName(auraEnum):
    return auraDict.get(auraEnum)

def getAuraShortName(auraEnum):
    auraShortName = str(getAuraName(auraEnum).split(" ", 2)[2])
    return auraShortName

def auraAddPreActions(attachee, args, evt_obj):
    auraName = getAuraName(args.get_arg(2))
    if evt_obj.is_modifier("{}".format(auraName)):
        duration = args.get_arg(0)
        duration += 1
        args.set_arg(0, duration)
        evt_obj.return_val = 0
    elif evt_obj.is_modifier("sp-Deafness"):
        args.condition_remove()
    return 0

def auraBeginRound(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

def queryHasAuraCondition(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def removeAura(attachee, args, evt_obj):
    args.condition_remove()
    return 0

def getTooltip(attachee, args, evt_obj):
    evt_obj.append("{}".format(getAuraName(args.get_arg(2))))
    return 0

def getEffectTooltipMinor(attachee, args, evt_obj):
    evt_obj.append(tpdp.hash("MARSHAL_MINOR_AURA"), -2, " ({})".format(getAuraShortName(args.get_arg(2))))
    return 0

def getEffectTooltipMajor(attachee, args, evt_obj):
    evt_obj.append(tpdp.hash("MARSHAL_MAJOR_AURA"), -2, " ({})".format(getAuraShortName(args.get_arg(2))))
    return 0
