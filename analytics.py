import gradio as gr
import pandas as pd
from flask import Flask, request, jsonify
from threading import Thread

class EmailAnalytics:
# Initialize Flask app and Gradio app
    def __init__(self):
  
        self.app = Flask(__name__)

        # Initialize the global dataframe with required columns
        self.email_data = pd.DataFrame(columns=["Email", "Status", "Delivery Status", "Opened"])

        # Webhook route to receive data and update the dataframe
        @self.app.route('/webhook/sendgrid', methods=['POST'])
        def webhook():

            # Get JSON data from the incoming webhook
            events = request.get_json()

            for event in events:
                new_row = {
                    "Email": None,
                    "Status": None,
                    # "Delivery Status": "N/A",
                    # "Opened": "N/A"
                }
                email = event.get('email')
                status = event.get("event")
                new_row["Email"] = email
                new_row["Status"] = status
                    

            self.email_data = pd.concat([self.email_data, pd.DataFrame([new_row])], ignore_index=True)

            # Return success response
            return jsonify({"status": "success"}), 200

    # Function to get the current dataframe for Gradio
    def get_data(self):
        return self.email_data

    # # Function to run Flask in a separate thread to avoid blocking Gradio
    # def start_flask(self):
    #     self.app.run(port=5000, debug=True, use_reloader=False)

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