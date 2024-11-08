import pandas as pd
from email_sender import send_email

import datetime
import time
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler



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
    datetime_obj = datetime.datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")

    # Convert to UNIX timestamp
    unix_timestamp = int(datetime_obj.timestamp())
    return unix_timestamp

def process_data(file=None, user_prompt = None, scheduled_at=None, max_emails_per_hour = None, batch_size = None):
    
    if scheduled_at:
        unix_timestamp = get_unix_timestamp(scheduled_at)
    if file is None:
        file = open('company_data.csv', 'r')
    df = pd.read_csv(file.name)


    BATCH_SIZE = batch_size if batch_size else len(df)
    THROTTLE_DELAY  = 3600 / max_emails_per_hour if max_emails_per_hour else 0
    scheduler = BackgroundScheduler()
    count = 0
   
    # for idx, row in df.iterrows():
    #     email = row['Email']
    #     prompt = create_prompt(row, user_prompt=user_prompt)
    #     message = generate_message(prompt)
    #     scheduled_time = unix_timestamp if scheduled_at else None
    #     personalisation_dict = {"send_at": scheduled_time}
        
    #     send_email(to_email=email, message_content=message, personalisations_dict=personalisation_dict)

    #     #remove this before finishing
    #     count += 1
    #     if count == 3:
    #         break

    batches = [df[i:i+batch_size] for i in range(0, len(df), batch_size)]

    def schedule_batch(batch_df):
        for _, row in batch_df.iterrows():
            email = row['Email']
            prompt = create_prompt(row, user_prompt=user_prompt)
            message = generate_message(prompt)
            scheduled_time = unix_timestamp if scheduled_at else None
            personalisation_dict = {"send_at": scheduled_time}
            send_email(to_email=email, message_content=message, personalisations_dict=personalisation_dict)
            time.sleep(THROTTLE_DELAY)
        
    if max_emails_per_hour:
        for idx,batch in enumerate(batches):
            run_time = datetime.now() + timedelta(minutes=idx * (60 / max_emails_per_hour))
            scheduler.add_job(schedule_batch, 'date', run_date=run_time, args=[batch])
        
        print("Emails scheduled with throttling")

    else:
        for batch in batches:
            schedule_batch(batch)
        print("Emails scheduled without throttling")

if __name__ == "__main__":
    process_data()
