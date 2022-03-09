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

async def losebtn(ctx, chans, rans):
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


async def checkansc(data, ansloc,quizans):
	x=False
	while x != True:
		try:
			if ansloc == 1:
				qa = quizans["capital"][0]
				qb = data[random.randint(0,len(data))]["capital"][0]
				qc = data[random.randint(0,len(data))]["capital"][0]
				qd = data[random.randint(0,len(data))]["capital"][0]
			if ansloc == 2:
				qa = data[random.randint(0,len(data))]["capital"][0]
				qb = quizans["capital"][0]
				qc = data[random.randint(0,len(data))]["capital"][0]
				qd = data[random.randint(0,len(data))]["capital"][0]
			if ansloc == 3: 
				qa = data[random.randint(0,len(data))]["capital"][0]
				qb = data[random.randint(0,len(data))]["capital"][0]
				qc = quizans["capital"][0]
				qd = data[random.randint(0,len(data))]["capital"][0]
			if ansloc == 4: 
				qa = data[random.randint(0,len(data))]["capital"][0]
				qb = data[random.randint(0,len(data))]["capital"][0]
				qc = data[random.randint(0,len(data))]["capital"][0]
				qd = quizans["capital"][0]
		except IndexError:
			pass
	return qa,qb,qc,qd
async def checkansf(data, ansloc,quizans):
	x=False
	while x != True:
		try:
			if ansloc == 1: 
				qa = quizans["name"]["common"]
				qb = data[random.randint(0,len(data))]["name"]["common"]
				qc = data[random.randint(0,len(data))]["name"]["common"]
				qd = data[random.randint(0,len(data))]["name"]["common"]
			if ansloc == 2:
				qa = data[random.randint(0,len(data))]["name"]["common"]
				qb = quizans["name"]["common"]
				qc = data[random.randint(0,len(data))]["name"]["common"]
				qd = data[random.randint(0,len(data))]["name"]["common"]
			if ansloc == 3: 
				qa = data[random.randint(0,len(data))]["name"]["common"]
				qb = data[random.randint(0,len(data))]["name"]["common"]
				qc = quizans["name"]["common"]
				qd = data[random.randint(0,len(data))]["name"]["common"]
			if ansloc == 4: 
				qa = data[random.randint(0,len(data))]["name"]["common"]
				qb = data[random.randint(0,len(data))]["name"]["common"]
				qc = data[random.randint(0,len(data))]["name"]["common"]
				qd = quizans["name"]["common"]
		except IndexError:
			pass
	return qa,qb,qc,qd