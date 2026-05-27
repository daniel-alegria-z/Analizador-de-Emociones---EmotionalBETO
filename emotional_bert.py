import gradio as gr  # type: ignore
from emotion_core import analizar_texto

def crear_interfaz():
    with gr.Blocks(title="EmotionalBETO", theme="soft") as demo:
        gr.Markdown("## 🧠 EmotionalBETO - Analizador de emociones")
        gr.Markdown("**Precisión de detección optimizada con umbrales**")

        with gr.Row():
            with gr.Column():
                entrada_texto = gr.Textbox(label="Escribe tu mensaje", lines=4)
                boton_enviar = gr.Button("Analizar", variant="primary")
                gr.Examples(
                    examples=[
                        ["Esto es increíble, me encanta 😊"],  # alegría
                        ["No puedo creer lo mal que ha ido..."],  # tristeza
                        ["¿Por qué no responden rápido?"],  # enojo/urgencia
                        ["Claro, como si todo estuviera bien..."],  # sarcasmo
                        ["¡Esto es increíble! Nunca volveré a comprar aquí."],  # enojo/sorpresa
                        ["Estoy muy feliz por el resultado obtenido."],  # alegría
                        ["Me siento muy triste hoy."],  # tristeza
                        ["Tengo miedo de lo que pueda pasar."],  # miedo
                        ["¡Esto es totalmente inaceptable!"],  # enojo
                        ["No esperaba que sucediera esto."],  # sorpresa
                        ["Gracias por tu ayuda, todo salió perfecto."],  # alegría
                        ["No me importa lo que digan los demás."],  # neutral
                        ["Estoy preocupado por la situación actual."],  # miedo
                        ["¡Qué alegría verte de nuevo!"],  # alegría
                        ["No tengo ninguna emoción al respecto."],  # neutral
                        ["¡Rápido! Necesito una respuesta urgente."],  # urgencia/enojo
                        ["No entiendo por qué pasó esto."],  # sorpresa/tristeza
                        ["Estoy satisfecho con el servicio recibido."],  # alegría
                        ["No me gustó para nada el trato que recibí."],  # enojo
                        ["¡Qué sorpresa tan agradable!"],  # sorpresa/alegría
                        ["No tengo palabras para describir lo que siento."],  # neutral/tristeza
                        ["Me siento seguro y tranquilo."],  # neutral
                        ["¡Esto es lo peor que me ha pasado!"],  # tristeza/enojo
                        ["No esperaba menos de ustedes, como siempre..."],  # sarcasmo
                        ["Por supuesto, todo salió mal como siempre."],  # sarcasmo/tristeza
                        ["Estoy asustado, no sé qué hacer."],  # miedo
                        ["¡Genial! Todo salió como esperaba."],  # alegría
                        ["No me interesa el resultado."],  # neutral
                        ["¡No puedo más con esta situación!"],  # enojo/tristeza
                        ["¿Por qué siempre me pasa esto a mí?"],  # tristeza
                    ],
                    inputs=entrada_texto
                )

            with gr.Column():
                salida_emocion = gr.Textbox(label="Emoción Principal")
                salida_confianza = gr.Textbox(label="Confianza")
                salida_grafica = gr.Plot(label="Distribución Emocional")
                salida_sarcasmo = gr.Textbox(label="Sarcasmo Detectado")
                salida_urgencia = gr.Textbox(label="Nivel de Urgencia")
                salida_respuesta = gr.Textbox(label="Respuesta Sugerida", lines=3)

        boton_enviar.click(
            fn=analizar_texto,
            inputs=entrada_texto,
            outputs=[
                salida_emocion,
                salida_confianza,
                salida_grafica,
                salida_sarcasmo,
                salida_urgencia,
                salida_respuesta
            ]
        )

    return demo


if __name__ == "__main__":
    print("Iniciando EmotionalBERT...")
    demo = crear_interfaz()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)