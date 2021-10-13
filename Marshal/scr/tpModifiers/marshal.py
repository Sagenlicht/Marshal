from templeplus.pymod import PythonModifier
from toee import *
import tpdp
import char_class_utils
import aura_utils
import tpactions

###################################################

def GetConditionName():
    return "Marshal"

print "Registering {}".format(GetConditionName())

classEnum = stat_level_marshal
classSpecModule = __import__('class083_marshal')

###################################################

########## Python Action ID's ##########
pythonActionToggleAuraId = 8301 
pythonActionAdrenalineId = 8302
########################################


#### standard callbacks - BAB and Save values
def OnGetToHitBonusBase(attachee, args, evt_obj):
    classLvl = attachee.stat_level_get(classEnum)
    babvalue = game.get_bab_for_class(classEnum, classLvl)
    evt_obj.bonus_list.add(babvalue, 0, 137) # untyped, description: "Class"
    return 0

def OnGetSaveThrowFort(attachee, args, evt_obj):
    value = char_class_utils.SavingThrowLevel(classEnum, attachee, D20_Save_Fortitude)
    evt_obj.bonus_list.add(value, 0, 137)
    return 0

def OnGetSaveThrowReflex(attachee, args, evt_obj):
    value = char_class_utils.SavingThrowLevel(classEnum, attachee, D20_Save_Reflex)
    evt_obj.bonus_list.add(value, 0, 137)
    return 0

def OnGetSaveThrowWill(attachee, args, evt_obj):
    value = char_class_utils.SavingThrowLevel(classEnum, attachee, D20_Save_Will)
    evt_obj.bonus_list.add(value, 0, 137)
    return 0

classSpecObj = PythonModifier(GetConditionName(), 2) #minorAuraEnum, majorAuraEnum
classSpecObj.AddHook(ET_OnToHitBonusBase, EK_NONE, OnGetToHitBonusBase, ())
classSpecObj.AddHook(ET_OnSaveThrowLevel, EK_SAVE_FORTITUDE, OnGetSaveThrowFort, ())
classSpecObj.AddHook(ET_OnSaveThrowLevel, EK_SAVE_REFLEX, OnGetSaveThrowReflex, ())
classSpecObj.AddHook(ET_OnSaveThrowLevel, EK_SAVE_WILL, OnGetSaveThrowWill, ())

#### Marshal Class Mechanics

## Get targets for Aura or Adrenaline Boost Effects

def getTargets(attachee, effectRadius):
    effectRadius = effectRadius + (attachee.radius / 12.0)
    crittersInRange = game.obj_list_cone(attachee, OLC_CRITTERS, effectRadius, 0, 360)
    targetList = []
    for target in crittersInRange:
        isFriendly = target.is_friendly(attachee)
        isDeaf = target.d20_query(Q_Critter_Is_Deafened)
        isDead = target.d20_query(Q_Dead)
        isUnconscious = target.d20_query(Q_Unconscious)
        isIntelligentEnough = True if target.stat_level_get(stat_intelligence) >= 3 else False
        if isFriendly and isIntelligentEnough and not isDead and not isUnconscious and not isDeaf:
            targetList.append(target)
    return targetList

## Major and Minor Aura Bonus

def getMajorAuraBonus(attachee):
    classLevel = attachee.stat_level_get(classEnum)
    if classLevel < 7:
        return 1
    elif classLevel < 14:
        return 2
    elif classLevel < 20:
        return 3
    return 4

def getMinorAuraBonus(attachee):
    #auraBonus can't be lower than 0
    charismaValue = attachee.stat_level_get(stat_charisma)
    auraBonus = int((charismaValue -10)/2)
    return max(auraBonus, 0)

## Auras

def auraRadial(attachee, args, evt_obj):
    auraRadialIdList = []

    #Add the top level menu
    radialParentMinor = tpdp.RadialMenuEntryParent("Minor Aura")
    radialParentMinorId = radialParentMinor.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)

    radialParentMajor = tpdp.RadialMenuEntryParent("Major Aura")
    radialParentMajorId = radialParentMajor.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)

    #Add aura childs
    for auraEnum, auraName in aura_utils.auraDict.items():
        if attachee.has_feat(auraName):
            auraName = auraName.split(" ", 2)
            auraName = str(auraName[2])
            #Enum start for Major Auras
            if auraEnum < 61:
                auraRadialId = tpdp.RadialMenuEntryPythonAction("Activate {}".format(auraName), D20A_PYTHON_ACTION, pythonActionToggleAuraId, auraEnum, "TAG_CLASS_FEATURES_MARSHAL_MINOR_AURAS")
                auraRadialId.add_as_child(attachee, radialParentMinorId)
            else:
                auraRadialId = tpdp.RadialMenuEntryPythonAction("Activate {}".format(auraName), D20A_PYTHON_ACTION, pythonActionToggleAuraId, auraEnum, "TAG_CLASS_FEATURES_MARSHAL_MAJOR_AURAS")
                auraRadialId.add_as_child(attachee, radialParentMajorId)

    #Add dismiss childs
    dismissMinorAuraId = tpdp.RadialMenuEntryPythonAction("Dismiss", D20A_PYTHON_ACTION, pythonActionToggleAuraId, -1, "TAG_CLASS_FEATURES_MARSHAL_MINOR_AURAS")
    dismissMinorAuraId.add_as_child(attachee, radialParentMinorId)

    dismissMajorAuraId = tpdp.RadialMenuEntryPythonAction("Dismiss", D20A_PYTHON_ACTION, pythonActionToggleAuraId, -2, "TAG_CLASS_FEATURES_MARSHAL_MAJOR_AURAS")
    dismissMajorAuraId.add_as_child(attachee, radialParentMajorId)
    return 0

