import json

global directory
global useddirectory
global config
global mockmode

directory = "./appdata/images"  # Use this line when running on local machine
# directory = "/usr/pccb/appdata/images" # Use this line when building image for docker
useddirectory = directory + r"/used";

config = json.load(open("./appdata/configuration.json"))

mockmode = True
