import gradio as gr
from reflection.pipeline import reflection_pipeline_stream

def update_model(api_type):
    if api_type == "Together AI":
        return gr.Dropdown(
            choices=[
                "Qwen/Qwen2.5-72B-Instruct-Turbo",
                "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "meta-llama/Llama-2-70b-chat-hf"
            ],
            value="Qwen/Qwen2.5-72B-Instruct-Turbo"
        )
    else:
        return gr.Dropdown(
            choices=["mistralai/Mixtral-8x7B-Instruct-v0.1"],
            value="mistralai/Mixtral-8x7B-Instruct-v0.1"
        )

def create_app():
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.Markdown("# 🤔 ReAgent")
        
        with gr.Tabs():
            with gr.TabItem("Chat"):
                with gr.Row():
                    with gr.Column(scale=1):
                        user_input = gr.Textbox(
                            label="Your Input",
                            lines=3,
                            placeholder="Type your question or statement here..."
                        )
                        
                        api_type = gr.Radio(
                            choices=["Together AI", "Hugging Face"],
                            label="API Type",
                            value="Together AI"
                        )
                        
                        model = gr.Dropdown(
                            choices=[
                                "Qwen/Qwen2.5-72B-Instruct-Turbo",
                                "mistralai/Mixtral-8x7B-Instruct-v0.1",
                                "meta-llama/Llama-2-70b-chat-hf"
                            ],
                            label="Model",
                            value="Qwen/Qwen2.5-72B-Instruct-Turbo"
                        )
                        
                        api_key = gr.Textbox(
                            label="API Key",
                            placeholder="Enter your API key...",
                            type="password"
                        )
                        
                        with gr.Row():
                            temperature = gr.Slider(
                                minimum=0.0,
                                maximum=1.0,
                                value=0.7,
                                step=0.1,
                                label="Temperature"
                            )
                            
                            max_tokens = gr.Slider(
                                minimum=256,
                                maximum=4096,
                                value=1024,
                                step=256,
                                label="Max Tokens"
                            )
                        
                        context_window = gr.Slider(
                            minimum=1024,
                            maximum=8192,
                            value=4096,
                            step=1024,
                            label="Context Window"
                        )
                        
                        submit_btn = gr.Button("Start Reflection", variant="primary")
                    
                    with gr.Column(scale=2):
                        chat_history = gr.Chatbot(
                            label="Reflection Steps",
                            height=700,
                            type="messages",
                            show_label=False
                        )
            
            with gr.TabItem("Memory"):
                gr.Markdown("# 🚧 Coming Soon!")
                gr.Markdown("""
                The ability to save and view past reflections will be added in a future update.
                Stay tuned for this exciting feature!
                """)
        
        api_type.change(
            update_model,
            inputs=[api_type],
            outputs=[model]
        )
        
        submit_btn.click(
            reflection_pipeline_stream,
            [user_input, api_type, api_key, temperature, max_tokens, context_window, model],
            [chat_history]
        )
    
    return demo

if __name__ == "__main__":
    app = create_app()
    app.launch() 