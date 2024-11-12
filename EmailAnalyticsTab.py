import gradio as gr
import pandas as pd
from flask import Flask, request, jsonify
from threading import Thread
import pandas as pd
from pymongo import MongoClient
from collections import defaultdict

class EmailAnalytics:
# Initialize Flask app and Gradio app
    def __init__(self):

        # Connect to MongoDB
        self.client = MongoClient('mongodb://localhost:27017/')  # For local MongoDB
        self.db = self.client['email_tracking']  # Database name
        self.emails_collection = self.db['emails_sent']  # Collection name
        self.clear_collection_on_init()
        self.app = Flask(__name__)
        # Webhook route to receive data and update the dataframe
        @self.app.route('/webhook/sendgrid', methods=['POST'])
        def webhook():

            # Get JSON data from the incoming webhook
            events = request.get_json()

            #group events because some events can have multiple updates for one email id, but we want only the latest one
            grouped_events = defaultdict(list)
            for event in events:
                email = event.get('email')
                grouped_events[email].append(event)

            # Process each group of events for an email
            for email, email_events in grouped_events.items():
                # Sort events for this email by timestamp (most recent first)
                sorted_events = sorted(email_events, key=lambda x: x['timestamp'], reverse=True)
                
                # Get the most recent event
                latest_event = sorted_events[0]
                event_status = latest_event.get('event')
                event_timestamp = latest_event.get('timestamp')

                # Fetch the current status from the database for comparison
                current_status = self.emails_collection.find_one({"email_id": email})

                # Update only if the current status is different or if the status has not been updated before
                if current_status is None or current_status['status'] != event_status:
                    print(f"Updating {email} to {event_status}")
                    self.emails_collection.update_one(
                        {"email_id": email},
                        {"$set": {"status": event_status}}
                    )

            return jsonify({"status": "success"}), 200
    
    def clear_collection_on_init(self):
        self.emails_collection.delete_many({})
    # Function to get the current dataframe for Gradio
    def get_data(self):
        # Query the MongoDB collection and retrieve all documents
        emails_cursor = self.emails_collection.find()  # You can add query parameters if needed

        # Convert the cursor to a list of dictionaries (which is what DataFrame expects)
        emails_data = list(emails_cursor)
        # Convert cursor to list and remove _id  and sg_message_id field from each document
        for document in emails_data:
            # Drop the _id field
            document.pop('_id', None)
            document.pop('sg_message_id', None)

        # Convert to Pandas DataFrame
        if not emails_data:
            emails_df = pd.DataFrame(columns=['Company Name', 'Email', 'Status'])
        else:
            emails_df = pd.DataFrame(data=emails_data)
            emails_df.rename(columns={
            'company_name': 'Company Name',
            'email_id': 'Email',
            'status': 'Status'
            }, inplace=True)
        
        return emails_df

    # Set up Gradio app
    def create_dashboard(self):
        with gr.TabItem("Email Analytics"):
            gr.Markdown("# 📊 Real-Time Email Analytics Dashboard")
            
            # DataFrame component to show the updated data
            with gr.Row():
                gr.DataFrame(self.get_data, every=gr.Timer(5), label="Email Status Dashboard")
    
    def start_webhook_server(self):
        # Run Flask in a separate thread to avoid blocking Gradio
        Thread(target=self.app.run, kwargs={"port": 5000}).start()