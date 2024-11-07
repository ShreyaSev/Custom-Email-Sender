import pandas as pd
from email_sender import send_email

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
    for idx, row in df.iterrows():
        email = row['Email']

        prompt = create_prompt(row)
        message = generate_message(prompt)
        send_email(to_email = email, message_content = message)
        count+=1
        if count==3:
            break
        

if __name__ == "__main__":
    process_data()
