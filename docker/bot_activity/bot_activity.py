import os
import time
import requests
from discord.ext import commands, tasks

TOKEN = os.environ.get('TOKEN_activity')

bot = commands.Bot(command_prefix='/')
old_all_nodes_status_mainnet = []
old_all_nodes_status_devnet = []
old_list_healthy_mainnet = []
old_list_healthy_devnet = []
old_list_unhealthy_mainnet = []
old_list_unhealthy_devnet = []
flag_mainnet = 1
flag_devnet = 1

@bot.event
async def on_ready():
    global ctx_mainnet
    global ctx_devnet
    channel_id_mainnet = os.environ.get('CHANNEL_ID_MAINNET')
    channel_id_devnet = os.environ.get('CHANNEL_ID_DEVNET')
    ctx_mainnet = bot.get_channel(int(channel_id_mainnet))
    ctx_devnet = bot.get_channel(int(channel_id_devnet))
    await ctx_mainnet.send("Broadcasting pool state", delete_after=5)
    await ctx_devnet.send("Broadcasting pool state", delete_after=5)
    update.start()
    
@commands.has_permissions(administrator=True)
@bot.command()
async def clear(ctx, limit: int):
    await ctx.channel.purge(limit=limit)
    await ctx.send('Cleared by {}'.format(ctx.author.mention), delete_after=10)
    await ctx.message.delete()

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!", delete_after=10)

