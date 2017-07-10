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
            if role.name.lower() == 'testrole':
                return True
            if role.name.lower() == 'zarząd':
                return True
            if role.name.lower() == 'community manager':
                return True
            if role.name.lower() == 'administrator':
                return True
            if role.name.lower() == 'developer':
                return True
            if role.name.lower() == 'support':
                return True
            if role.name.lower() == 'moderator':
                return True

    return False


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # message is meant for this bot
    if message.content.lower().startswith(('vbot', 'v-bot')):

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
                # only authorised users can use this command
                if not is_worthy(message.author):
                    await client.send_message(message.author, 'Nie masz uprawnien do tej komendy')
                    await client.delete_message(message)
                    return

                msg = 'Nazwa kanału: %s' % message.channel.name
                await client.send_message(message.channel, msg)
                return

            if words[1].lower() == 'join':
                # only authorised users can use this command
                if not is_worthy(message.author):
                    await client.send_message(message.author, 'Nie masz uprawnien do tej komendy')
                    await client.delete_message(message)
                    return

                if len(words) >= 2:
                    member_joined = message.server.get_member_named(words[2])
                    if member_joined:
                        await on_member_join(member_joined)
                    else:
                        await client.send_message(message.author, 'Nie znalazłem użytkownika "%s" '
                                                                  'wśród obecnie aktywnnych.'
                                                                  'Spróbuj wpisać jego @mention po "join"' % words[2])
                        await client.delete_message(message)
                else:
                    await client.send_message(message.author, 'Podaj nazwę użytkownika po "join"')
                    await client.delete_message(message)
                return

            if words[1].lower() == 'maul':
                # only authorised users can use this command
                if not is_worthy(message.author):
                    await client.send_message(message.author, 'Nie masz uprawnien do tej komendy')
                    await client.delete_message(message)
                    return

                maul = 'Maul'
                maul_member = message.server.get_member_named('Maul#4420')
                if maul_member:
                    maul = maul_member.mention

                msg = 'Użytkownik %s 10 lipca 2017 o 20:30 napisał:\n' \
                      '***Wywalcie tego vbota to jest zmarnowanie produktywności ludzkiej ' \
                      'na coś co i tak nie ma praktycznego zastosowania***' % maul

                await client.send_message(message.channel, msg)
                return

            # msg = message.author.mention + ' nie zrozumiałem polecenia\n' \
            #     'Ale nie lękaj się, V-Bot czuwa'
            # await client.send_message(message.channel, msg)
            await client.send_message(message.author, 'Nie zrozumiałem polecenia "%s"' % message.content)
            await client.delete_message(message)
            return

        elif len(words) == 1:
            msg = message.author.mention + ' nie lękaj się, V-Bot czuwa'
            await client.send_message(message.channel, msg)


@client.event
async def on_member_join(member):
    chan = get_main_channel(member.server)
    tada = '\U0001F389'
    msg = '%s **Witamy nowego użytkownika %s!** %s \n Ekipa V-Santos życzy Ci miłej gry na naszym serwerze' \
        % (tada, member.mention, tada)

    if chan:
        await client.send_message(chan, msg)
    return


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run('MzMzNjg5NTU4MTgzMDUxMjY0.DEQUPQ.mKyrenL5PF5mBsQOAs3Op3PekYg')
