import os
import json
from PIL import Image
from postcard_creator.postcard_creator import PostcardCreator, Postcard, Token, Recipient, Sender

directory = "./appdata/images" # Use this line when running on local machine
#directory = "/usr/pccb/appdata/images" # Use this line when building image for docker
useddirectory = directory + r"/used";

config = json.load(open("./appdata/configuration.json"))

mockmode = True

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
        if mockmode:
            print("Mock mode, let's go")
        elif not w.has_free_postcard():
            print("You don't have free postcard for the moment")
            return
    except Exception:
        print("Huuuum, a strange error occured, you should try to BURN YOUR COMPUTER")
        return

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

            cardWasSent = send_postcard(w, config, filepath, usedfilepath)

            if cardWasSent:
                print("Card was sent")
                return
            else:
                print('Card was not sent, trying another...')


def send_postcard(w, config, filepath, usedfilepath):
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

        resize_image(filepath)
        cardPicture = open(filepath, 'rb')
        card = Postcard(
            message=config['card']['message'],
            recipient=recipient,
            sender=sender,
            picture_stream=cardPicture)

        cardWasSent = w.send_free_card(postcard=card, mock_send=mockmode, image_export=False)
        cardPicture.close()
        os.rename(filepath, usedfilepath)
        return cardWasSent

    except Exception as e:
        print("I'm a bad robot ... I was not able to send your postcard : " + str(e))
        return False

def resize_image(filepath):
    image = Image.open(filepath)
    width = image.size[0]
    height = image.size[1]
    landscape = True if width > height else False
    minwidth = 1819 if landscape else 1311
    minheight = 1311 if landscape else 1819
    ratioWE = width / height
    ratioEW = height / width
    if width < minwidth or height < minheight:
        print("Image too small, resizing it")
        newwidth = 0
        newheight = 0
        if width < minwidth:
            newwidth = minwidth
            newheight = minwidth * ratioEW
        if newheight < minheight:
            newheight = minheight
            newwidth = minheight * ratioWE

        image_resized = image.resize((int(newwidth), int(newheight)))
        image.close()
        image_resized.save(filepath)
        image_resized.close()