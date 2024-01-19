from asyncio.tasks import sleep
import Main
import discord
client = discord.Client()
ls1 = list()
ls2 = list()
ls3 = list()
i=0
with open("TwitterLinks_A17.txt") as file:
    for line in file:
        ls1.append(line)

with open("TwitterLinks_GokuBlack.txt") as file:
    for line in file:
        ls2.append(line)

with open("TwitterLinks_GokuBlue.txt") as file:
    for line in file:
        ls3.append(line)
  
while(i<0):
    lb1 = list()
    lb2 = list()
    lb3 = list()
    with open("TwitterLinks_A17.txt") as file:
        if(ls1[0]!=file.readline()):
            Main.send_Link("TwitterLinks_A17.txt", client.get_channel(888376010519740457), client.get_channel(888376010519740457).history(limit=None))

    with open("TwitterLinks_GokuBlack.txt") as file:
        if(ls2[0]!=file.readline()):
            Main.send_Link("TwitterLinks_GokuBlack.txt", client.get_channel(890631861099970631), client.get_channel(890631861099970631).history(limit=None))

    with open("TwitterLinks_GokuBlue.txt") as file:
        if(ls3[0]!=file.readline()):
            Main.send_Link("TwitterLinks_GokuBlue.txt", client.get_channel(890634130390409256), client.get_channel(890634130390409256).history(limit=None))
    sleep(2)
