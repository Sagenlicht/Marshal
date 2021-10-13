from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import aura_utils

print "Registering Major Aura Motivate Ardor"

def auraBonus(attachee, args, evt_obj):
    auraName = aura_utils.getAuraName(args.get_arg(2))
    auraTag = aura_utils.getAuraShortName(args.get_arg(2)).upper().replace(" ", "_")
    evt_obj.damage_packet.bonus_list.add(args.get_arg(1), 21, "~Circumstance~[TAG_MODIFIER_CIRCUMSTANCE] : ~{}~[TAG_AURA_{}]".format(auraName, auraTag))
    return 0

majorAura = PythonModifier("Major Aura Motivate Ardor", 3, False) #duration, auraBonus, auraEnum
majorAura.AddHook(ET_OnDealingDamage, EK_NONE, auraBonus, ())
majorAura.AddHook(ET_OnConditionAddPre, EK_NONE, aura_utils.auraAddPreActions, ())
majorAura.AddHook(ET_OnBeginRound, EK_NONE, aura_utils.auraBeginRound, ())
majorAura.AddHook(ET_OnD20PythonSignal, "S_Marshal_Major_Aura_End", aura_utils.removeAura, ())
majorAura.AddHook(ET_OnD20PythonQuery, "Q_Has_Marshal_Major_Aura", aura_utils.queryHasAuraCondition, ())
majorAura.AddHook(ET_OnGetTooltip, EK_NONE, aura_utils.getTooltip, ())
majorAura.AddHook(ET_OnGetEffectTooltip, EK_NONE, aura_utils.getEffectTooltipMajor, ())