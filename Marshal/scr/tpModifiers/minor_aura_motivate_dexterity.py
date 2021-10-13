from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import aura_utils

print "Registering Minor Aura Motivate Dexterity"

def auraBonus(attachee, args, evt_obj):
    auraName = aura_utils.getAuraName(args.get_arg(2))
    auraTag = aura_utils.getAuraShortName(args.get_arg(2)).upper().replace(" ", "_")
    evt_obj.bonus_list.add(args.get_arg(1), 21,"~Circumstance~[TAG_MODIFIER_CIRCUMSTANCE] : ~{}~[TAG_AURA_{}]".format(auraName, auraTag))
    return 0

minorAura = PythonModifier("Minor Aura Motivate Dexterity", 3, False) #duration, auraBonus, auraEnum
minorAura.AddHook(ET_OnGetAbilityCheckModifier, EK_STAT_DEXTERITY, auraBonus, ())
minorAura.AddHook(ET_OnGetSkillLevel, EK_SKILL_BALANCE, auraBonus, ())
minorAura.AddHook(ET_OnGetSkillLevel, EK_SKILL_ESCAPE_ARTIST, auraBonus, ())
minorAura.AddHook(ET_OnGetSkillLevel, EK_SKILL_HIDE, auraBonus, ())
minorAura.AddHook(ET_OnGetSkillLevel, EK_SKILL_MOVE_SILENTLY, auraBonus, ())
minorAura.AddHook(ET_OnGetSkillLevel, EK_SKILL_OPEN_LOCK, auraBonus, ())
minorAura.AddHook(ET_OnGetSkillLevel, EK_SKILL_RIDE, auraBonus, ())
minorAura.AddHook(ET_OnGetSkillLevel, EK_SKILL_PICK_POCKET, auraBonus, ())
minorAura.AddHook(ET_OnGetSkillLevel, EK_SKILL_TUMBLE, auraBonus, ())
minorAura.AddHook(ET_OnGetSkillLevel, EK_SKILL_USE_ROPE, auraBonus, ())
minorAura.AddHook(ET_OnConditionAddPre, EK_NONE, aura_utils.auraAddPreActions, ())
minorAura.AddHook(ET_OnBeginRound, EK_NONE, aura_utils.auraBeginRound, ())
minorAura.AddHook(ET_OnD20PythonSignal, "S_Marshal_Minor_Aura_End", aura_utils.removeAura, ())
minorAura.AddHook(ET_OnD20PythonQuery, "Q_Has_Marshal_Minor_Aura", aura_utils.queryHasAuraCondition, ())
minorAura.AddHook(ET_OnGetTooltip, EK_NONE, aura_utils.getTooltip, ())
minorAura.AddHook(ET_OnGetEffectTooltip, EK_NONE, aura_utils.getEffectTooltipMinor, ())