@tasks.loop(seconds=20)
async def update():
    global flag_mainnet
    global ctx_mainnet
    global old_all_nodes_status_mainnet
    global old_list_healthy_mainnet
    global old_list_unhealthy_mainnet
    list_nodes_mainnet = []
    list_healthy_mainnet = []
    list_unhealthy_mainnet = []
    print("Contacting Api")
    api = os.environ.get('API_URL')
    raw = requests.get(api) #gets the api request
    temp = raw.json()
    for i in temp:
        list_nodes_mainnet.append(i) #loops through the list of nodes and adds them to array

    all_nodes_status_mainnet = []
    y = 0
    for i in temp: #loops through the list of nodes and adds them to array
        shrt = temp[f'{list_nodes_mainnet[y]}']['dlt.green']['isMainnetHealthy']
        all_nodes_status_mainnet.append(shrt)
        y += 1
    if all_nodes_status_mainnet != old_all_nodes_status_mainnet: #
        print(f"all_nodes_status = {all_nodes_status_mainnet}")
        lie = all(all_nodes_status_mainnet) # checks if there is a False in the array
        if lie == False: #if there is a False in the array lie = False
            v = 0
            for i in temp: #loops through the list of nodes and adds them to array
                if temp[f'{list_nodes_mainnet[v]}']['dlt.green']['isMainnetHealthy'] is True:
                    shrt_healthy_mainnet = list_nodes_mainnet[v]
                    list_healthy_mainnet.append(shrt_healthy_mainnet)
                if temp[f'{list_nodes_mainnet[v]}']['dlt.green']['isMainnetHealthy'] is False:
                    shrt_unhealthy_mainnet = list_nodes_mainnet[v]
                    list_unhealthy_mainnet.append(shrt_unhealthy_mainnet)
                v += 1
            
            difference_healthy_mainnet = [x for x in list_healthy_mainnet if x not in old_list_healthy_mainnet]
            difference_unhealthy_mainnet = [x for x in list_unhealthy_mainnet if x not in old_list_unhealthy_mainnet]
            print(difference_healthy_mainnet)
            print(difference_unhealthy_mainnet)
            
            if flag_mainnet == 0:
                x = 0
                for i in difference_unhealthy_mainnet: #send all unhealthy nodes
                    await ctx_mainnet.send(f"```diff\n- {difference_unhealthy_mainnet[x]} is now unhealthy\n```", delete_after=172800)
                    x +=1
                    time.sleep(0.5)

                x = 0  
                for i in difference_healthy_mainnet: #send all healthy nodes
                    await ctx_mainnet.send(f"```yaml\n+ {difference_healthy_mainnet[x]} is now healthy\n```", delete_after=172800)
                    x +=1
                    time.sleep(0.5)
                x = 0
                old_list_healthy_mainnet = list_healthy_mainnet
                old_list_unhealthy_mainnet = list_unhealthy_mainnet
            else:
                old_list_healthy_mainnet = list_healthy_mainnet
                old_list_unhealthy_mainnet = list_unhealthy_mainnet
                
        if list_unhealthy_mainnet == []:
            await ctx_mainnet.send("```yaml\nAll nodes are healthy\n```", delete_after=172800)
    
      
    old_all_nodes_status_mainnet = all_nodes_status_mainnet
    
    print(flag_mainnet)
    print(list_healthy_mainnet)
    print(list_unhealthy_mainnet)
    print(list(old_list_healthy_mainnet))
    print(list(old_list_unhealthy_mainnet))
    flag_mainnet = 0

    global flag_devnet
    global ctx_devnet
    global old_all_nodes_status_devnet
    global old_list_healthy_devnet
    global old_list_unhealthy_devnet
    list_nodes_devnet = []
    list_healthy_devnet = []
    list_unhealthy_devnet = []
    for i in temp:
        list_nodes_devnet.append(i) #loops through the list of nodes and adds them to array

    all_nodes_status_devnet = []
    y = 0
    for i in temp: #loops through the list of nodes and adds them to array
        shrt = temp[f'{list_nodes_devnet[y]}']['dlt.green']['isDevnetHealthy']
        all_nodes_status_devnet.append(shrt)
        y += 1
    if all_nodes_status_devnet != old_all_nodes_status_devnet: #
        print(f"all_nodes_status = {all_nodes_status_devnet}")
        lie = all(all_nodes_status_devnet) # checks if there is a False in the array
        if lie == False: #if there is a False in the array lie = False
            v = 0
            for i in temp: #loops through the list of nodes and adds them to array
                if temp[f'{list_nodes_devnet[v]}']['dlt.green']['isDevnetHealthy'] is True:
                    shrt_healthy_devnet = list_nodes_devnet[v]
                    list_healthy_devnet.append(shrt_healthy_devnet)
                if temp[f'{list_nodes_devnet[v]}']['dlt.green']['isDevnetHealthy'] is False:
                    shrt_unhealthy_devnet = list_nodes_devnet[v]
                    list_unhealthy_devnet.append(shrt_unhealthy_devnet)
                v += 1
            
            difference_healthy_devnet = [x for x in list_healthy_devnet if x not in old_list_healthy_devnet]
            difference_unhealthy_devnet = [x for x in list_unhealthy_devnet if x not in old_list_unhealthy_devnet]
            print(difference_healthy_devnet)
            print(difference_unhealthy_devnet)
            
            if flag_devnet == 0:
                x = 0
                for i in difference_unhealthy_devnet: #send all unhealthy nodes
                    await ctx_devnet.send(f"```diff\n- {difference_unhealthy_devnet[x]} is now unhealthy\n```", delete_after=172800)
                    x +=1
                    time.sleep(0.5)

                x = 0  
                for i in difference_healthy_devnet: #send all healthy nodes
                    await ctx_devnet.send(f"```yaml\n+ {difference_healthy_devnet[x]} is now healthy\n```", delete_after=172800)
                    x +=1
                    time.sleep(0.5)
                x = 0
                old_list_healthy_devnet = list_healthy_devnet
                old_list_unhealthy_devnet = list_unhealthy_devnet
            else:
                old_list_healthy_devnet = list_healthy_devnet
                old_list_unhealthy_devnet = list_unhealthy_devnet
                
        if list_unhealthy_devnet == []:
            await ctx_devnet.send("```yaml\nAll nodes are healthy\n```")
    
      
    old_all_nodes_status_devnet = all_nodes_status_devnet
    
    print(flag_devnet)
    print(list_healthy_devnet)
    print(list_unhealthy_devnet)
    print(list(old_list_healthy_devnet))
    print(list(old_list_unhealthy_devnet))
    flag_devnet = 0

bot.run(TOKEN)