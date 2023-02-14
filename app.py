import schedule
import time
import os
import json
from PIL import Image
from postcard_creator.postcard_creator import PostcardCreator, Postcard, Token, Recipient, Sender

directory = "appdata/images"
useddirectory = directory + r"\used";

config = json.load(open("appdata/configuration.json"))

def job():
    # Connexion
    token = Token()
    print("Hi ! First of all, I will try to connect using your credentials")

    try:
        token.fetch_token(username=config['username'], password=config['password'], method=config['loginmethod'])
        #token.has_valid_credentials(username=config['username'], password=config['password'])
        print("Yaaasss I succeed")
    except Exception:
        print("Sorry, an error occured while logging you in.\nCheck your username/password\nIf it still does not work, big L for you")
        exit()
        return

    # Test postcard gratuite dispo ou non
    try:
        w = PostcardCreator(token)
        if not w.has_free_postcard():
            print("You don't have free postcard for the moment")
            return
    except Exception:
        print("Huuuum, a strange error occured, you should try to BURN YOUR COMPUTER")


    print("I'm now searching for available picture to send")
    # Parcours des fichiers dans le répertoire
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.jpg', '.jpeg')):
            filepath = os.path.join(directory, filename)
            usedfilepath = os.path.join(useddirectory, filename)
            print(f"I found one ! ({filename})")
            print(f"Full path is : {filepath}")
            print("I will now try to send the image")
            try:
                #SEND IMAGE
                os.rename(filepath, usedfilepath)
            except Exception:
                print("I'm really bad... I was not able to send your postcard, I will try again in one hour !")

            return



schedule.every(1).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
