import discord
import time
import random
import os
from bs4 import BeautifulSoup
import requests
import re
import configparser

# Config environment
config = configparser.ConfigParser()
config.read('conf.ini')

# Variables Tateti
tablero = [["0", "1", "2"], ["3", "4", "5"], ["6", "7", "8"]]
jug = ["", ""]
tateti_iniciar = False
turno_jug = 0

# Discord Client
client = discord.Client()

# -----------Eventos-----------
@client.event
async def on_message(message):
    # Variables globales
    global tablero
    global tateti_iniciar
    global jug
    global turno_jug

    # Respuestas aleatorias
    respuesta = ["Si",
                 "No",
                 "Tal vez",
                 "Nunca",
                 "Seguramente",
                 "Nah",
                 "100% Seguro"]

    # Frases aleatorias
    frases = ["Sos pelotudo",
              "Hola",
              "Aguante River"]

    # El que escriba el comando no sea el mismo bot
    if(message.author == client.user):
        return
        #pass

    # Comando !hola
    if message.content == '!hola':
        msg = 'Buenos dias, {0.author.mention}'.format(message)
        await message.channel.send(msg)

    # Comando !hora
    if message.content == '!hora':
        msg = 'La hora es '+time.strftime("%H:%M:%S").format(message)
        await message.channel.send(msg)

    # Comando !fecha
    if message.content == '!fecha':
        msg = 'La fecha es '+time.strftime("%d/%m/%y").format(message)
        await message.channel.send(msg)

    # Comando !roll
    if message.content == '!roll':
        num = str(random.randrange(100))
        msg = (
            "El usuario {0.author.mention} saco el numero: " + num).format(message)
        await message.channel.send(msg)

    # Comando !purgar_chat
    if message.content == '!purgar_chat':
        msg = "Purgando todo el chat en 5 segundos \n"
        await message.channel.send(msg)
        time.sleep(5)
        await message.channel.purge()

    # Comando !borrame_esto
    if message.content == "!borrame_esto":
        msg = "Borrando esta mierda \n "
        await message.channel.delete()

    # Comando !help
    if message.content == '!help' or message.content == "!":
        msg = "Commandos de Neo Bot: \n"
        msg += "!hola --> Saludo \n"
        msg += "!hora --> Hora del sistema \n"
        msg += "!fecha --> Fecha del sistema \n"
        msg += "!roll --> Tira los dados \n"
        msg += "!help --> Ayuda del Bot \n"
        msg += "!pregunta --> Preguntale algo al Bot \n"
        msg += "!random --> El bot tira una frase random \n"
        msg += "!ping --> Podes consultar el lag que tenes \n"
        msg += "!purgar_chat --> (solo dev) Borra los ultimos mensajes del canal de chat donde se lanzo el comando\n"
        msg += "!borrame_esto --> (solo dev) Borra el ultimo mensaje del canal donde se lanzo el comando\n"
        msg += "!imagen <palabra> --> Busca una imagen dado una palabra o frase en google, la imagen no tiene un tamaño considerable\n"
        msg += "!iniciar_tateti <jugador a retar> --> Inicia una partida de tateti\n"
        msg += "!tateti <posicion> --> Juega la posicion indicada en el tateti\n"
        msg += "!hablar <frase> --> (solo dev) El bot dice algo\n"
        await message.channel.send(msg)

    # Comando !ping
    if message.content == "!ping":
        msg = round(client.latency * 1000)
        await message.channel.send("Ping : " + str(msg))

    # Comando "!usuarios"
    if message.content == "!usuarios":
        for u in message.guild.members:
            print(u.status)

    # Comando !random
    if message.content == "!random":
        await message.channel.send(random.choice(frases))

    # Comando !pregunta
    if message.content.startswith("!pregunta"):
        preg = re.compile(r"(!pregunta)").sub("", message.content,)
        await message.channel.send(preg+"? " + random.choice(respuesta))
    
    # Happy birthday
    if 'happy birthday' in message.content.lower() or 'feliz cumpleaños' in message.content.lower():
        await message.channel.send('Feliz cumpleaños!! 🎈🎉')

    # Busqueda de imagenes !imagen
    if message.content.startswith("!imagen"):
        image_list = []
        palabra_imagen = re.compile(r"(!imagen)").sub("", message.content,)
        url_google = "https://www.google.com/search?q=" + \
            palabra_imagen + "&source=lnms&tbm=isch"
        print("Link de la busqueda:" + url_google)
        res = requests.get(url_google).content
        soup = BeautifulSoup(res, 'html.parser')
        for link in soup.find_all("img"):
            image_list.append(link.get("src"))
        image_list = list(filter(None, image_list))
        image_list = list(filter(lambda a: "http" in a, image_list))
        e = discord.Embed()
        e.set_image(
            url=image_list[random.randrange(1 + (len(image_list) - 1))])
        await message.channel.send(embed=e)

    # El chat bot habla
    if message.content.startswith("!habla"):
        mensaje_habla = re.sub(r"!habla","", message.content)
        mensaje_habla = re.sub(r"r ","",mensaje_habla)
        await message.channel.send(mensaje_habla)

    # Tateti !tateti
    if message.content.startswith("!iniciar_tateti"):
        if tateti_iniciar:
            msg = "Ya hay una partida iniciada"
        else:
            rival = ""
            if len([x.id for x in message.mentions]) == 1:
                for u in [x.id for x in message.mentions]:
                    rival = u
                    jug[0] = message.author.id
                    jug[1] = rival
            if len([x.id for x in message.mentions]) > 1:
                msg = "Solo se puede retar a un usuario"
            elif len([x.id for x in message.mentions]) == 0:
                msg = "No se nombro a ningun usuario para la partida"
            elif rival not in [x.id for x in message.mentions]:
                msg = "El rival no se encuentra en la lista de usuarios"
            elif rival == message.author.id:
                msg = "El rival no puede ser el mismo usuario"
            else:
                tateti_iniciar = True
                msg = "Se inicia una partida de tateti entre <@" + str(message.author.id) + "> y <@" + str(rival) + ">\n"
                username1 = client.get_user(jug[0])
                username2 = client.get_user(jug[1])
                turno_jug = random.randrange(0,2)
                msg += "Turno de <@" + str(jug[turno_jug]) + "> "
        await message.channel.send(msg)
        
    if message.content.startswith("!tateti") and tateti_iniciar:
        if jug[turno_jug] == message.author.id:
            pos = re.compile(r"(!tateti)").sub("", message.content,)
            if tablero[(int(pos) // 3)][(int(pos) % 3)] == "X" or tablero[(int(pos) // 3)][(int(pos) % 3)] == "O":
                msg = "La posicion ya esta ocupada por " + tablero[(int(pos) // 3)][(int(pos) % 3)]
            else:
                if turno_jug == 0:
                    tablero[(int(pos) // 3)][(int(pos) % 3)] = "X"
                    turno_jug = 1
                else:
                    tablero[(int(pos) // 3)][(int(pos) % 3)] = "O"
                    turno_jug = 0
                msg = tablero[0][0] + " | " + tablero[0][1] + " | " + tablero[0][2] + "\n" \
                    + "----------\n" \
                    + tablero[1][0] + " | " + tablero[1][1] + " | " + tablero[1][2] + "\n" \
                    + "----------\n" \
                    + tablero[2][0] + " | " + tablero[2][1] + " | " + tablero[2][2]
                if tablero[0][0] == tablero[0][1] and tablero[0][0] == tablero[0][2] or \
                        tablero[1][0] == tablero[1][1] and tablero[1][0] == tablero[1][2] or \
                        tablero[2][0] == tablero[2][1] and tablero[2][0] == tablero[2][2] or \
                        tablero[0][0] == tablero[1][0] and tablero[0][0] == tablero[2][0] or \
                        tablero[0][1] == tablero[1][1] and tablero[0][1] == tablero[1][2] or \
                        tablero[0][2] == tablero[1][2] and tablero[0][2] == tablero[2][2] or \
                        tablero[0][0] == tablero[1][1] and tablero[0][0] == tablero[2][2] or \
                        tablero[2][0] == tablero[1][1] and tablero[2][0] == tablero[0][2]:
                    msg += "\n El ganador fue <@" + str(message.author.id) + "> , se limpiara el tablero"
                    # Limpio el tablero a como estaba antes
                    tablero = [["0", "1", "2"], ["3", "4", "5"], ["6", "7", "8"]]
                    tateti_iniciar = False
                else:
                    cant = 0
                    for i in range(0,3):
                        for j in range(0,3):
                            if tablero[i][j] == "X" or tablero[i][j] == "O":
                                cant += 1
                    if cant == 9:
                        msg += "\n El juego termino en empate"
                        # Limpio el tablero a como estaba antes
                        tablero = [["0", "1", "2"], ["3", "4", "5"], ["6", "7", "8"]]
                        tateti_iniciar = False
                    else:
                        msg += "\n Sigue el jugador <@" + str(jug[turno_jug]) + ">"
        else:
            msg = "No es el turno del jugador <@" + str(message.author.id) + ">"
        await message.channel.send(msg)
    elif message.content.startswith("!tateti") and not tateti_iniciar:
        msg = "Aun no se ha iniciado una partida de tateti, iniciala con !iniciar_tateti"
        await message.channel.send(msg)


@client.event
async def on_message_delete(message):
    await message.channel.send("Un mensaje ha sido borrado")


@client.event
async def on_ready():
    print("Neo-Bot preparado")
    print("Iniciado como {0.user}".format(client))


@client.event
async def on_member_join(member):
    # Envio de mensaje privado
    await member.create_dm()
    await member.dm_channel.send(f'Hola {member.name}, bienvenido a mi servidor de Discord!')
# -----------Eventos-----------

# Main

client.run(config['TOKEN']['secret_token'])
