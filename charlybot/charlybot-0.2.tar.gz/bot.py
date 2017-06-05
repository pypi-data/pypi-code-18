from __future__ import unicode_literals
import discord
import aiohttp
from discord.ext.commands import Bot
import secrets
import dropbox
from dropbox.exceptions import ApiError,AuthError
from dropbox.files import WriteMode
import datetime
import youtube_dl
import re
import sys
import properties
import tweepy
import os
from time import sleep

#Description du Bot
description = 'charly-bot est un bot multitâche'
#Définition du préfixe de chaque commande
client_bot = Bot(description=description,command_prefix="!")
#Token pour accéder à dropbox
dbx = dropbox.Dropbox(secrets.DROPBOX_TOKEN)
#Racine dropbox
root = '/'

#Twitter
auth = tweepy.OAuthHandler(secrets.CONSUMMER_KEY, secrets.CONSUMMER_SECRET)
auth.set_access_token(secrets.ACCESS_TOKEN, secrets.ACCESS_TOKEN_SECRET)
auth.secure = True
api = tweepy.API(auth)
#Fin twitter

#Youtube Dl
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

#Option youtube-dl
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'progress_hooks': [my_hook],
}

#Liste de mots générant une réaction 
#list_text_reaction = ['Oui','Non']

#####Connexion#####

@client_bot.event
async def on_ready():
	print('Connexion ok!!')
	print('Nom bot: {}'.format(client_bot.user.name))
	print('ID du bot: {}'.format(client_bot.user.id))
	print('Version : {}'.format(discord.__version__))

#####Fin Connexion#####

#####Commandes#####

@client_bot.command()
async def commands():
    """Tous les services proposés par le bot"""
    embed=discord.Embed(title="Les services de charly-bot", 
        description="**YOUTUBE**  :musical_note: \n"
                    "`mp3`     `infos`\n\n"
                    "**DROPBOX** :open_file_folder:\n"
                    "`mydb`    `create`     `delete`     `box`     `upload`     `versions`     `restore`     `shared`     `share`      `link`      `copy`      `move`\n\n"
                    "**WEATHER** :white_sun_small_cloud:\n"
                    "`weathers`\n\n"
                    "**TWITTER**  :speech_balloon: \n\n"
                    "`twitter`    `follow`     `tweeter`     `unfollow`     `bot_tweet`\n\n"
                    "**Autres** :point_right: \n"
                    "`lyric`    `status`     `img`     `cleanner`", 
                    color=0xe0876a)
    embed.set_thumbnail(url='http://www.gifss.com/robot/robot-20.gif')
    embed.set_footer(text="Tapez .help <command> pour plus de détails sur l'utilisation de la commande")
    await client_bot.say(embed=embed)

#####Fin commandes#####

#####Twitter#####

@client_bot.command()
async def twitter(user_name):
    """Information du profile du user en paramètre"""
    user = api.get_user(screen_name = user_name)
    emb=discord.Embed(title="Aller sur le twitter de {}".format(user.screen_name), url=properties.TWITTER_URL + user_name, color=0x3498db)
    emb.set_author(name="Envoyé par charly-bot", icon_url= client_bot.user.avatar_url)
    emb.set_thumbnail(url = properties.URL_INFO)
    emb.set_image(url = user.profile_image_url)
    emb.add_field(name="ID :key:", value=user.id, inline=True)
    emb.add_field(name="Nom", value=user.name, inline=True)
    emb.add_field(name="Screen name", value="@"+user.screen_name, inline=True)
    emb.add_field(name="Création :date:", value=user.created_at, inline=True)
    #emb.add_field(name="Localisation", value=user.location, inline=True)
    emb.add_field(name="Nombre de liste", value=user.listed_count, inline=True)
    emb.add_field(name="Favoris :star: ", value=user.favourites_count, inline=True)
    emb.add_field(name="Followers :heart_eyes: ", value=user.followers_count, inline=True)
    emb.add_field(name="Nombre d'amis :busts_in_silhouette:", value=user.friends_count, inline=True)
    emb.add_field(name="Nombre de tweets", value=user.statuses_count, inline=True)
    embed.set_image(url= properties.TWITTER_IMG)
    await client_bot.say(embed=emb)

