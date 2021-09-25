import os
import discord

from DBManager import DBManager

TOKEN = os.getenv('DISCORD_TOKEN')
WELCOME_CHANNEL = 'bienvenidos'

client = discord.Client()

db_manager = DBManager()
conn = db_manager.get_conn()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_member_join(member):
    channels = member.guild.channels

    for channel in channels:
        if channel.name == WELCOME_CHANNEL:
            await channel.send(f"Bienvenido {member.mention}, gracias ")


@client.event
async def on_message(message):
    if message.content == "$set_welcome_channel":

        roles = message.author.roles

        for role in roles:
            if role.permissions.administrator:
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM EspecialChannel WHERE type = 'welcome';")
                result = cursor.fetchall()

                if not result:
                    cursor.execute("INSERT INTO EspecialChannel (guild_id,channel_id,type,name) VALUES (%s,%s,%s,%s)",
                                   (
                                       str(message.guild.id),
                                       str(message.channel.id),
                                       "welcome",
                                       message.channel.name)
                                   )

                else:
                    cursor.execute("""UPDATE EspecialChannel 
                                        SET guild_id = %s, 
                                        channel_id = %s,
                                        type = %s,
                                        name = %s
                                        WHERE id = %s
                                        """,
                                   (
                                       str(message.guild.id),
                                       str(message.channel.id),
                                       "welcome",
                                       message.channel.name,
                                       result[0][0]
                                   ))
                conn.commit()

                await message.channel.send("Channel has been set as welcome channel")


client.run(TOKEN)