def toggleAura(attachee, args, evt_obj):
    auraEnum = evt_obj.d20a.data1
    duration = 1
    if auraEnum >= 0:
        auraName = aura_utils.auraDict.get(auraEnum)
    #Deactivate Minor Aura
    if auraEnum == -1:
        attachee.float_text_line("Minor Aura dismissed")
        targetList = getTargets(attachee, 120.0)
        for target in targetList:
            target.d20_send_signal("S_Marshal_Minor_Aura_End")
        args.set_arg(0, 0)
    #Deactivate Major Aura
    elif auraEnum == -2:
        attachee.float_text_line("Major Aura dismissed")
        targetList = getTargets(attachee, 120.0)
        for target in targetList:
            target.d20_send_signal("S_Marshal_Major_Aura_End")
        args.set_arg(1, 0)
    #Toggle Minor Aura
    elif auraEnum < 61:
        targetList = getTargets(attachee, 60.0)
        auraBonus = getMinorAuraBonus(attachee)
        for target in targetList:
            target.d20_send_signal("S_Marshal_Minor_Aura_End")
            target.float_text_line("{}".format(auraName))
            target.condition_add_with_args("{}".format(auraName), duration, auraBonus, auraEnum)
        args.set_arg(0, auraEnum)
    #Toggle Major Aura
    else:
        targetList = getTargets(attachee, 60.0)
        auraBonus = getMajorAuraBonus(attachee)
        for target in targetList:
            target.d20_send_signal("S_Marshal_Major_Aura_End")
            target.float_text_line("{}".format(auraName))
            target.condition_add_with_args("{}".format(auraName), duration, auraBonus, auraEnum)
        args.set_arg(1, auraEnum)
    return 0

def dismissOnRest(attachee, args, evt_obj):
    targetList = getTargets(attachee, 60.0)
    for target in targetList:
        target.d20_send_signal("S_Marshal_Minor_Aura_End")
        target.d20_send_signal("S_Marshal_Major_Aura_End")
    args.set_arg(0, 0)
    args.set_arg(1, 0)
    return 0

def auraBeginRound(attachee, args, evt_obj):
    auraEnumMinor = args.get_arg(0)
    auraEnumMajor = args.get_arg(1)
    duration = 1
    if auraEnumMinor:
        targetList = getTargets(attachee, 60.0)
        for target in targetList:
            auraName = aura_utils.auraDict.get(auraEnumMinor)
            auraBonus = getMinorAuraBonus(attachee)
            target.condition_add_with_args("{}".format(auraName), duration, auraBonus, auraEnumMinor)
    if auraEnumMajor:
        targetList = getTargets(attachee, 60.0)
        for target in targetList:
            auraName = aura_utils.auraDict.get(auraEnumMajor)
            auraBonus = getMajorAuraBonus(attachee)
            target.condition_add_with_args("{}".format(auraName), duration, auraBonus, auraEnumMajor)
    return 0

def onConditionPreActions(attachee, args, evt_obj):
    #Deactivate Aura if specific conditions are added
    #panicked & fascinated missing
    #Basically all conditions that prohibit communication will end the auras
    if (evt_obj.is_modifier("Unconscious")
    or evt_obj.is_modifier("Dead")
    or evt_obj.is_modifier("sp-Silence")
    or evt_obj.is_modifier("Held")
    or evt_obj.is_modifier("sp-Daze")
    or evt_obj.is_modifier("Nauseated Condition")
    or evt_obj.is_modifier("Paralyzed")
    or evt_obj.is_modifier("Stunned")):
        if args.get_arg(0):
            targetList = getTargets(attachee, 120.0)
            for target in targetList:
                target.d20_send_signal("S_Marshal_Minor_Aura_End")
            args.set_arg(0, 0)
        if args.get_arg(1):
            targetList = getTargets(attachee, 120.0)
            for target in targetList:
                target.d20_send_signal("S_Marshal_Major_Aura_End")
            args.set_arg(1, 0)
    return 0

classSpecObj.AddHook(ET_OnBuildRadialMenuEntry , EK_NONE, auraRadial, ())
classSpecObj.AddHook(ET_OnD20PythonActionPerform, pythonActionToggleAuraId, toggleAura, ())
classSpecObj.AddHook(ET_OnBeginRound, EK_NONE, auraBeginRound, ())
classSpecObj.AddHook(ET_OnConditionAddPre, EK_NONE, onConditionPreActions, ())
classSpecObj.AddHook(ET_OnNewDay, EK_NEWDAY_REST, dismissOnRest, ())
#classSpecObj.AddHook(ET_OnD20Signal, EK_S_Teleport_Reconnect, dismissOnRest, ())

