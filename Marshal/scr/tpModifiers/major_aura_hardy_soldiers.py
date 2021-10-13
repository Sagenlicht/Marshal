from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import aura_utils

print "Registering Major Aura Hardy Soldiers"

def auraBonus(attachee, args, evt_obj):
    evt_obj.damage_packet.add_physical_damage_res(args.get_arg(1), D20DAP_UNSPECIFIED, 126)
    return 0

majorAura = PythonModifier("Major Aura Hardy Soldiers", 3, False) #duration, auraBonus, auraEnum
majorAura.AddHook(ET_OnTakingDamage, EK_NONE, auraBonus, ())
majorAura.AddHook(ET_OnConditionAddPre, EK_NONE, aura_utils.auraAddPreActions, ())
majorAura.AddHook(ET_OnBeginRound, EK_NONE, aura_utils.auraBeginRound, ())
majorAura.AddHook(ET_OnD20PythonSignal, "S_Marshal_Major_Aura_End", aura_utils.removeAura, ())
majorAura.AddHook(ET_OnD20PythonQuery, "Q_Has_Marshal_Major_Aura", aura_utils.queryHasAuraCondition, ())
majorAura.AddHook(ET_OnGetTooltip, EK_NONE, aura_utils.getTooltip, ())
majorAura.AddHook(ET_OnGetEffectTooltip, EK_NONE, aura_utils.getEffectTooltipMajor, ())
