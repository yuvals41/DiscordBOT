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
    await send_Link("TwitterLinks_A17.txt", client.get_channel('server id'), client.get_channel('server id').history(limit=None))
    await send_Link("TwitterLinks_GokuBlack.txt", client.get_channel('server id'), client.get_channel('server id').history(limit=None))
    await send_Link("TwitterLinks_GokuBlue.txt", client.get_channel('server id'), client.get_channel('server id').history(limit=None))


client.run('')
