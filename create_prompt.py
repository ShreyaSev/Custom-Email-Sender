import pandas as pd
from email_sender import send_email

import datetime
import time
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler


# Global variables to store job statuses and progress
job_statuses = []
progress = 0

def create_prompt(row, user_prompt):
    # user_prompt = f"Generate an email selling my marketing services to this company {company} located at {location} which sells these {products}"
    user_prompt_formatted = user_prompt.format(**row)
    return user_prompt_formatted

def generate_message(prompt):
    return f"This is a message: {prompt}"

def get_unix_timestamp(scheduled_at):
    # DateTime string
    # datetime_string = "2024-11-7 22:36:00"
    datetime_string = scheduled_at

    # Parse the string into a datetime object
    datetime_obj = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")

    # Convert to UNIX timestamp
    unix_timestamp = int(datetime_obj.timestamp())
    return unix_timestamp

def process_data(file=None, user_prompt = None, scheduling = False, scheduled_at=None, throttling = False, max_emails_per_hour = None):
    
    if scheduled_at:
        unix_timestamp = get_unix_timestamp(scheduled_at)
    if file is None:
        file = open('company_data.csv', 'r')
    df = pd.read_csv(file.name)


    THROTTLE_DELAY  = 3600 / max_emails_per_hour if throttling else 0
    scheduler = BackgroundScheduler()
       
    for idx, row in df.iterrows():
        email = row['Email']
        prompt = create_prompt(row, user_prompt=user_prompt)
        message = generate_message(prompt)
        scheduled_time = unix_timestamp if scheduled_at else None
        personalisation_dict = {"send_at": scheduled_time}
                
        run_time = (datetime.strptime(scheduled_at, "%Y-%m-%d %H:%M:%S") if scheduling else datetime.now()) + timedelta(seconds= idx * THROTTLE_DELAY)
        scheduler.add_job(send_email, args=[email, message, personalisation_dict], run_date=run_time, misfire_grace_time=5)
        
    scheduler.start()

    try:
        while True:
            time.sleep(2)
            if len(scheduler.get_jobs()) == 0:
                break
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

if __name__ == "__main__":
    process_data(user_prompt="Generate an email to {Company Name} located at {Location} promoting my marketing services to them, emphasizing my experience in selling {Products}.", 
                 scheduled_at="2024-11-8 23:37:00",
                 max_emails_per_hour=10)
