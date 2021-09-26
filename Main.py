import discord

client = discord.Client()


async def send_Link(filename, channel, history):
    flag = True
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            async for message in history:
                if(message.content + "\n" == line or message.content == line):
                    flag = False
                    break
            if(flag == True):
                await channel.send(line)
            flag = True


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await send_Link("TwitterLinks_A17.txt", client.get_channel(888376010519740457), client.get_channel(888376010519740457).history(limit=None))
    await send_Link("TwitterLinks_GokuBlack.txt", client.get_channel(890631861099970631), client.get_channel(890631861099970631).history(limit=None))
    await send_Link("TwitterLinks_GokuBlue.txt", client.get_channel(890634130390409256), client.get_channel(890634130390409256).history(limit=None))


client.run('ODg4MzczNjAyNzQxODAwOTcy.YURwZA.gg1v3u3cJCqDMRSdcct4XHVnTKE')
