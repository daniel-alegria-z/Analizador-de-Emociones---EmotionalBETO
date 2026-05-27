import gradio as gr  # type: ignore

from emotional_bert import crear_interfaz


demo = crear_interfaz()


if __name__ == "__main__":
    print("Iniciando EmotionalBETO para Hugging Face Spaces...")
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
