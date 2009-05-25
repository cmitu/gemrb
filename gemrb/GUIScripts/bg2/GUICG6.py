# GemRB - Infinity Engine Emulator
# Copyright (C) 2003 The GemRB Project
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# $Id$
#
#character generation, (thief) skills (GUICG6)
import GemRB

SkillWindow = 0
TextAreaControl = 0
DoneButton = 0
SkillTable = 0
TopIndex = 0
PointsLeft = 0
RowCount = 0
ClickCount = 0
OldDirection = 0
OldPos = 0
AvailableSkillIndices = []

def RedrawSkills(direction):
	global TopIndex, OldDirection, ClickCount

	if PointsLeft == 0:
		DoneButton.SetState(IE_GUI_BUTTON_ENABLED)

	SumLabel = SkillWindow.GetControl(0x10000005)
	SumLabel.SetText(str(PointsLeft) )

	for i in range(4):
		if len(AvailableSkillIndices) <= i:
			Label = SkillWindow.GetControl (0x10000001+i)
			Label.SetText ("")
			Button1 = SkillWindow.GetControl(i*2+11)
			Button1.SetState(IE_GUI_BUTTON_DISABLED)
			Button1.SetFlags(IE_GUI_BUTTON_NO_IMAGE,OP_OR)
			Button2 = SkillWindow.GetControl(i*2+12)
			Button2.SetState(IE_GUI_BUTTON_DISABLED)
			Button2.SetFlags(IE_GUI_BUTTON_NO_IMAGE,OP_OR)
			Label = SkillWindow.GetControl(0x10000006+i)
			Label.SetText("")
			continue

		Pos = AvailableSkillIndices[TopIndex+i]

		SkillName = SkillTable.GetValue(Pos+2,1)
		Label = SkillWindow.GetControl(0x10000006+i)
		Label.SetText(SkillName)

		SkillName=SkillTable.GetRowName(Pos+2)
		Ok=SkillTable.GetValue(SkillName, KitName)
		Button1 = SkillWindow.GetControl(i*2+11)
		Button2 = SkillWindow.GetControl(i*2+12)
		if Ok == -1:
			Button1.SetState(IE_GUI_BUTTON_DISABLED)
			Button2.SetState(IE_GUI_BUTTON_DISABLED)
			Button1.SetFlags(IE_GUI_BUTTON_NO_IMAGE,OP_OR)
			Button2.SetFlags(IE_GUI_BUTTON_NO_IMAGE,OP_OR)
		else:
			Button1.SetState(IE_GUI_BUTTON_ENABLED)
			Button2.SetState(IE_GUI_BUTTON_ENABLED)
			Button1.SetFlags(IE_GUI_BUTTON_NO_IMAGE,OP_NAND)
			Button2.SetFlags(IE_GUI_BUTTON_NO_IMAGE,OP_NAND)

		Label = SkillWindow.GetControl(0x10000001+i)
		ActPoint = GemRB.GetVar("Skill "+str(Pos) )
		Label.SetText(str(ActPoint) )

	if direction:
		if OldDirection == direction:
			ClickCount = ClickCount + 1
			if ClickCount>20:
				GemRB.SetRepeatClickFlags(GEM_RK_DOUBLESPEED, OP_OR)
			return

	OldDirection = direction
	ClickCount = 0
	GemRB.SetRepeatClickFlags(GEM_RK_DOUBLESPEED, OP_NAND)
	return

def ScrollBarPress():
	global TopIndex

	TopIndex = GemRB.GetVar("TopIndex")
	RedrawSkills(0)
	return

