# neo_bot

Hecho por Santiago Menendez

# Descripcion
Primer bot que programe para Discord.

# Funcionamiento
El bot posee los siguientes comandos:
- !hola --> Saludo
- !hora --> Hora del sistema
- !fecha --> Fecha del sistema
- !roll --> Tira los dados
- !help --> Ayuda del Bot
- !pregunta --> Preguntale algo al Bot
- !random --> El bot tira una frase random
- !ping --> Podes consultar el lag que tenes
- !purgar_chat --> (solo dev) Borra los ultimos mensajes del canal de chat donde se lanzo el comando
- !borrame_esto --> (solo dev) Borra el ultimo mensaje del canal donde se lanzo el comando
- !imagen <palabra> --> Busca una imagen dado una palabra o frase en google, la imagen no tiene un tamaño considerable ya que scrappea en el HTML de la busqueda.
- !iniciar_tateti <jugador a retar> --> Inicia una partida de tateti
- !tateti <posicion> --> Juega la posicion indicada en el tateti
- !hablar <frase> --> (solo dev) El bot dice algo

# Modulos
Lista de modulos necesarios en Python para ejecutar el bot:
- discord
- time
- random
- os
- bs4
- requests
- re
- configparser

Todos los modulos se pueden instalar con pip.

# Configuracion
Para configurar el bot y correrlo en el canal de discord deben configurar una app en la pagina https://discord.com/developers/applications.
Luego deben incluirlo en su canal de discord.
Despues deben modificar en el archivo conf.ini y agregar el token secreto que les provee la pagina.
Y por ultimo ejecutan neo_bot.py y les funcionara el bot dentro de la pagina.
