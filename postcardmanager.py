import os
from postcard_creator.postcard_creator import PostcardCreator, Postcard, Token, Recipient, Sender
from imagemanager import resize_image, get_datetime_taken, get_location_info
import settings
import time


def job():
    # Connection
    token = Token()
    print("\n\n\n===============================================================")
    print("Hi ! First of all, I will try to connect using your credentials")

    try:
        token.fetch_token(username=settings.config['username'], password=settings.config['password'],
                          method=settings.config['loginmethod'])
        print("Yaaasss I succeed")
    except Exception:
        print(
            "Sorry, an error occured while logging you in.\nCheck your username/password\nIf it still does not work, big L for you\nI will try again in one hour")
        return

    # Does the user has a free postcard available ?
    try:
        w = PostcardCreator(token)
        if settings.mockmode:
            print("Mock mode, let's go")
        elif not w.has_free_postcard():
            print("You don't have free postcard for the moment")
            return
    except Exception:
        print("Huuuum, a strange error occured, you should try to BURN YOUR COMPUTER")
        return

    print("I'm now searching for available picture to send")

    # Iterating over files in the folder
    for filename in os.listdir(settings.directory):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            filepath = os.path.join(settings.directory, filename)
            usedfilepath = os.path.join(settings.useddirectory, filename)
            print()
            print(f"I found one ! ({filename})")
            print(f"Full path is : {filepath}")
            print("I will now try to send the image")

            resize_image(filepath)
            cardWasSent = send_postcard(w, settings.config, filepath, usedfilepath)

            if cardWasSent:
                print("Card was sent")
                return
            else:
                print('Card was not sent, trying another...')
                time.sleep(1)


def send_postcard(w, config, filepath, usedfilepath):
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

    cardPicture = open(filepath, 'rb')

    message = ""
    message += config['card']['message']
    datetime = get_datetime_taken(filepath)
    if datetime is not None:
        message += " " + datetime
    message = message.replace(" ", "\n")

    location = get_location_info(filepath)
    if location[0] is not None:
        message += " " + location[0]
    if location[1] is not None:
        message += " " + location[1]

    card = Postcard(
        message=message,
        recipient=recipient,
        sender=sender,
        picture_stream=cardPicture)

    cardWasSent = w.send_free_card(postcard=card, mock_send=settings.mockmode, image_export=False)
    cardPicture.close()
    os.rename(filepath, usedfilepath)
    return cardWasSent
