import gradio as gr
from create_prompt import process_data
import pandas as pd

def process_file(file, prompt):

    process_data(file, prompt)
    return "Emails sent successfully!"

# iface = gr.Interface(fn=process_file, inputs="file", outputs="text")
# iface.launch()
with gr.Blocks() as demo:
    file = gr.File(label="Upload CSV file")
    prompt = gr.Textbox(label="Prompt", placeholder="Enter a prompt")
    submit = gr.Button("Submit")
    output = gr.Textbox(label="Output")

    submit.click(fn = process_file, inputs = [file, prompt], outputs = output)

demo.launch()