import gradio as gr
from create_prompt import process_data
import pandas as pd

def process_file(file, prompt, scheduled_at):


    process_data(file, prompt, scheduled_at)
    return "Emails sent successfully!"

# def on_button_click(column):
#     print(column)

# # Function to show placeholders by creating dynamic buttons
# def show_placeholders(file):
#     df = pd.read_csv(file.name)
#     columns = df.columns.to_list()

#     # Create a list of button components with their click events defined
#     buttons = []
#     for column in columns:
#         btn = gr.Button(column)
#         btn.click(
#             fn=on_button_click,
#             inputs=[gr.State(value=column)],
#             outputs=None,
#         )
#         buttons.append(btn)

#     return buttons

# # Function to dynamically create buttons based on CSV columns
# def show_placeholders(file):
#     df = pd.read_csv(file.name)
#     columns = df.columns.to_list()

#     # Return a list of buttons with their click events registered
#     button_components = []
#     for column in columns:
#         btn = gr.Button(column)
#         # Define click event within the context
#         btn.click(fn=on_button_click, inputs=[gr.State(value=column)], outputs=result_text)
#         button_components.append(btn)

#     return button_components
def on_click(current_text, column):
    return current_text + " " + "{" + column + "}"

with gr.Blocks() as demo:
    file = gr.File(label="Upload CSV file")
    
    @gr.render(inputs=file)
    def show_buttons(file):
        df = pd.read_csv(file.name)
        columns = df.columns.to_list()
        with gr.Row():
            for column in columns:
                gr.Button(column).click(fn = on_click, inputs = [prompt, gr.State(value=column)], outputs = prompt)

    prompt = gr.Textbox(label="Prompt", placeholder="Enter a prompt")
    


    scheduled_at = gr.DateTime(label="Scheduled at", type="string")
    submit = gr.Button("Submit")
    output = gr.Textbox(label="Output")

    submit.click(fn = process_file, inputs = [file, prompt, scheduled_at], outputs = output)

demo.launch()