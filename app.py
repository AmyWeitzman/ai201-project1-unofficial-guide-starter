import gradio as gr

from compare_chunking import compare_for_query
from query import ask

DOCUMENT_CATEGORIES: dict[str, list[str]] = {
    "Student Reviews": [
        "cs_course_recommendations.txt",
        "cs_courses_tier_list.txt",
        "cs_upper_division_class_recommendation.txt",
        "easy_classes_computer_science.txt",
        "good_courses_uci_ics.txt",
        "good_cs_upper_div_project_courses.txt",
        "low_stress_cs_electives.txt",
        "rate_my_professor.txt",
        "review_of_every_undergrad_cs_elective.txt",
    ],
    "Course Catalog": [
        "courses_cs.txt",
        "courses_ics.txt",
        "courses_inf.txt",
    ],
    "Course Offerings": [
        "course_offerings_cs.txt",
        "course_offerings_cs_reg.txt",
        "course_offerings_ics.txt",
        "course_offerings_ics_reg.txt",
        "course_offerings_inf.txt",
        "course_offerings_inf_reg.txt",
    ],
    "Requirements & Planning": [
        "cs_requirements.txt",
        "cs_sample_plan.txt",
        "schedule_for_cs_major.txt",
        "schedule_for_cs_major_2.txt",
    ],
}


def resolve_source_filter(selected_categories: list[str]) -> list[str] | None:
    # No filter when nothing or everything is selected
    if not selected_categories or set(selected_categories) == set(DOCUMENT_CATEGORIES.keys()):
        return None
    sources = []
    for cat in selected_categories:
        sources.extend(DOCUMENT_CATEGORIES[cat])
    return sources


def build_source_footer(result: dict) -> str:
    parts = []
    if result["sources"]:
        parts.append("**Sources:** " + " · ".join(result["sources"]))
    parts.append(f"*{result['retrieval_method']}*")
    return "\n\n---\n" + "\n\n".join(parts)


def handle_query(
    question: str,
    use_hybrid: bool,
    show_comparison: bool,
    selected_categories: list[str],
    history: list[dict],
    chatbot_val: list,
) -> tuple:
    if not question.strip():
        return chatbot_val, "", history, ""

    source_filter = resolve_source_filter(selected_categories)
    result = ask(
        question,
        use_hybrid=use_hybrid,
        source_filter=source_filter,
        history=history,
    )

    # Clean history for Groq API — no source footers
    new_history = history + [
        {"role": "user", "content": question},
        {"role": "assistant", "content": result["answer"]},
    ]

    # Chatbot display — answer with source footer appended
    new_chatbot = (chatbot_val or []) + [
        {"role": "user", "content": question},
        {"role": "assistant", "content": result["answer"] + build_source_footer(result)},
    ]

    comp_text = compare_for_query(question) if show_comparison else ""

    return new_chatbot, comp_text, new_history, ""


def clear_conversation() -> tuple:
    return [], "", [], ""


with gr.Blocks(title="ChatZOT", theme=gr.themes.Soft()) as demo:
    gr.Markdown("### The UCI Unofficial Course Guide for CS Majors\nAsk about courses, professors, schedules, and degree requirements.")

    history_state = gr.State([])

    with gr.Accordion("Filters & Settings", open=False):
        categories = gr.CheckboxGroup(
            choices=list(DOCUMENT_CATEGORIES.keys()),
            value=list(DOCUMENT_CATEGORIES.keys()),
            label="Source Type",
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
                info="Compares small/medium/large chunking strategies and displays results in the Chunking Strategies Comparison panel below the chat. (Note: takes about ~30s to run the first time).",
            )

    chatbot = gr.Chatbot(label="Chat", height=450)

    inp = gr.Textbox(
        label="Query",
        show_label=False,
        placeholder="What are some project-based upper-div courses?",
        lines=2,
    )
    with gr.Row():
        btn = gr.Button("Submit", variant="primary", scale=3)
        clear_btn = gr.Button("New Chat", variant="secondary", scale=1)

    with gr.Accordion("Chunking Strategy Comparison", open=False):
        comparison = gr.Textbox(
            label="",
            show_label=False,
            lines=14,
            interactive=False,
            placeholder="Enable 'Compare Chunking Strategies' in settings above, then submit a query.",
        )

    inputs = [inp, use_hybrid, show_comparison, categories, history_state, chatbot]
    outputs = [chatbot, comparison, history_state, inp]

    btn.click(handle_query, inputs=inputs, outputs=outputs)
    inp.submit(handle_query, inputs=inputs, outputs=outputs)
    clear_btn.click(clear_conversation, outputs=[chatbot, comparison, history_state, inp])


if __name__ == "__main__":
    demo.launch(favicon_path="./petr.png")
