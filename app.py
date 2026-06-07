import gradio as gr

from compare_chunking import compare_for_query
from query import ask


def handle_query(question: str, use_hybrid: bool, show_comparison: bool) -> tuple:
    if not question.strip():
        return "", "", ""

    result = ask(question, use_hybrid=use_hybrid)

    sources_lines = [f"• {s}" for s in result["sources"]]
    sources_lines.append(f"\n[{result['retrieval_method']}]")
    sources_text = "\n".join(sources_lines)

    comp_text = compare_for_query(question) if show_comparison else ""
    return result["answer"], sources_text, comp_text


with gr.Blocks(title="UCI CS Unofficial Guide", theme=gr.themes.Soft()) as demo:
    gr.Markdown("## UCI CS Unofficial Course Guide\nAsk about courses, professors, schedules, and degree requirements.")

    inp = gr.Textbox(
        label="Your query",
        placeholder="e.g. What are some easy upper-div project courses?",
        lines=2,
    )

    with gr.Row():
        use_hybrid = gr.Checkbox(
            value=True,
            label="Hybrid Search (BM25 + Semantic)",
            info="Combines keyword and semantic search for better exact-match results.",
        )
        show_comparison = gr.Checkbox(
            value=False,
            label="Compare Chunking Strategies",
            info="Shows how Small / Medium / Large chunk sizes compare for this query. Slow on first run (~30s).",
        )

    btn = gr.Button("Submit", variant="primary")
    answer = gr.Textbox(label="Response", lines=10, interactive=False)
    sources = gr.Textbox(label="Sources", lines=5, interactive=False)
    comparison = gr.Textbox(
        label="Chunking Strategy Comparison (enable checkbox above to populate)",
        lines=14,
        interactive=False,
    )

    btn.click(
        handle_query,
        inputs=[inp, use_hybrid, show_comparison],
        outputs=[answer, sources, comparison],
    )
    inp.submit(
        handle_query,
        inputs=[inp, use_hybrid, show_comparison],
        outputs=[answer, sources, comparison],
    )


if __name__ == "__main__":
    demo.launch()