def OnLoad():
	global SkillWindow, TextAreaControl, DoneButton, TopIndex
	global SkillTable, PointsLeft, KitName, RowCount, AvailableSkillIndices
	
	SkillTable = GemRB.LoadTableObject("skills")
	RowCount = SkillTable.GetRowCount()-2

	Kit = GemRB.GetVar("Class Kit")
	if Kit != 0:
		KitList = GemRB.LoadTableObject("kitlist")
		KitName = KitList.GetValue(Kit, 0) #rowname is just a number
		PointsLeft = SkillTable.GetValue("FIRST_LEVEL",KitName)
		if PointsLeft < 0:
			Kit = 0
		
	if Kit == 0:
		ClassTable = GemRB.LoadTableObject("classes")
		Class = GemRB.GetVar("Class")-1
		KitName = ClassTable.GetRowName(Class)
	else:
		KitList = GemRB.LoadTableObject("kitlist")
		KitName = KitList.GetValue(Kit, 0) #rowname is just a number

	# setup the indices/count of usable skills
	AvailableSkillIndices = []
	for i in range(SkillTable.GetRowCount()-2):
		SkillName = SkillTable.GetRowName (i+2)
		if SkillTable.GetValue (SkillName, KitName) != -1:
			AvailableSkillIndices.append(i)

	SkillRacTable = GemRB.LoadTableObject("SKILLRAC")
	RaceTable = GemRB.LoadTableObject("RACES")
	RaceName = RaceTable.GetRowName(GemRB.GetVar("Race")-1)

	Ok=0
	for i in range(RowCount):
		SkillName = SkillTable.GetRowName(i+2)
		if SkillTable.GetValue(SkillName, KitName)==1:
			b=SkillRacTable.GetValue(RaceName, SkillName)
			GemRB.SetVar("Skill "+str(i),b)
			GemRB.SetVar("SkillBase "+str(i), b)
			Ok=1
		else:
			GemRB.SetVar("Skill "+str(i),0)

	if Ok==0:  #skipping 
		GemRB.SetNextScript("GUICG9")
		return
	
	Level = GemRB.GetVar("Level")
	PointsLeft = SkillTable.GetValue("FIRST_LEVEL",KitName)
	if Level>1:
		PointsLeft = PointsLeft + SkillTable.GetValue("RATE",KitName)*(Level-1)

	GemRB.SetToken("number",str(PointsLeft) )

	GemRB.LoadWindowPack("GUICG", 640, 480)
	SkillTable = GemRB.LoadTableObject("skills")
	SkillWindow = GemRB.LoadWindowObject(6)

	if len(AvailableSkillIndices) > 4:
		GemRB.SetVar("TopIndex", 0)
		ScrollBarControl = SkillWindow.GetControl(26)
		ScrollBarControl.SetEvent(IE_GUI_SCROLLBAR_ON_CHANGE, "ScrollBarPress")
		#decrease it with the number of controls on screen (list size)
		ScrollBarControl.SetVarAssoc("TopIndex", RowCount-3)
		ScrollBarControl.SetDefaultScrollBar ()
	else:
		if len(AvailableSkillIndices):
			# autoscroll to the first valid skill; luckily all three monk ones are adjacent
			GemRB.SetVar("TopIndex", AvailableSkillIndices[0])

	for i in range(len(AvailableSkillIndices)):
		if i == 4:
				break
		Button = SkillWindow.GetControl(i+21)
		Button.SetVarAssoc("Skill",AvailableSkillIndices[i])
		Button.SetEvent(IE_GUI_BUTTON_ON_PRESS, "JustPress")

		Button = SkillWindow.GetControl(i*2+11)
		Button.SetVarAssoc("Skill",AvailableSkillIndices[i])
		Button.SetEvent(IE_GUI_BUTTON_ON_PRESS, "LeftPress")

		Button = SkillWindow.GetControl(i*2+12)
		Button.SetVarAssoc("Skill",AvailableSkillIndices[i])
		Button.SetEvent(IE_GUI_BUTTON_ON_PRESS, "RightPress")

	BackButton = SkillWindow.GetControl(25)
	BackButton.SetText(15416)
	BackButton.SetFlags (IE_GUI_BUTTON_CANCEL, OP_OR)
	DoneButton = SkillWindow.GetControl(0)
	DoneButton.SetText(11973)
	DoneButton.SetFlags(IE_GUI_BUTTON_DEFAULT,OP_OR)

	TextAreaControl = SkillWindow.GetControl(19)
	TextAreaControl.SetText(17248)

	DoneButton.SetEvent(IE_GUI_BUTTON_ON_PRESS,"NextPress")
	BackButton.SetEvent(IE_GUI_BUTTON_ON_PRESS,"BackPress")
	DoneButton.SetState(IE_GUI_BUTTON_DISABLED)
	TopIndex = 0
	RedrawSkills(0)
	SkillWindow.SetVisible(1)
	GemRB.SetRepeatClickFlags(GEM_RK_DISABLE, OP_NAND)
	return


def JustPress():
	Pos = GemRB.GetVar("Skill")+TopIndex
	TextAreaControl.SetText(SkillTable.GetValue(Pos+2,0) )
	return

def RightPress():
	global PointsLeft, ClickCount, OldPos

	Pos = GemRB.GetVar("Skill")+TopIndex
	TextAreaControl.SetText(SkillTable.GetValue(Pos+2,0) )
	ActPoint = GemRB.GetVar("Skill "+str(Pos) )
	BasePoint = GemRB.GetVar("SkillBase "+str(Pos) )
	if ActPoint <= 0 or ActPoint == BasePoint:
		return
	GemRB.SetVar("Skill "+str(Pos),ActPoint-1)
	PointsLeft = PointsLeft + 1
	if OldPos != Pos:
		OldPos = Pos
		ClickCount = 0

	RedrawSkills(2)
	return

def LeftPress():
	global PointsLeft, ClickCount, OldPos

	Pos = GemRB.GetVar("Skill")+TopIndex
	TextAreaControl.SetText(SkillTable.GetValue(Pos+2,0) )
	if PointsLeft == 0:
		return
	ActPoint = GemRB.GetVar("Skill "+str(Pos) )
	if ActPoint >= 200:
		return
	GemRB.SetVar("Skill "+str(Pos), ActPoint+1)
	PointsLeft = PointsLeft - 1
	if OldPos != Pos:
		OldPos = Pos
		ClickCount = 0

	RedrawSkills(1)
	return

def BackPress():
	if SkillWindow:
		SkillWindow.Unload()
	GemRB.SetNextScript("CharGen6")
	for i in range(RowCount):
		GemRB.SetVar("Skill "+str(i), 0)
	GemRB.SetRepeatClickFlags(GEM_RK_DISABLE, OP_OR)
	return

def NextPress():
	if SkillWindow:
		SkillWindow.Unload()
	GemRB.SetNextScript("GUICG9") #weapon proficiencies
	GemRB.SetRepeatClickFlags(GEM_RK_DISABLE, OP_OR)
	return
