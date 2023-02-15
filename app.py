import schedule
import time
from postcardmanager import job
import settings

schedule.every(1).hours.do(job)

print("Welcome to PostcardCreatorBot.\n\nThis script will be executed periodically, every hour.")
if settings.mockmode:
    print("Warning : Mock Mode activated")
while True:
    schedule.run_pending()
    time.sleep(1)