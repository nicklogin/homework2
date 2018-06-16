import StarTrekBot

bot = StarTrekBot.MarkoffTrigramBot('trigram_frequencies.csv',12)
print('bot ready!')
s = input()
while s!='stop!':
    print(bot.reply(s))
    s = input()