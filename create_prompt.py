import pandas as pd
from email_sender import send_email

import datetime

# DateTime string
datetime_string = "2024-11-7 22:36:00"

# Parse the string into a datetime object
datetime_obj = datetime.datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")

# Convert to UNIX timestamp
unix_timestamp = int(datetime_obj.timestamp())

def create_prompt(row):
    company = row["Company Name"]
    location = row["Location"]
    products = row["Products"]
    user_prompt = f"Generate an email selling my marketing services to this company {company} located at {location} which sells these {products}"
 
    return user_prompt

def generate_message(prompt):
    return f"This is a message: {prompt}"


def process_data():
    df = pd.read_csv('company_data.csv')
    count = 0
    scheduled_time = unix_timestamp
    personalisation_dict = {"send_at": scheduled_time}
    for idx, row in df.iterrows():
        email = row['Email']
        prompt = create_prompt(row)
        message = generate_message(prompt)
        send_email(to_email = email, message_content = message, personalisations_dict = personalisation_dict)
        count+=1
        if count==3:
            break
        

if __name__ == "__main__":
    process_data()
