# basic_aps_call.py
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def hello():
    print(f"[{datetime.now()}] Hello from APScheduler!")

if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="Asia/Kuala_Lumpur")

    # run hello() every 5 seconds
    scheduler.add_job(hello, trigger="interval", seconds=5, id="hello_job")

    print("Scheduler started. Press Ctrl+C to stop.")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")