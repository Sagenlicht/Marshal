from templeplus.pymod import PythonModifier
from __main__ import game
from toee import *
import tpdp

def auraName():
    return "Marshal Adrenaline Boost Condition"

print "Registering {}".format(auraName())

def grantTempHp(attachee, args, evt_obj):
    tempHpBonus = args.get_arg(1)
    currentHp = attachee.stat_level_get(stat_hp_current)
    maxHp = attachee.stat_level_get(stat_hp_max)
    if (currentHp * 2) <= maxHp:
        tempHpBonus *= 2
    attachee.condition_add_with_args('Temporary_Hit_Points', 0, 10, tempHpBonus)
    return 0

def auraBeginRound(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

def removeTempHpSignal(attachee, args, evt_obj):
    attachee.d20_send_signal(S_Spell_End, 'Temporary_Hit_Points')
    return 0

def conditionRemoveActions(attachee, args, evt_obj):
    attachee.d20_send_signal(S_Spell_End, 'Temporary_Hit_Points')
    return 0

def queryHasMinorAuraCondition(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def signalKilled(attachee, args, evt_obj):
    args.condition_remove()
    return 0

adrenalineCondition = PythonModifier("{}".format(auraName()), 2) #duration, adrenalineBonus
adrenalineCondition.AddHook(ET_OnConditionAdd, EK_NONE, grantTempHp, ())
adrenalineCondition.AddHook(ET_OnConditionRemove, EK_NONE, conditionRemoveActions, ())
adrenalineCondition.AddHook(ET_OnD20Signal, EK_S_Temporary_Hit_Points_Removed, removeTempHpSignal, ())
adrenalineCondition.AddHook(ET_OnBeginRound, EK_NONE, auraBeginRound, ())
adrenalineCondition.AddHook(ET_OnD20Signal, EK_S_Killed, signalKilled, ())