@client_bot.command()
async def follow():
    """Follow les users
       Récupère les ids des users à suivre dans le fichier 
    """
    with open('follow.txt') as f:
        for line in f:
            user_id = line.strip()
            api.create_friendship(user_id)
        embed=discord.Embed(title="Vous suivez dès à présent les twittos spécifiés", color=0x3498db)
        embed.set_thumbnail(url=properties.FOLW)
        embed.set_image(url= properties.TWITTER_IMG)
        return await client_bot.say(embed=embed)

@client_bot.command()
async def tweeter(message):
    """Envoyer un tweet"""
    if len(message) <= 140:
        api.update_status(status=message)
        emb=discord.Embed(title="**Envoyé**", color=0x3498db)
        emb.set_thumbnail(url=properties.TWEET_SEND)
        emb.add_field(name="**@Cpdyn**", value=message, inline=False)
        emb.set_footer(text="Votre tweet fait: {} caractère(s)".format(len(message)))
        embed.set_image(url= properties.TWITTER_IMG)
        await client_bot.say(embed=emb)
    else:
        emb=discord.Embed(title="Tweet refusé", description="Vous avez saisi plus de 140 caractères!!!!", color=0xe74c3c)
        emb.set_thumbnail(url=properties.TWEET_LONG)
        emb.set_footer(text="Votre tweet fait: **{}** caractère(s)".format(len(message)))
        embed.set_image(url= properties.TWITTER_IMG)
        await client_bot.say(embed=emb)

@client_bot.command()
async def unfollow():
    """Unfollow les users
       Récupère les ids des users à unfollow dans le fichier 
    """
    with open('unfollow.txt') as f:
        for line in f:
            user_id = line.strip()
            api.destroy_friendship(user_id)
        embed=discord.Embed(title="Vous ne suivez plus ces twittos", color=0x3498db)
        embed.set_thumbnail(url=properties.FOLW)
        embed.set_image(url= properties.TWITTER_IMG)
        return await client_bot.say(embed=embed)
"""
@client_bot.command()
async def bot_tweet():
    Function permettant au bot d'envoyer les messages contenu dans le fichier
    my_file=open('tweet_for_bot.txt','r')
    file_lines=my_file.readlines()
    my_file.close()
    for line in file_lines:
        try:
            print(line)
            if  line != '\n':
                api.update_status(line)
                sleep(900)
            else:
                pass
        except tweepy.TweepError as e:
            print(e.raison)
            sleep(2)
    return await client_bot.say("test")
"""

#####Fin twitter#####

#Quelques fonctionnalités

@client_bot.command()
async def status(*arg):
    """Changer le status"""
    x = " ".join(str(e) for e in arg)
    await client_bot.change_presence(game = discord.Game(name=x))  

@client_bot.command()
async def img(channelID, path, message):
    """Envoyer un fichier à un channel"""
    with open(path,'rb') as image:
        return await client_bot.send_file(client_bot.get_channel(channelID), image, content=str(message))
    return client_bot.say('Image envoyé')
#Fin

#####Youtube#####

@client_bot.command()
async def mp3(url):
    """Télécharge une vidéo youtube, vimeo à l'adresse <url> et convertir en mp3"""
    with youtube_dl.YoutubeDL(ydl_opts) as you_dl_convert:
        result = you_dl_convert.download([url])
        embed=discord.Embed(title="Les doigts dans le nez", color=0x2ecc71)
        embed.set_author(name="Charly-Bot")
        embed.set_thumbnail(url= properties.OK_MP3)
        embed.set_image(url = properties.MP3_ICON)
        return await client_bot.say(embed=embed)

@client_bot.command()
async def infos(url):
    """Affiche les informations d'une vidéo youtube, vimeo...donc l'adresse est <url>
       ATTENTION: les chants étant différents selon les cas, seul les infos youtubes sont traitées
    """
    await client_bot.say(embed=emb)
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as you_dl_info:
        infos = you_dl_info.extract_info(url, download=False)
        emb=discord.Embed(title=infos['title'], url=url, color=0x9b59b6)
        emb.set_author(name="Envoyé par charly-bot", icon_url= client_bot.user.avatar_url)
        emb.set_thumbnail(url = properties.URL_INFO)
        emb.set_image(url = properties.YOUTUBE_ICON)
        emb.add_field(name="ID Vidéo", value=infos['id'], inline=True)
        emb.add_field(name="Publiée par", value=infos['uploader'], inline=True)
        emb.add_field(name="Mise en ligne", value=infos['upload_date'], inline=True)
        emb.add_field(name="Durée", value=infos['duration'], inline=True)
        emb.add_field(name="Age limite", value=infos['age_limit'], inline=True)
        emb.add_field(name="Vu", value=infos['view_count'], inline=True)
        emb.add_field(name="Aime", value=infos['like_count'], inline=True)
        emb.add_field(name="Aime pas", value=infos['dislike_count'], inline=True)
        emb.add_field(name="Description de la vidéo", value=infos['description'], inline=True)
        await client_bot.say(embed=emb)

