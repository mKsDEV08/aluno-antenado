from datetime import datetime
from time import sleep

import requests

from bs4 import BeautifulSoup

from telethon import TelegramClient

from consume_ids import consume_ids

month = datetime.now().month
year = datetime.now().year

months = ['Janeiro', 'Fevereiro', 'Marco', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro',
          'Novembro', 'Dezembro']

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/86.0.4240.198 Safari/537.36"
}

api_id = 12345678
api_hash = '123456789a0a0a12345a0a0a0a0a123a'
bot_token = "1234567890:ABCDEf_ab0aBC0ABVdefgh0aBcd0a12a_bcd"

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

def main():
    while True:
        last = get_last()

        file = open("last_new.txt", 'r+')

        old = file.read()

        if last is not None:
            title_utf8 = str(last[2])
            title_utf8 = title_utf8.split('/')
            title_utf8 = title_utf8[len(title_utf8) - 1]
            
            if title_utf8 != old:
                with client:
                    client.loop.run_until_complete(send_messages(last[0], last[1], last[2], last[3]))

                file.seek(0)
                file.truncate(0)
                file.write(title_utf8)

                print("New, sending messages...")

            else:
                print("No news")

        else:
            print("No news last is none")

        file.close()

        sleep(600)


def get_last():
    for i in range(0, 20):
        try:
            url = f'https://www.gov.br/mec/pt-br/assuntos/noticias/{year}/{months[month - 1]}?b_start:int={i * 20}'
            site = requests.get(url, headers=headers)
            soup = BeautifulSoup(site.content, 'html.parser')

            title = soup.find_all("a", class_="state-published url")
            title = title[len(title) - 1].text

            description = soup.find_all("p", class_="description discreet")
            description = description[len(description) - 1].text

            link = soup.find_all("a", class_="state-published url", href=True)
            link = link[len(link) - 1]['href']

            date = soup.find_all("span", class_="documentByLine")
            date = date[len(date) - 1].text.split("\n")[9].split("                            ")[1]

            last = [title, description, link, date]

        except:
            try:
                return last
            except:
                return


async def send_messages(title, desc, link, date):
    ids = consume_ids()

    for i in ids:
        try:
            await client.send_message(int(i), f"**{title}** \n\n{desc} \n\n{link} \n\nData de postagem: {date}")

        except:
            print('Não foi possível enviar a mensagem')


main()
