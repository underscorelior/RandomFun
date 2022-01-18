import discord
async def permcheck(perm):
	prm = discord.Permissions(perm)
	perms = ""
	if prm.administrator == True:
		perms += "Administrator "
	if prm.ban_members == True:
		perms += "Ban Members "
	if prm.kick_members == True:
		perms += "Kick Members "
	if prm.manage_nicknames == True:
		perms += "Manage Nicknames "
	if prm.manage_roles == True:
		perms += "Manage Roles "
	if prm.manage_messages == True:
		perms += " Manage Messages "

	if prm.manage_guild == True:
		perms += "Manage Guild/Server "
	if prm.manage_channels == True:
		perms += "Manage Channels "
	if prm.manage_webhooks == True:
		perms += "Manage Webhooks "
	if prm.manage_emojis == True:
		perms += "Manage Emojis "
	if prm.manage_permissions == True:
		perms += "Manage Permissions "

	if prm.view_audit_log == True:
		perms += "View Audit Log "
	if prm.mention_everyone == True:
		perms += "Mention Everyone/Here "
	if prm.move_members == True:
		perms += "Move Members "
	if prm.mute_members == True:
		perms += "Mute Members "
	if prm.deafen_members == True:
		perms += "Deafen Members "
	if perms == "":
		perms = "None"
	return perms