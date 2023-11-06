from telethon import TelegramClient, events
from cs50 import SQL

db = SQL("sqlite:///aluno-antenado.db")

api_id = 12345678
api_hash = '123456789a0a0a12345a0a0a0a0a123a'
bot_token = "1234567890:ABCDEf_ab0aBC0ABVdefgh0aBcd0a12a_bcd"

bot = TelegramClient('bot_start', api_id, api_hash).start(bot_token=bot_token)


async def main():
    @bot.on(events.NewMessage(pattern='/start'))
    async def start(event):
        sender = await event.get_sender()
        ids = []

        rows = db.execute("SELECT id FROM users;")
        for row in rows:
            ids.append(row['id'])

        if sender.id not in ids:
            db.execute("INSERT INTO users (first_name, id) VALUES (?, ?)", sender.first_name, sender.id)
            await bot.send_message(sender.id, f"**Parabéns**, {sender.first_name}!\n\n"
                                   "Você foi adicionado na newsletter de notícias oficiais do MEC.\n\n"
                                   "Se quiser parar de receber as notícias utilize o /cancelar .")

        else:
            await bot.send_message(sender.id, "**Você já foi adicionado na newsletter de notícias oficiais do MEC** \n\n"
                                   "Se quiser parar de receber as notícias utilize o /cancelar .")

    @bot.on(events.NewMessage(pattern='/cancelar'))
    async def cancel(event):
        sender = await event.get_sender()
        ids = []

        rows = db.execute("SELECT id FROM users;")
        for row in rows:
            ids.append(row['id'])

        if sender.id in ids:
            db.execute("DELETE FROM users WHERE first_name = ? AND id = ?;", sender.first_name, sender.id)
            await bot.send_message(sender.id, f"**Que pena =(**, {sender.first_name}\n\n"
                                              "Você foi removido na newsletter de notícias oficiais do MEC.\n\n"
                                              "Se quiser começar a receber as notícias novamente utilize o /start .")

        else:
            await bot.send_message(sender.id,
                                   "**Você nao esta adicionado na newsletter de notícias oficiais do MEC** \n\n"
                                   "Se quiser começar a receber as notícias utilize o /start .")


with bot:
    bot.loop.run_until_complete(main())
    bot.run_until_disconnected()
