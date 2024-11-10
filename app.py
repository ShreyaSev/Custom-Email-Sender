import gradio as gr
from create_prompt import process_data
import datetime
import pandas as pd

def process_file(file, prompt, scheduling, scheduled_at, throttling, max_emails_per_hour):


    process_data(file, prompt, scheduling, scheduled_at, throttling, max_emails_per_hour)
    return "Emails sent successfully!"

def toggle_throttling(throttling):
    return gr.update(visible=throttling)

def toggle_scheduling(scheduling):
    return gr.update(visible=scheduling)

def on_click(current_text, column):
    return current_text + " " + "{" + column + "}"

with gr.Blocks() as demo:
    gr.Markdown("# Custom Email Sender Application")
    file = gr.File(label="Upload CSV file")

    @gr.render(inputs=file)
    def show_buttons(file):
        df = pd.read_csv(file.name)
        columns = df.columns.to_list()
        gr.Markdown("## Select placeholders to include in the prompt")
        with gr.Row():
            for column in columns:
                gr.Button(column).click(fn = on_click, inputs = [prompt, gr.State(value=column)], outputs = prompt)

    prompt = gr.Textbox(label="Prompt", placeholder="Enter a prompt")
    
    with gr.Accordion(label="Scheduling Options" , open=False):
        scheduling = gr.Checkbox(label="Schedule Emails")
        scheduled_at = gr.DateTime(label="Select a date and time: ", type="string", visible=False)
        throttling = gr.Checkbox(label="Throttle Emails")
        max_emails_per_hour = gr.Number(label="Max emails per hour", interactive=True, value=10, visible=False)
        
        scheduling.change(toggle_scheduling, inputs = [scheduling], outputs = [scheduled_at])
        throttling.change(toggle_throttling, inputs = [throttling], outputs = [max_emails_per_hour])
        

    submit = gr.Button("Submit")
    output = gr.Textbox(label="Output")

    
    submit.click(fn = process_file, inputs = [file, prompt, scheduling, scheduled_at,throttling,max_emails_per_hour], outputs = output)

demo.launch()