## Adrenaline Boost Alternate Class Feature

def adrenalineBoostRadial(attachee, args, evt_obj):
    #Add the top level menu
    radialParentAdrenalineId = tpdp.RadialMenuEntryPythonAction("Adrenaline Boost ({}/{})".format(args.get_arg(0), args.get_arg(1)), D20A_PYTHON_ACTION, pythonActionAdrenalineId, 0, "TAG_CLASS_FEATURES_MARSHAL_ADRENALINE_BOOST")
    radialParentAdrenalineId.add_as_child(attachee, tpdp.RadialMenuStandardNode.Class)
    return 0

def resetBoostsToMax(attachee, args, evt_obj):
    classLevel = attachee.stat_level_get(classEnum)
    maxUses = classLevel/4
    args.set_arg(0, maxUses)
    args.set_arg(1, maxUses)
    return 0

def activateAdrenalineBoost(attachee, args, evt_obj):
    chargesLeft = args.get_arg(0)
    if chargesLeft < 1:
        attachee.float_text_line("Out of charges", tf_red)
    else:
        classLevel = attachee.stat_level_get(classEnum)
        tempHp = classLevel
        duration = classLevel * 10
        #Adrenaline has only half range of Auras
        targetList = getTargets(attachee, 30.0)
        if targetList:
            #generate new spell_id
            spellId = tpactions.get_new_spell_id()
            for target in targetList:
                #Adrenaline does not work on self
                if not target == attachee:
                    game.particles('sp-Cure Minor Wounds', target)
                    target.float_text_line("Adrenaline Boost")
                    target.condition_add_with_args("Adrenaline Boost Condition", spellId, duration, tempHp)
        chargesLeft -= 1
        args.set_arg(0, chargesLeft)
    return 0

adrenalineBoost = PythonModifier("Adrenaline Boost Feat", 2) #chargesLeft, maxUses
adrenalineBoost.MapToFeat("Marshal Adrenaline Boost")
adrenalineBoost.AddHook(ET_OnBuildRadialMenuEntry , EK_NONE, adrenalineBoostRadial, ())
adrenalineBoost.AddHook(ET_OnNewDay, EK_NEWDAY_REST, resetBoostsToMax, ())
adrenalineBoost.AddHook(ET_OnConditionAdd, EK_NONE, resetBoostsToMax, ())
adrenalineBoost.AddHook(ET_OnD20PythonActionPerform, pythonActionAdrenalineId, activateAdrenalineBoost, ())

def adrenalineBoostEffectOnConditionPreActions(attachee, args, evt_obj):
    #Adrenaline Boost does not stack with itself.
    #If used again while old Boost is active
    #tempHP will be reset; this is done by removing
    #the old condition and apply the newer one
    if evt_obj.is_modifier("Adrenaline Boost Condition"):
        evt_obj.return_val = 1
        args.condition_remove()
    return 0

def adrenalineBoostEffectOnConditionAddActions(attachee, args, evt_obj):
    #Adrenaline Boost TempHP are doubled if target is at or below half HP
    currentHp = attachee.stat_level_get(stat_hp_current)
    maxHp = attachee.stat_level_get(stat_hp_max)
    tempHp = args.get_arg(2)
    if (currentHp * 2) <= maxHp:
        tempHp *= 2
    attachee.condition_add_with_args('Temporary_Hit_Points', args.get_arg(0), args.get_arg(1), tempHp)
    return 0

def adrenalineBoostEffectBeginRound(attachee, args, evt_obj):
    args.set_arg(1, args.get_arg(1)-evt_obj.data1) # Ticking down duration
    if args.get_arg(1) < 0:
        args.condition_remove()
    return 0

def adrenalineBoostRemoveTempHp(attachee, args, evt_obj):
    attachee.d20_send_signal(S_Spell_End, args.get_arg(0))
    return 0

adrenalineBoostEffect = PythonModifier("Adrenaline Boost Condition", 3, False) #spell_id, duration, tempHp
adrenalineBoostEffect.AddHook(ET_OnConditionAddPre , EK_NONE, adrenalineBoostEffectOnConditionPreActions, ())
adrenalineBoostEffect.AddHook(ET_OnConditionAdd, EK_NONE, adrenalineBoostEffectOnConditionAddActions, ())
adrenalineBoostEffect.AddHook(ET_OnBeginRound, EK_NONE, adrenalineBoostEffectBeginRound, ())
adrenalineBoostEffect.AddHook(ET_OnConditionRemove, EK_NONE, adrenalineBoostRemoveTempHp, ())
adrenalineBoostEffect.AddHook(ET_OnD20Signal, EK_S_Temporary_Hit_Points_Removed, adrenalineBoostRemoveTempHp, ())
