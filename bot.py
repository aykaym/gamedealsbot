import discord
from discord.ext.commands import Bot
import requests
import datetime
import csv
import time

BOT_PREFIX = "/"
TOKEN = open("token_test.txt", 'r').read().replace("\n", '')
client = Bot(command_prefix = BOT_PREFIX)
client.remove_command('help')



@client.event
async def on_ready():
    print("Its working")


def get_games(id):
    if id == 100:
        url = "http://www.cheapshark.com/api/1.0/deals?pageSize=60"
    else:
        url = "http://www.cheapshark.com/api/1.0/deals?storeID="+id
    response = requests.get(url)
    data = response.json()
    return data


def get_stores():
    url = "http://cheapshark.com/api/1.0/stores"
    response = requests.get(url)
    platforms = response.json()
    return platforms

def parse_games(data):
    game_list = []
    stores = []
    ids = []
    platforms = get_stores()

    for key in platforms:
        stores.append(key['storeName'])
        ids.append(key['storeID'])

    for key in data:
        game = []
        title = key['title']
        sale_price = key['salePrice']
        normal_price = key['normalPrice']
        savings = key['savings']
        deal_rating = key['dealRating']
        picture = key['thumb']
        storeID = key['storeID']
        dealID = key['dealID']
        steamRatingText = key['steamRatingText']
        steamRatingPercent = key['steamRatingPercent']
        steamRatingCount = key['steamRatingCount']
        thumb = key['thumb']
        i = ids.index(storeID)
        store = stores[i]
        csv_deal_link = "=HYPERLINK(\"https://www.cheapshark.com/redirect.php?dealID="+dealID+"\",\""+title+"\")" #dont ever fuck with this, escape character madness
        deal_link = "https://www.cheapshark.com/redirect.php?dealID=" + dealID
        game.extend((title, steamRatingText, steamRatingPercent, steamRatingCount, csv_deal_link, store, normal_price, sale_price, savings, deal_rating, thumb, deal_link))
        game_list.append(game)
    return game_list


def csv_create(game_list):
    filename = (datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+ ".csv")
    with open(filename, 'w') as game_file:
        game_writer = csv.writer(game_file, delimiter = ',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
        game_writer.writerow(["Title", "Store", "MSRP", "Sale Price", "Discount", "Deal Rating", "Steam Rating", "No. of Steam Reviews"])
        for game in game_list:
            game_writer.writerow([game[4], game[5], game[6], game[7], game[8], game[9], game[1], game[3]])
    game_file.close()
    return filename



#Commands

@client.command(pass_context=True, aliases = ['Deals_CSV', 'deals_Csv', 'Deals_csv', 'deals_CSV', 'DEALS_CSV'])
async def deals_csv(ctx):
    author = ctx.message.author
    channel = ctx.message.channel
    id = 100
    data = get_games(id)
    game_list = parse_games(data)
    filename = csv_create(game_list)
    await channel.send("Your csv file is being sent to your DMs")
    print("/deals_csv: " + filename)
    await author.send(file=discord.File(filename))

@client.command(pass_context=True, aliases = ['Deals_Spam', 'Deals_spam', 'deals_Spam', 'DEALS_SPAM'])
async def deals_spam(ctx):
    id = 100
    author = ctx.message.author
    channel = ctx.message.channel
    data = get_games(id)
    game_list = parse_games(data)
    print("/deals_spam")
    await channel.send("Your game deals are being sent to your DMs right now")
    for game in game_list:
                await author.send("-" * 120 + "\nDeal Link: "+ game[11] +"\nTitle: " + game[0] + "\nStore: " + game[5] + "\nMSRP: " + game[6] + "\nSale Price: " + game[7] + "\nDiscount: " + game[8] + "\nDeal Rating: " + game[9])
                time.sleep(1)

@client.command(pass_context=True, aliases = ['Deals_Custom', 'Deals_custom', 'deals_Custom', 'DEALS_CUSTOM'])
async def deals_custom(ctx, arg):
    author = ctx.message.author
    channel = ctx.message.channel
    arg = arg.lower()
    stores = []
    ids = []
    platforms = get_stores()
    for key in platforms:
        stores.append(key['storeName'].lower())
        ids.append(key['storeID'])
    if arg in stores:
        i = stores.index(arg)
        id = ids[i]
    data = get_games(id)
    game_list = parse_games(data)
    filename = csv_create(game_list)
    await channel.send("Your custom csv file for " + arg + " is being sent to your DMs")
    print(filename)
    await author.send(file=discord.File(filename))


@client.command(pass_context=True, aliases = ['ShowStores', 'Showstores', 'showstores', 'SHOWSTORES'])
async def showStores(ctx):
    author = ctx.message.author
    stores = []
    platforms = get_stores()
    for key in platforms:
        stores.append(key['storeName'])
    await author.send("These are all the stores that our bot can check for:\n" + stores[0] + "\n" + stores[1] + "\n"+ stores[2] + "\n" + stores[3] + "\n" + stores[4] + "\n" + stores[5] + "\n" + stores[6] + "\n" + stores[7] + "\n" + stores[8] + "\n" + stores[9] + "\n" + stores[10] + "\n" + stores[11] + "\n" + stores[12] + "\n" + stores[13] + "\n" + stores[14] + "\n" + stores[15] + "\n" + stores[16] + "\n" + stores[17] + "\n" + stores[18] + "\n" + stores[19] + "\n" + stores[20] + "\n" + stores[21] + "\n" + stores[22] + "\n" + stores[23] + "\n" + stores[24]) 


@client.command(pass_context=True, aliases = ['Help', 'HELP'])
async def help(ctx):
    help = "You have asked for help!\nThis discord bot is capable of requesting the best game deals from a Public API across multiple platforms.\nCommands:\n`/deals_csv` - Sends detailed game deals information to DMs in csv format\n`/deals_spam` - Sends game deals to your DMs and includes a picture.\n`/deals_custom \"<store>\"` - Searches for specific store\n`/showStores` - Shows stores that can be used in custom search"
    author = ctx.message.author
    channel = ctx.message.channel
    await channel.send(help) 


client.run(TOKEN, reconnect=True)
