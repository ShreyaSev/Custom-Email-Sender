import gradio as gr
from create_prompt import process_data
import pandas as pd

def process_file(file, prompt, scheduled_at):


    process_data(file, prompt, scheduled_at)
    return "Emails sent successfully!"

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
    


    scheduled_at = gr.DateTime(label="Scheduled at", type="string")
    submit = gr.Button("Submit")
    output = gr.Textbox(label="Output")

    submit.click(fn = process_file, inputs = [file, prompt, scheduled_at], outputs = output)

demo.launch()