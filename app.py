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
    if not selected_categories:
        return None
    sources = []
    for cat in selected_categories:
        sources.extend(DOCUMENT_CATEGORIES[cat])
    return sources


def handle_query(
    question: str,
    use_hybrid: bool,
    show_comparison: bool,
    selected_categories: list[str],
) -> tuple:
    if not question.strip():
        return "", "", ""

    source_filter = resolve_source_filter(selected_categories)
    result = ask(question, use_hybrid=use_hybrid, source_filter=source_filter)

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

    gr.Markdown("**Filter by document type** — leave all unchecked to search everything")
    categories = gr.CheckboxGroup(
        choices=list(DOCUMENT_CATEGORIES.keys()),
        value=[],
        label="",
        interactive=True,
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

    inputs = [inp, use_hybrid, show_comparison, categories]
    outputs = [answer, sources, comparison]

    btn.click(handle_query, inputs=inputs, outputs=outputs)
    inp.submit(handle_query, inputs=inputs, outputs=outputs)


if __name__ == "__main__":
    demo.launch()
