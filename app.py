import schedule
import time
import os
import json
from PIL import Image
from postcard_creator.postcard_creator import PostcardCreator, Postcard, Token, Recipient, Sender

directory = "/usr/pccb/appdata/images"
useddirectory = directory + r"/used";

config = json.load(open("/usr/pccb/appdata/configuration.json"))


def job():
    # Connexion
    token = Token()
    print("\n\n\n===============================================================")
    print("Hi ! First of all, I will try to connect using your credentials")

    try:
        token.fetch_token(username=config['username'], password=config['password'], method=config['loginmethod'])
        print("Yaaasss I succeed")
    except Exception:
        print("Sorry, an error occured while logging you in.\nCheck your username/password\nIf it still does not work, big L for you\nI will try again in one hour")
        return

    # Does the user has a free postcard available ?
    try:
        w = PostcardCreator(token)
        if not w.has_free_postcard() :
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
            print()
            print(f"I found one ! ({filename})")
            print(f"Full path is : {filepath}")
            print("I will now try to send the image")

            cardWasSent = False

            try:
                recipient = Recipient(
                    prename=config['recipient']['firstname'],
                    lastname=config['recipient']['lastname'],
                    street=config['recipient']['street'],
                    place=config['recipient']['city'],
                    zip_code=config['recipient']['npa'])

                sender = Sender(
                    prename=config['sender']['firstname'],
                    lastname=config['sender']['lastname'],
                    street=config['sender']['street'],
                    place=config['sender']['city'],
                    zip_code=config['sender']['npa'])

                initialPic = Image.open(filepath)

                initialPic.close()
                cardPicture = open(filepath, 'rb')
                card = Postcard(
                    message=config['card']['message'],
                    recipient=recipient,
                    sender=sender,
                    picture_stream=cardPicture)

                cardWasSent = w.send_free_card(postcard=card, mock_send=False, image_export=False)
                cardPicture.close()
                os.rename(filepath, usedfilepath)
            except Exception:
                print("I'm a bad robot ... I was not able to send your postcard, I will try again in one hour !")
            if cardWasSent:
                print("Card was sent")
                return
            else:
                print('Card was not sent, trying another...')



schedule.every(1).hours.do(job)
print("Welcome to PostcardCreatorBot.\n\nThis script will be executed periodically, every hour.")
while True:
    schedule.run_pending()
    time.sleep(1)
