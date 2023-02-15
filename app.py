import schedule
import time
from postcardmanager import job

schedule.every(1).hours.do(job)

print("Welcome to PostcardCreatorBot.\n\nThis script will be executed periodically, every hour.")

while True:
    schedule.run_pending()
    time.sleep(1)