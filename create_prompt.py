import pandas as pd
from email_sender import send_email

import datetime



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

def process_data(file=None, user_prompt = None, scheduled_at=None):
    if scheduled_at:
        unix_timestamp = get_unix_timestamp(scheduled_at)
    if file is None:
        file = open('company_data.csv', 'r')
    df = pd.read_csv(file.name)
    count = 0
    scheduled_time = unix_timestamp if scheduled_at else None
    personalisation_dict = {"send_at": scheduled_time}
    for idx, row in df.iterrows():
        email = row['Email']
        prompt = create_prompt(row, user_prompt=user_prompt)
        message = generate_message(prompt)
        send_email(to_email=email, message_content=message, personalisations_dict=personalisation_dict)

        #remove this before finishing
        count += 1
        if count == 3:
            break
        

if __name__ == "__main__":
    process_data()
