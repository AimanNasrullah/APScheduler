from time import sleep
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler

# define job that needs to be executed
def display(msg):
    print("Message: ", msg)
    # job_id.remove()
    # scheduler.shutdown(wait=False)

# create scheduler instance (try one at a time)

# scheduler = BackgroundScheduler() # nothing output as it runs in background . If the main program ends this execution before background scheduler gets to do anything, the background scheduler shut down immediately.

scheduler = BlockingScheduler() #  blocks the main program from exiting, so the scheduled jobs can run.
x = "2"

# scheduler.add_job(display, 'interval', seconds=5) # whenever we call scheduler.add_job(), it returns a job id
# job_id = scheduler.add_job(display, 'interval', seconds=1, args=["Hello, world!"]) # can use job_id to manage the job later(cancel, etc)

# # scheduler multiple jobs
# job_id2 = scheduler.add_job(display, 'interval', seconds=3, args=["Job 1!"])
# job_id3 = scheduler.add_job(display, 'interval', seconds=5, args=["Job 2!"])

# # date trigger - run once at specific time
# job_id4 = scheduler.add_job(display, 'date', run_date=datetime(2025, 12, 22, 14, 25, 0), args=["Job Date!"]) # run_date can pass in string too : "2023-12-22 14:25:00"

# cron trigger - run at specific times like linux cron jobs
job_id5 = scheduler.add_job(display, 'cron', hour=16, minute=30, second="*", args=["Job Cron!"]) # runs every second when time is 16:30

scheduler.start() 
if isinstance(scheduler, BackgroundScheduler):
    print("If running BackgroundScheduler, this line will be printed immediately.")
else:
    print("If running BlockingScheduler, this line will be printed after scheduler is shut down.")

# can ignore this , just to shows isinstance usage
if isinstance(x, int):
    print("x is 2")
else:
    print("x is '2'")