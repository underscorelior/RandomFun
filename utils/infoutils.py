import discord

def format_seconds(time_seconds):
    """Formats some number of seconds into a string of format d days, x hours, y minutes, z seconds"""
    seconds = time_seconds
    hours = 0
    minutes = 0
    days = 0
    while seconds >= 60:
        if seconds >= 60 * 60 * 24:
            seconds -= 60 * 60 * 24
            days += 1
        elif seconds >= 60 * 60:
            seconds -= 60 * 60
            hours += 1
        elif seconds >= 60:
            seconds -= 60
            minutes += 1

    return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
async def permcheck(perm):
    prm = discord.Permissions(perm)
    perms = ""
    if prm.administrator:
        perms += "Administrator "
    if prm.ban_members:
        perms += "Ban Members "
    if prm.kick_members:
        perms += "Kick Members "
    if prm.manage_nicknames:
        perms += "Manage Nicknames "
    if prm.manage_roles:
        perms += "Manage Roles "
    if prm.manage_messages:
        perms += " Manage Messages "

    if prm.manage_guild:
        perms += "Manage Guild/Server "
    if prm.manage_channels:
        perms += "Manage Channels "
    if prm.manage_webhooks:
        perms += "Manage Webhooks "
    if prm.manage_emojis:
        perms += "Manage Emojis "
    if prm.manage_permissions:
        perms += "Manage Permissions "

    if prm.view_audit_log:
        perms += "View Audit Log "
    if prm.mention_everyone:
        perms += "Mention Everyone/Here "
    if prm.move_members:
        perms += "Move Members "
    if prm.mute_members:
        perms += "Mute Members "
    if prm.deafen_members:
        perms += "Deafen Members "
    if perms == "":
        perms = "None"
    return perms