#####Fin Youtube#####
#####Dropbox#####

@client_bot.command()
async def mydb():
    """Informations du compte dropbox de l'utilisateur courant"""
    try:
        account = dbx.users_get_current_account()
    except AuthError as err:
        embed=discord.Embed(title="ATTENTION", description="**Token invalide. Régénérez un nouveau**", color=0xe74c3c)
        embed.set_thumbnail(url=properties.DANGER)
        return await client_bot.say(embed=embed)
    else:
        embed=discord.Embed(title="Compte dropbox", url=properties.DB_URL, color=0x2ecc71)
        embed.set_thumbnail(url=account.profile_photo_url)
        embed.add_field(name="Nom", value=account.name.surname, inline=True)
        embed.add_field(name="Prénom", value=account.name.given_name, inline=True)
        embed.add_field(name="Nom familier", value=account.name.familiar_name, inline=True)
        embed.add_field(name="Nom affiché", value=account.name.display_name, inline=True)
        embed.add_field(name="Abréviation ", value=account.name.abbreviated_name, inline=True)
        embed.add_field(name="Email", value=account.email, inline=True)
        if account.email_verified:
            embed.add_field(name="Email vérifié", value="Oui", inline=True)
        else:
            embed.add_field(name="Email vérifié", value="Non", inline=True)
        embed.add_field(name="Langue", value=account.locale, inline=True)
        embed.add_field(name="Pays", value="CH", inline=True)
        #embed.add_field(name="Type de compte", value="Basic", inline=True)
        embed.add_field(name="Lien de reférence", value=account.referral_link, inline=True)
        embed.set_footer(text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        embed.set_image(url= properties.DROP_IMG)
        await client_bot.say(embed=embed)

@client_bot.command()
async def create(path):
    """Créer un dossier dropbox en indiquant le chemin <path>. 
        Ex1: toto va créer le dossier toto
        Ex1: toto/tata/titi va créer tata et titi
    """
    try:
        data = dbx.files_create_folder(root + path, autorename=True)
    except ApiError as err:
        if(err.error.is_path() and err.error.get_path().is_malformed_path()):
            embed=discord.Embed(title=":warning: **ATTENTION** CHEMIN MAL FORME", 
                    description="Si vous voulez créer à la racine de dropbox:   **monDossier**\n"
                                "Si c'est un sous dossier:   **dossierExistant/monDossier**\n"
                                "Plusieurs dossiers à la fois:   **dossier1/dossier2/dossier3/...**",
                    color=0xe74c3c)
            embed.set_thumbnail(url=properties.DANGER)
            return await client_bot.say(embed=embed)
    else:
        embed=discord.Embed(title="**Dossier créé**", color=0x8e44ad)
        #embed.set_author(name="charly-bot")
        embed.set_thumbnail(url=properties.FOLDER_CREATE)
        embed.add_field(name="Dossier", value= data.name, inline=True)
        embed.add_field(name="Localisation", value= data.path_display, inline=True)
        embed.set_image(url= properties.DROP_IMG)
        #embed.add_field(name="Partagé", value="Non", inline=False)
        embed.set_footer(text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        await client_bot.say(embed=embed)

@client_bot.command()
async def delete(path):
    """Supprimer un fichier ou un dossier"""
    try:
        data = dbx.files_delete(root + path)
    except ApiError as err:
        print("Erreur: {} ".format(err))
        embed=discord.Embed(title="ERREUR", description="Vérifier que l'élément existe bien\nRenseigner le bon chemin (pas de **/** au début)", color=0x2ecc71)
        embed.set_thumbnail(url=properties.DANGER)
        embed.set_image(url= properties.DROP_IMG)
        return await client_bot.say(embed=embed)
    else:
        print(data)
        embed=discord.Embed(title="**Elément supprimé**", color=0xe74c3c)
        #embed.set_author(name="charly-bot")
        embed.set_thumbnail(url=properties.TRASH)
        embed.add_field(name="Dossier", value= data.name, inline=True)
        embed.add_field(name="Localisation", value= data.path_display, inline=True)
        embed.set_image(url= properties.DROP_IMG)
        #embed.add_field(name="Partagé", value="Non", inline=False)
        embed.set_footer(text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        await client_bot.say(embed=embed)

@client_bot.command()
async def box(path):
    """Eléments contenu dans le path spécifié"""
    try:
        data = dbx.files_list_folder(root + path)
    except ApiError as err:
        print("Erreur: {} ".format(err))
        embed=discord.Embed(title="ERREUR", description="Vérifier que l'élément existe bien\nRenseigner le bon chemin (pas de **/** au début)", color=0xe74c3c)
        embed.set_thumbnail(url=properties.DANGER)
        embed.set_image(url= properties.DROP_IMG)
        return await client_bot.say(embed=embed)
    else:
        for entry in data.entries:
            embed=discord.Embed(title="Dossier", color=0x3498db)
            embed.set_thumbnail(url=properties.DROP_THU)
            embed.add_field(name="Nom", value=entry.name, inline=True)
            embed.add_field(name="Localisation", value=entry.path_display, inline=True)
            embed.set_image(url= properties.DROP_IMG)
            await client_bot.say(embed=embed)

@client_bot.command()
async def upload(local_file, dropbox_dest):
    """Uploader un fichier sur dropbox. 
        Attention il faut mettre l'extension du fichier. 
        Taille de fichier de moins de 150MB
        
        Ex: upload fichier.txt fichier_uploader.txt
    """
    with open(local_file, 'rb') as f:
        try:
            data = dbx.files_upload(f.read(), root +dropbox_dest, mode=WriteMode('overwrite'))
            res = dbx.sharing_create_shared_link(root + dropbox_dest, short_url=True)
        except ApiError as err:
            print("Erreur: {} ".format(err))
            embed=discord.Embed(title="ERREUR", description="Vérifier que l'élément existe bien\nRenseigner le bon chemin (pas de **/** au début)", color=0xe74c3c)
            embed.set_thumbnail(url=properties.DANGER)
            embed.set_image(url= properties.DROP_IMG)
            return await client_bot.say(embed=embed)
        else:
            embed=discord.Embed(title="Sauvegarde", description="**Sauvegarde du fichier {} réussie**\n"
                                                                "**Lien de partage**: {}\n"
                                                                "**Lien de téléchargement**: {}\n"
                                                                .format(data.name, res.url, re.sub(r"\?dl\=0", "?dl=1", res.url))
                                                                , color=0x2ecc71)
            embed.set_thumbnail(url=properties.UP)
            embed.set_footer(text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
            embed.set_image(url= properties.DROP_IMG)
            return await client_bot.say(embed=embed)

@client_bot.command()
async def versions(dropbox_dest):
    """Retourne toutes les versions d'un fichier trié de la plus anciennes à la plus récente"""
    try:
        entries = dbx.files_list_revisions(root + dropbox_dest, limit=30).entries
        revisions = sorted(entries, key=lambda entry: entry.server_modified)
    except ApiError as err:
        print("Erreur: {} ".format(err))
        embed=discord.Embed(title="ERREUR", description="Vérifier que l'élément existe bien\nRenseigner le bon chemin (pas de **/** au début)\nVérifier les extensions", color=0xe74c3c)
        embed.set_thumbnail(url=properties.DANGER)
        embed.set_image(url= properties.DROP_IMG)
        return await client_bot.say(embed=embed)
    else:
        count = 0
        for revision in revisions:
            #print(revision)
            count +=1
            embed=discord.Embed(title="Version {}".format(count), description="**ID:** {} \n**Date de Création:** {}".format(revision.rev, revision.server_modified), color=0x9b59b6)
            embed.set_thumbnail(url=properties.CLOCK)
            embed.set_image(url= properties.DROP_IMG)
            await client_bot.say(embed=embed)

@client_bot.command()
async def restore(local_file, dropbox_dest, rev):
    """Restaurer une version du fichier"""
    if(len(rev) < 9):
        embed=discord.Embed(title="ERREUR", description="L'ID est incorrecte, il doit contenir 9 caractères", color=0xe74c3c)
        embed.set_thumbnail(url=properties.DANGER)
        embed.set_image(url= properties.DROP_IMG)
        return await client_bot.say(embed=embed)
    try:
        #On restaure une version du fichier dropbox
        dbx.files_restore(root + dropbox_dest, rev)
        #On télécharge le fichier dropbox en local
        dbx.files_download_to_file(local_file, root + dropbox_dest, rev)
    except ApiError as err:
        print("Erreur: {} ".format(err))
        embed=discord.Embed(title="ERREUR", description="Vérifier que l'élément existe bien\nRenseigner le bon chemin (pas de **/** au début)\nVérifier les extensions\nVérifier l'ID de la version", color=0xe74c3c)
        embed.set_thumbnail(url=properties.DANGER)
        embed.set_image(url= properties.DROP_IMG)
        return await client_bot.say(embed=embed)
    else:
        embed=discord.Embed(title="Restauration réussie", description="Restauration de votre fichier à une autre version réussi\n **ID de la version**: {}".format(rev), color=0x2ecc71)
        embed.set_thumbnail(url= properties.RESTORE)
        embed.set_image(url= properties.DROP_IMG)
        return await client_bot.say(embed=embed)

@client_bot.command()
async def copy(from_, to):
    """Copier un fichier ou un dossier de from_ à to des dossiers dropbox. Ainsi que les éléments partagés
       Ex: copy folder1 forlder2 (important! folder2 sera créé. Si un dossier du même nom on renomme folder2)
    """
    try:
        dbx.files_copy(root + from_, root + to, allow_shared_folder=True, autorename=True)
    except ApiError as err:
        print("Erreur: {} ".format(err))
        embed=discord.Embed(title="ERREUR", description="Vérifier que le fichier ou le dossier existe bien\nRenseigner le bon chemin (pas de **/** au début)", color=0xe74c3c)
        embed.set_thumbnail(url=properties.DANGER)
        embed.set_image(url= properties.DROP_IMG)
        return await client_bot.say(embed=embed)
    else:
        embed=discord.Embed(title="Copier réussie",color=0x2ecc71)
        embed.set_thumbnail(url= properties.COPY)
        embed.set_image(url= properties.DROP_IMG)
        embed.set_footer(text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        return await client_bot.say(embed=embed)

@client_bot.command()
async def move(from_, to):
    """Déplacer un fichier ou un dossier vers une autre destination. Sauf les éléments partagés
       Ex: move folder1 forlder2 (important! folder2 sera créé. Si un dossier du même nom on renomme folder2)
    """
    try:
        dbx.files_move(root + from_, root + to, allow_shared_folder=False, autorename=True)
    except ApiError as err:
        print("Erreur: {} ".format(err))
        embed=discord.Embed(title="ERREUR", description="Vérifier que le fichier ou le dossier existe bien\nRenseigner le bon chemin (pas de **/** au début)", color=0xe74c3c)
        embed.set_thumbnail(url=properties.DANGER)
        embed.set_image(url= properties.DROP_IMG)
        return await client_bot.say(embed=embed)
    else:
        embed=discord.Embed(title="Changement réussi",color=0x2ecc71)
        embed.set_thumbnail(url= properties.MOVE)
        embed.set_image(url= properties.DROP_IMG)
        embed.set_footer(text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        return await client_bot.say(embed=embed)

@client_bot.command()
async def shared():
    """Afficher les dossiers partagés"""
    try:
        share = dbx.sharing_list_folders(limit= 20)
    except ApiError as err:
        print("Erreur: {} ".format(err))
        embed=discord.Embed(title="ERREUR", description="Attention. un problème est survenu! Réessayéz plus tard", color=0xe74c3c)
        embed.set_thumbnail(url=properties.DANGER)
        embed.set_image(url= properties.DROP_IMG)
        return await client_bot.say(embed=embed)
    else:
        for entry in share.entries:
            if(entry.access_type.is_owner()):
                embed=discord.Embed(title="Dossier", description="**Nom:** {} \n"
                    "**Propriétaire:** Vous\n"
                    "**Droits:** Tous les droits\n"
                    "**Date invitation:** {} \n"
                    "**Téléchargement:** {} \n"
                    "**Visualisation:** {} \n"
                    "**Localisation:** {}"
                    .format(entry.name,
                            entry.time_invited,
                            re.sub(r"\?dl\=0", "?dl=1", entry.preview_url),
                            entry.preview_url,
                            entry.path_lower
                            ), color=0xf1c40f)
            elif(entry.access_type.is_editor()):
                embed=discord.Embed(title="Dossier", description="**Nom:** {} \n"
                    "**Propriétaire:** Autre\n"
                    "**Droits:** Consulter et Editer le dossier\n"
                    "**Date invitation:** {} \n"
                    "**Téléchargement:** {} \n"
                    "**Visualisation:** {} \n"
                    "**Localisation:** {}"
                    .format(entry.name,
                            entry.time_invited,
                            re.sub(r"\?dl\=0", "?dl=1", entry.preview_url),
                            entry.preview_url,
                            entry.path_lower
                            ), color=0xf1c40f)
            elif(entry.access_type.is_viewer()):
                embed=discord.Embed(title="Dossier", description="**Nom:** {} \n"
                    "**Propriétaire:** Autre\n"
                    "**Droits:** Vous pouvez jsute consulter le dossier\n"
                    "**Date invitation:** {} \n"
                    "**Téléchargement:** {} \n"
                    "**Visualisation:** {} \n"
                    "**Localisation:** {}"
                    .format(entry.name,
                            entry.time_invited,
                            re.sub(r"\?dl\=0", "?dl=1", entry.preview_url),
                            entry.preview_url,
                            entry.path_lower
                            ), color=0xf1c40f)
            elif(entry.access_type.is_viewer_no_comment()):
                embed=discord.Embed(title="Dossier", description="**Nom:** {} \n"
                    "**Propriétaire:** Autre\n"
                    "**Droits:** Vous pouvez jsute consulter le dossier, pas possible de commenter\n"
                    "**Date invitation:** {} \n"
                    "**Téléchargement:** {} \n"
                    "**Visualisation:** {} \n"
                    "**Localisation:** {}"
                    .format(entry.name,
                            entry.time_invited,
                            re.sub(r"\?dl\=0", "?dl=1", entry.preview_url),
                            entry.preview_url,
                            entry.path_lower
                            ), color=0xf1c40f)
            embed.set_thumbnail(url=properties.SHARE)
            embed.set_image(url= properties.DROP_IMG)
            await client_bot.say(embed=embed)

@client_bot.command()
async def share(path, email):
    """Partager un dossier avec d'autres personnes
       Ex: share dossier1/dossier2 pour dossier 1 ou share dossier1 pour dossier1
    """
    try:
        folder_launch = dbx.sharing_share_folder(root + path)
        meta_data = folder_launch.get_complete()
        print(meta_data)
        member_select = dropbox.sharing.MemberSelector.email(email)
        access_level = dropbox.sharing.AccessLevel.editor
        add_member = dropbox.sharing.AddMember(member_select, access_level)
        dbx.sharing_add_folder_member(meta_data.shared_folder_id, [add_member], custom_message= "Me rejoindre")
    except ApiError as err:
        print("Erreur: {} ".format(err))
        embed=discord.Embed(title="ERREUR", description="Vérifier le chemin du dossier", color=0xe74c3c)
        embed.set_thumbnail(url=properties.DANGER)
        embed.set_image(url= properties.DROP_IMG)
        return await client_bot.say(embed=embed)
    else:
        embed=discord.Embed(title="PARTAGE réussi", description="**{}** est bien ajouté au dossier".format(email), color=0x3498db)
        embed.set_thumbnail(url=properties.SHARE)
        embed.set_footer(text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        embed.set_image(url= properties.DROP_IMG)
        return await client_bot.say(embed=embed)

@client_bot.command()
async def link(path):
    """Générer un lien de partage vers un dossier dropbox"""
    try:
        result = dbx.sharing_create_shared_link(root + path, short_url=True)
    except ApiError as err:
        print("Erreur: {} ".format(err))
        embed=discord.Embed(title="ERREUR", description="Vérifier le chemin du dossier", color=0xe74c3c)
        embed.set_thumbnail(url=properties.DANGER)
        embed.set_image(url= properties.DROP_IMG)
        return await client_bot.say(embed=embed)
    else:
        embed=discord.Embed(title="Voilà le lien de partage vers l'élément dropbox", description="**Envoyer ce lien à la personne désirée: {}\nLien de téléchargement: {}".format(result.url, re.sub(r"\?dl\=0", "?dl=1", result.url)),color=0x3498db)
        embed.set_thumbnail(url= properties.SHARE_LINK)
        embed.set_footer(text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        embed.set_image(url= properties.DROP_IMG)
        await client_bot.say(embed=embed)

#####Fin dropbox#####

    
#####Météo#####

#En remplacement de certaines icones de l'API
weather_dict = {
    'clear sky':  properties.IMG_1,
    'few clouds': properties.IMG_2,
    'scattered clouds': properties.IMG_3,
    'broken clouds': properties.IMG_4,
    'shower rain': properties.IMG_9,
    'rain': properties.IMG_10,
    'thunderstorm': properties.IMG_11,
    'snow': properties.IMG_13,
    'mist': properties.IMG_50,
}

@client_bot.command()
async def weather(city, code):
    """Affiche la météo de la ville spécifiée"""
    url1 = 'http://api.openweathermap.org/data/2.5/weather?q='+city+','+code+'&appid='+secrets.WEATHER_KEY
    url2 = 'http://api.openweathermap.org/data/2.5/forecast?q='+city+','+code+'&appid='+secrets.WEATHER_KEY+'&ctn=8'

    async with aiohttp.ClientSession() as session:
        async with session.get(url1) as response:
            resp = await response.json()
    async with aiohttp.ClientSession() as session:
        async with session.get(url2) as response_2:
            resp_2 = await response_2.json()

    embed=discord.Embed(title="Ajourd'hui :calendar_spiral:", description=resp['weather'][0]['description'], color=0xffff00)
    #embed.set_thumbnail(url= properties.WEATHER_ICON + resp_2['list'][0]['weather'][0]['icon']+".png") 
    time = resp['weather'][0]['description']
    if time in weather_dict:
        embed.set_thumbnail(url = weather_dict[time])
        embed.set_image(url= weather_dict[time])
    else:
        embed.set_thumbnail(url= properties.WEATHER_ICON + resp_2['list'][0]['weather'][0]['icon']+".png")
        embed.set_image(url= properties.WEATHER_ICON + resp_2['list'][0]['weather'][0]['icon']+".png")
    embed.add_field(name="Température  :thermometer: ", value= "**"+str(int(resp['main']['temp']- 273.15))+" °C / "+ str(int((resp['main']['temp']- 273.15)*1.8000+32.00))+" °F**", inline=True)
    embed.add_field(name="Levé du soleil  :sunrise_over_mountains: ", value= "**"+str(datetime.datetime.fromtimestamp(resp['sys']['sunrise']))[11:16]+"**", inline=True)
    embed.add_field(name="Couché du soleil  :city_sunset: ", value= "**"+str(datetime.datetime.fromtimestamp(resp['sys']['sunset']))[11:16]+"**", inline=False)
    embed.add_field(name="Humidité  :droplet: ", value= "**"+str(resp['main']['humidity'])+' %**', inline=True)
    embed.add_field(name="Vent  :cyclone: ", value="**"+str(round(resp['wind']['speed']*3.6,1))+' km/h**', inline=True)
    #embed.add_field(name="Direction du vent  :triangular_flag_on_post: ", value="**"+str(int(resp['wind']['deg']))+' °**', inline=False)
    embed.add_field(name="Pression  :parking: ", value= "**"+str(resp['main']['pressure'])+' hPa**', inline=True)
    if 'visibility' in resp:
        embed.add_field(name="Visibilité  :eyeglasses: ", value= "**"+str(resp['visibility']/1000)+" km/h**", inline=True)
    else:
        embed.add_field(name="Visibilité  :eyeglasses: ", value= "--", inline=True)
    embed.add_field(name="Maximum  :point_up_2: ", value="**"+str(int(resp['main']['temp_max']- 273.15))+" °C / "+str(int((resp['main']['temp_max']- 273.15)*1.8000+32.00))+" °F**", inline=True)
    embed.add_field(name="Minimum  :point_down: ", value="**"+str(int(resp['main']['temp_min']- 273.15))+" °C / "+str(int((resp['main']['temp_min']- 273.15)*1.8000+32.00))+" °F**", inline=True)
    embed.set_footer(text="Dernière mise à jour: "+str(datetime.datetime.fromtimestamp(resp['dt']))[5:22])
    await client_bot.say(embed=embed)

#####Fin météo#####

client_bot.run(secrets.BOT_TOKEN)






