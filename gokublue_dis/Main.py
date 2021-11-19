import discord

client = discord.Client()

### by default its set to 17 channel and file

idd = 888376010519740457 
file = "/home/master/discord/TwitterLinks_A17.txt"

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
                if(message.content + '\n' == line or message.content == line):
                    flag = False
                    break
            if(flag == True):
                await channel.send(line)
            flag = True

   
def char(ident,name):
    global idd, file
    idd = ident
    file = name

@client.event
async def on_ready():
    print('We have logged in as {0.user},{1},{2}'.format(client,idd,file))
    history1 = await view_history(await client.get_channel(idd).history(limit=None).flatten())
    await send_Link(file, client.get_channel(idd), history1)
    await client.close()

if __name__ == '__main__':
    client.run('ODg4MzczNjAyNzQxODAwOTcy.YURwZA.Eh22NZT0w5BR5BwoP8-EbYCxHFc')
