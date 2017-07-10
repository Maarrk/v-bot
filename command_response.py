import discord

client = discord.Client()


def get_main_channel(server):
    text_channels = [chan for chan in server.channels if chan.type == discord.ChannelType.text]

    for chan in text_channels:
        if chan.name == 'general' or chan.name == 'glowny':
            return chan

    return None


def get_pstr(server):
    pointemoji = None
    emojiname = None

    if server.name.lower() == 'rasputin':
        emojiname = 'putin'
    elif server.name.lower() == 'v-santos.pl':
        emojiname = 'vsantos'

    if emojiname:
        for emoji in server.emojis:
            if emoji.name == emojiname:
                pointemoji = emoji
                break

    if pointemoji:
        return '\n' + str(pointemoji) + ' '
    else:
        return '\n- '


def is_worthy(command_author):

    # Maarrk
    if command_author.id == '176918774618914826':
        return True
    # Toyer
    if command_author.id == '256169168884203520':
        return True

    roles = command_author.roles
    if len(roles) > 0:
        for role in roles:
            if role.name.lower() == "testrole":
                return True
            if role.name.lower() == "zarząd":
                return True
            if role.name.lower() == "community manager":
                return True
            if role.name.lower() == "administrator":
                return True
            if role.name.lower() == "developer":
                return True

    return False


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # message is meant for this bot
    if message.content.lower().startswith(('vbot', 'v-bot')):

        # we only process messages from certain users
        if not is_worthy(message.author):
            await client.send_message(message.author, 'Nie masz uprawnien do obsługi V-Bota')
            return

        words = message.content.split()
        if len(words) > 1:
            if words[1].lower() == 'sens':

                pstr = get_pstr(message.server)

                msgs = ['**Zamierzamy zgodnie z planem uruchomić zarówno serwer voice i tekstowy ponieważ:**',
                        'Decyzja o kształcie serwera nie była podjęta w 15 minut, owszem przemyśleliśmy to',
                        'Wiemy co powoduje podział graczy na dwa serwery',
                        '''Jesteśmy dopiero w fazie Alfa. Dla nieoczytanych wklejam z Wikipedii:
*Alpha software can be unstable and could cause crashes or data loss. Alpha software may not contain all of the features that are planned for the final version.*''',
                        'Serwer nie jest w ostatecznym kształcie, wybraliśmy opcję która pozwoli nam zebrać najwięcej wiedzy',
                        'Mamy chętnych do gry na obu wersjach: *Vox populi, vox Dei*']

                msg = pstr.join(msgs)
                await client.send_message(message.channel, msg)
                return

            if words[1].lower() == 'faq':
                msg = '**Najczęściej zadawane pytania:** https://www.facebook.com/vsantosrp/posts/1121559141309289'
                await client.send_message(message.channel, msg)
                return

            if words[1].lower() == 'data':
                msg = 'Nazwa kanału: %s' % message.channel.name
                await client.send_message(message.channel, msg)
                return

            else:
                msg = message.author.mention + ' nie zrozumiałem polecenia\n' \
                                               'Ale nie lękaj się, V-Bot czuwa'
                await client.send_message(message.channel, msg)

        else:
            msg = message.author.mention + ' nie lękaj się, V-Bot czuwa'
            await client.send_message(message.channel, msg)


@client.event
async def on_member_join(member):
    pass


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run('MzMzNjg5NTU4MTgzMDUxMjY0.DEQUPQ.mKyrenL5PF5mBsQOAs3Op3PekYg')
