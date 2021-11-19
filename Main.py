import discord
client = discord.Client()

def exe(file,channel_id,token):

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


    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))
        history1 = await view_history(await client.get_channel(channel_id).history(limit=None).flatten())
        await send_Link(file, client.get_channel(channel_id), history1)
        print('Sent links')
        await client.close()
    client.run(token)
