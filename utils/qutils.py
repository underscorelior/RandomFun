import discord
from discord_components import Button, ButtonStyle
import random

async def winbtn(wch):
    if wch == 1: 
        btnwn=[[Button(emoji="🇦",style=ButtonStyle.green,disabled=True),Button(emoji='🇧',style=ButtonStyle.grey,disabled=True),Button(emoji="🇨",style=ButtonStyle.grey,disabled=True),Button(emoji='🇩',style=ButtonStyle.grey,disabled=True)]]
    if wch == 2: 
        btnwn=[[Button(emoji="🇦",style=ButtonStyle.grey,disabled=True),Button(emoji='🇧',style=ButtonStyle.green,disabled=True),Button(emoji="🇨",style=ButtonStyle.grey,disabled=True),Button(emoji='🇩',style=ButtonStyle.grey,disabled=True)]]
    if wch == 3: 
        btnwn=[[Button(emoji="🇦",style=ButtonStyle.grey,disabled=True),Button(emoji='🇧',style=ButtonStyle.grey,disabled=True),Button(emoji="🇨",style=ButtonStyle.green,disabled=True),Button(emoji='🇩',style=ButtonStyle.grey,disabled=True)]]
    if wch == 4: 
        btnwn=[[Button(emoji="🇦",style=ButtonStyle.grey,disabled=True),Button(emoji='🇧',style=ButtonStyle.grey,disabled=True),Button(emoji="🇨",style=ButtonStyle.grey,disabled=True),Button(emoji='🇩',style=ButtonStyle.green,disabled=True)]]
    return btnwn

async def losebtn(chans, rans):
    if chans == 1:
        chbtn = Button(emoji="🇦",style=ButtonStyle.red,disabled=True)
    if chans == 2:
        chbtn = Button(emoji="🇧",style=ButtonStyle.red,disabled=True)
    if chans == 3:
        chbtn = Button(emoji="🇨",style=ButtonStyle.red,disabled=True)
    if chans == 4:
        chbtn = Button(emoji="🇩",style=ButtonStyle.red,disabled=True)
    if rans == 1: 
        rbtn = Button(emoji="🇦",style=ButtonStyle.green,disabled=True)
        if chans == 2:
            btnls = [[rbtn,chbtn,Button(emoji="🇨",style=ButtonStyle.grey,disabled=True),Button(emoji='🇩',style=ButtonStyle.grey,disabled=True)]]
        if chans == 3:
            btnls = [[rbtn,Button(emoji="🇧",style=ButtonStyle.grey,disabled=True),chbtn,Button(emoji='🇩',style=ButtonStyle.grey,disabled=True)]]
        if chans == 4:
            btnls = [[rbtn,Button(emoji="🇧",style=ButtonStyle.grey,disabled=True),Button(emoji='🇨',style=ButtonStyle.grey,disabled=True),chbtn]]
    if rans == 2: 
        rbtn = Button(emoji="🇧",style=ButtonStyle.green,disabled=True)
        if chans == 1:
            btnls = [[chbtn,rbtn,Button(emoji="🇨",style=ButtonStyle.grey,disabled=True),Button(emoji='🇩',style=ButtonStyle.grey,disabled=True)]]
        if chans == 3:
            btnls = [[Button(emoji="🇦",style=ButtonStyle.grey,disabled=True),rbtn,chbtn,Button(emoji='🇩',style=ButtonStyle.grey,disabled=True)]]
        if chans == 4:
            btnls = [[Button(emoji="🇦",style=ButtonStyle.grey,disabled=True),rbtn,Button(emoji='🇨',style=ButtonStyle.grey,disabled=True),chbtn]]
    if rans == 3: 
        rbtn = Button(emoji="🇨",style=ButtonStyle.green,disabled=True)
        if chans == 1:
            btnls = [[chbtn,Button(emoji="🇧",style=ButtonStyle.grey,disabled=True),rbtn,Button(emoji='🇩',style=ButtonStyle.grey,disabled=True)]]
        if chans == 2:
            btnls = [[Button(emoji="🇦",style=ButtonStyle.grey,disabled=True),chbtn,rbtn,Button(emoji='🇩',style=ButtonStyle.grey,disabled=True)]]
        if chans == 4:
            btnls = [[Button(emoji="🇦",style=ButtonStyle.grey,disabled=True),Button(emoji='🇧',style=ButtonStyle.grey,disabled=True),rbtn,chbtn]]
    if rans == 4: 
        rbtn = Button(emoji="🇩",style=ButtonStyle.green,disabled=True)
        if chans == 1:
            btnls = [[chbtn,Button(emoji="🇧",style=ButtonStyle.grey,disabled=True),Button(emoji='🇨',style=ButtonStyle.grey,disabled=True),rbtn]]
        if chans == 2:
            btnls = [[Button(emoji="🇦",style=ButtonStyle.grey,disabled=True),chbtn,Button(emoji='🇨',style=ButtonStyle.grey,disabled=True),rbtn]]
        if chans == 3:
            btnls = [[Button(emoji="🇦",style=ButtonStyle.grey,disabled=True),Button(emoji='🇧',style=ButtonStyle.grey,disabled=True),chbtn,rbtn]]

    return btnls,chans,rans

async def checkans(data, ansloc, quizans, type):
	x=True
	while x is True:
		if ansloc == 1:
			qa = quizans[type]
			qb = data[random.randint(0,len(data))][type]
			qc = data[random.randint(0,len(data))][type]
			qd = data[random.randint(0,len(data))][type]
		if ansloc == 2:
			qa = data[random.randint(0,len(data))][type]
			qb = quizans[type]
			qc = data[random.randint(0,len(data))][type]
			qd = data[random.randint(0,len(data))][type]
		if ansloc == 3: 
			qa = data[random.randint(0,len(data))][type]
			qb = data[random.randint(0,len(data))][type]
			qc = quizans[type]
			qd = data[random.randint(0,len(data))][type]
		if ansloc == 4: 
			qa = data[random.randint(0,len(data))][type]
			qb = data[random.randint(0,len(data))][type]
			qc = data[random.randint(0,len(data))][type]
			qd = quizans[type]
		if qa == qb or qa == qc or qa== qb: x=True
		else: x=False
	return qa,qb,qc,qd