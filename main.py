# main.py
import gradio as gr
from threading import Thread
from EmailSenderTab import create_email_sender_tab
from EmailAnalyticsTab import EmailAnalytics

def main():
    # Initialize analytics
    analytics = EmailAnalytics()
    
    # Start webhook server in a separate thread
    webhook_thread = Thread(target=analytics.start_webhook_server)
    webhook_thread.daemon = True
    webhook_thread.start()
  
    with gr.Blocks() as demo:
        with gr.Tabs():
            # Email sender tab
            create_email_sender_tab()
            
            # Analytics tab
            analytics.create_dashboard()
        
    # Launch the application
    demo.launch()

if __name__ == "__main__":
    main()