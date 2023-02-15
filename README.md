
# PostcardCreatorBot :incoming_envelope: :mailbox_with_no_mail:
## How it works :crystal_ball:
This bot run a python script inside a Docker image. Every hour, the script will
- Connect to Postcard Creator using yours credentials
- Check if a free postcard is available
- Send a Postcard
## Installation :electric_plug:
To install this bot, please follows thoses steps
- Download and install Docker Desktop
	- https://docs.docker.com/desktop/install/windows-install/ 
- Download this Github repository on your PC
	- https://github.com/malo-romano/PostcardCreatorBot/archive/refs/heads/main.zip
- Unzip it anywhere you want (C: drive, Desktop, whatever...)
- In the ``appdata`` folder, copy the ``configuration.json.template`` file and rename it to ``configuration.json``
- Open the file with an editor (notepad, notepad++, etc)
	- fill in your username/password (recommended to use a unique password for this app)
	-  select your login method (since june 2022, only SwissID is accepted by Post)
	- enter the sender and recipient informations
- Fill in the ``/appdata/images`` folder with beautiful pictures you want on hang to your wall
	- Please note : images must have an extension type of ``jpg`` or ``jpeg``.
- Run the ``RUN.bat`` script, by double-clicking it
