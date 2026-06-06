import gradio as gr

from query import ask

def handle_query(question: str) -> tuple[str, str]:
    if not question.strip():
        return "", ""
    
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])

    return result["answer"], sources


with gr.Blocks(title="UCI CS Unofficial Guide", theme=gr.themes.Soft()) as demo:
    gr.Markdown("## UCI CS Unofficial Course Guide\nAsk about courses, professors, schedules, and degree requirements.")

    inp = gr.Textbox(label="Your query", placeholder="e.g. What are some easy upper-div project courses?", lines=2)
    btn = gr.Button("Submit", variant="primary")
    answer = gr.Textbox(label="Response", lines=10, interactive=False)
    sources = gr.Textbox(label="Sources", lines=4, interactive=False)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

if __name__ == "__main__":
    demo.launch()
