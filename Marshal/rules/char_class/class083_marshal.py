from toee import *
import char_class_utils
import char_editor
###################################################

def GetConditionName(): # used by API
    return "Marshal"

def GetCategory():
    return "Miniatures Handbook Base Classes"

def GetClassDefinitionFlags():
    return CDF_BaseClass

def GetClassHelpTopic():
    return "TAG_MARSHALS"

classEnum = stat_level_marshal

###################################################

class_feats = {

1: (feat_armor_proficiency_light, feat_armor_proficiency_medium, feat_armor_proficiency_heavy, feat_shield_proficiency, feat_simple_weapon_proficiency, 
feat_martial_weapon_proficiency_all, feat_skill_focus_diplomacy,),
4: ("Marshal Adrenaline Boost",)
}

minor_auras = ["Minor Aura Accurate Strike", "Minor Aura Art of War", "Minor Aura Demand Fortitude", "Minor Aura Determined Caster", "Minor Aura Force of Will", 
"Minor Aura Master of Opportunity", "Minor Aura Master of Tactics", "Minor Aura Motivate Charisma", "Minor Aura Motivate Constitution", "Minor Aura Motivate Dexterity", 
"Minor Aura Motivate Intelligence", "Minor Aura Motivate Strength", "Minor Aura Motivate Wisdom", "Minor Aura Over the Top", "Minor Aura Watchful Eye"]

major_auras = ["Major Aura Hardy Soldiers", "Major Aura Motivate Ardor", "Major Aura Motivate Attack", "Major Aura Motivate Care", 
"Major Aura Motivate Urgency", "Major Aura Resilient Troops", "Major Aura Steady Hand"]

class_skills = (skill_bluff, skill_diplomacy, skill_handle_animal, skill_intimidate, skill_knowledge_all, skill_listen, skill_perform, skill_ride, skill_sense_motive, skill_spot, skill_wilderness_lore, skill_swim)

def IsEnabled():
    return 1

def GetHitDieType():
    return 8
    
def GetSkillPtsPerLevel():
    return 4
    
def GetBabProgression():
    return base_attack_bonus_type_semi_martial
    
def IsFortSaveFavored():
    return 1
    
def IsRefSaveFavored():
    return 0
    
def IsWillSaveFavored():
    return 1

def GetSpellListType():
    return spell_list_type_none

def IsClassSkill(skillEnum):
    return char_class_utils.IsClassSkill(class_skills, skillEnum)

def IsClassFeat(featEnum):
    return char_class_utils.IsClassFeat(class_feats, featEnum)

def GetClassFeats():
    return class_feats

def IsAlignmentCompatible(alignment):
    return 1

def ObjMeetsPrereqs(obj):
    return 1

def GetDeityClass():
    return stat_level_fighter

 ## Levelup

def auraLevelList(newLevel):
    majorAuraLevelList = [2, 5, 9, 14, 20]
    minorAuraLevelList = [1, 3, 6, 8, 10, 12, 15, 19] #Changed from 5, 7, 9 to 6, 8, 10 because 5 and 9 would be double extra feat
    if newLevel in minorAuraLevelList:
        auraType = 1
    elif newLevel in majorAuraLevelList:
        auraType = 2
    elif newLevel in minorAuraLevelList and newLevel in majorAuraLevelList: #if possible to grant more than one feat at once
        auraType = 4
    else:
        auraType = 0
    return auraType

def IsSelectingFeatsOnLevelup(obj):
    newLevel = obj.stat_level_get(classEnum) + 1
    getsAuraFeat = auraLevelList(newLevel)
    if getsAuraFeat:
        return 1
    return 0

def LevelupGetBonusFeats(obj):
    newLevel = obj.stat_level_get(classEnum) + 1
    auraType = auraLevelList(newLevel)
    auraList = []
    if auraType == 2:
        for aura in major_auras:
            auraInfo = char_editor.FeatInfo(aura)
            auraList.append(auraInfo)
    elif auraType == 1:
        for aura in minor_auras:
            auraInfo = char_editor.FeatInfo(aura)
            auraList.append(auraInfo)
    char_editor.set_bonus_feats(auraList)
    return

def LevelupSpellsFinalize( obj, classLvlNew = -1 ):
    return 0