import discord
from decouple import config
client = discord.Client()

async def view_history(history):
    ls = list()
    for message in history:
        ls.append(message)
    return ls


async def send_Link(filename, channel, history):
    flag = True
    ls = await view_history(history)
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            for message in ls:
                print(message.content,message.created_at)
                if(message.content + '\n' == line or message.content == line):
                    flag = False
                    break
            if(flag == True):
               await channel.send(line)
            flag = True


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    history1 = await view_history(await client.get_channel(888376010519740457).history(limit=None).flatten())
    history2 = await view_history(await client.get_channel(890631861099970631).history(limit=None).flatten())
    history3 = await view_history(await client.get_channel(890634130390409256).history(limit=None).flatten())
    await send_Link("TwitterLinks_A17.txt", client.get_channel(888376010519740457),history1)
    await send_Link("TwitterLinks_GokuBlack.txt", client.get_channel(890631861099970631), history2)
    await send_Link("TwitterLinks_GokuBlue.txt", client.get_channel(890634130390409256), history3)


client.run(config('TOKEN'))
