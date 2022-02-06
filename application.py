from bs4 import BeautifulSoup
import requests
import discord
import asyncio

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class chair:
    def __init__(self, name, total_price, used, link):
        self.name = name
        self.total_price = total_price
        self.used = used
        self.link = link

    def __str__(self):
        return f"Name     : {self.name}\nPrice    : ${self.total_price:.2f}\nUsed?    : {self.used}\nLink     : {self.link}"

def find():
    page = 1
    url = " "
    url_next = ""
    chair_set = set()
    avg_price = 0.0
    alert_threshold = 0.6  # alerts at 40% under average

    while url != url_next:

        url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=herman+miller+aeron+size+b&_sacat=0&LH_TitleDesc=0&_pgn={page}"
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, "lxml")
        next = soup.find("a", class_= "pagination__next")
        url_next = next['href']

        print(f"Reading page {page}...")

        listings = soup.find_all("li", class_="s-item")
        listings.pop(0)                                     # first element is irrelevant code

        for i in listings:
            name = i.h3.text
            price = i.find("span", class_="s-item__price").text
            used = i.find("span", class_="SECONDARY_INFO").text

            link = i.a["href"]

            price = price.replace("$", "")
            price = price.replace(",", "")

            if "seat" in name.lower():                      # filters out irrelevant listings
                continue

            if "backrest" in name.lower():
                continue

            if "back" in name.lower():
                continue

            if "to" in price:                               # finds avg. price if listing price has range (i.e. "$1,150.00 to $1,400.00")
                price_range = price.split()
                min = float( price_range[0] )
                max = float( price_range[2] )
                price = (min + max) / 2

            price = float(price)

            if price < 200:
                continue
            if "Brand New" in name:
                continue

            chair_obj = chair(name, price, used, link)
            chair_set.add(chair_obj)

        page += 1
    page -= 1
    print(f"Scanned through {page} pages.\n")

    for i in chair_set:
        avg_price += i.total_price

    avg_price = avg_price / len(chair_set)
    print(f"Average price = ${avg_price:.2f}")

    TOKEN = "OTMwNDQ4MDk5NDcyNzE5ODcy.Yd2BUQ.vFTln76hte2QTqgacg3A2ZBFNec"
    client = discord.Client()

    @client.event
    async def on_ready():
        channels = [c for g in client.guilds for c in g.text_channels]      # getting all the text channels bot can see
        channel = discord.utils.get(channels, name="testchannel")

        print(f"We have logged in as {client.user}")
        await channel.send("Beep bop, hello world")

        for i in chair_set:
            if i.total_price < avg_price * alert_threshold:
                await channel.send(f"{i}\n---------------\n")           # sends the chair message
        await channel.send("Listings finished.")
        await client.close()


    client.run(TOKEN)


if __name__ == '__main__':
    find()
