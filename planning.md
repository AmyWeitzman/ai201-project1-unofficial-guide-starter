# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

This unofficial guide helps students plan their course schedules as computer science students at the University of California, Irvine based on student reviews and availability of courses. This knowledge is valuable so students can effectively plan their courses so they meet the graduation requirements on time and ensure they have the best experience so they aren't stuck with bad professors, 8am classes, tough electives, etc. Real reviews of professors aren't available through official school resources and it can be difficult for one to synthesize all the course requirements and schedule of classes manually to pick the best schedule for them. Having all these resources in a central location and being able to query it simply with natural language woul help speed up course planning for students and ensure they don't overlook certain requirements.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit | A Review of Every Undergraduate CS Elective I Took | https://www.reddit.com/r/UCI/comments/1s5gwzm/a_review_of_every_undergraduate_cs_elective_i_took/ |
| 2 | Reddit | Schedule for CS Major | https://www.reddit.com/r/UCI/comments/vq3psd/schedule_for_cs_major/ |
| 3 | Reddit | Which schedule is better for a CS major? | https://www.reddit.com/r/UCI/comments/tkgdxg/which_schedule_is_better_for_a_cs_major/ |
| 4 | Reddit | Easy classes of Computer Science? | https://www.reddit.com/r/UCI/comments/cf3ob5/easy_classes_of_computer_science/ |
| 5 | Reddit | Any cs course recommendations from this list? | https://www.reddit.com/r/UCI/comments/1jr11gq/any_cs_course_recommendations_from_this_list/ |
| 6 | Reddit | What are some good CS upper div project courses? | https://www.reddit.com/r/UCI/comments/asi82z/what_are_some_good_cs_upper_div_project_courses/ |
| 7 | Reddit | CS upper-division class recommendation | https://www.reddit.com/r/UCI/comments/unlhxa/cs_upperdivision_class_recommendation/ |
| 8 | Reddit | Low stress CS electives | https://www.reddit.com/r/UCI/comments/jw4csm/low_stress_cs_electives/ |
| 9 | Reddit | CS Courses Tier List | https://www.reddit.com/r/UCI/comments/13866f3/cs_courses_tier_list/ |
| 10 | Quora | What are some good courses to take at the Donald Bren School of Information and Computer Science in the University of California, Irvine? | https://www.quora.com/What-are-some-good-courses-to-take-at-the-Donald-Bren-School-of-Information-and-Computer-Science-in-the-University-of-California-Irvine |
| 11 | RateMyProfessor | Rate My Professor: Computer Science department at UC Irvine | https://www.ratemyprofessors.com/search/professors/1074?q=*&did=11 |
| 12 | UCI General Catalogue | UCI BS in CS Degree Requirements | https://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/computerscience_bs/#requirementstext |
| 13 | UCI General Catalogue | UCI BS in CS Sample Program| https://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/computerscience_bs/#sampleprogramtext |
| 14 | UCI General Catalogue | UCI Catalog: Computer Science (COMPSCI) | https://catalogue.uci.edu/allcourses/compsci/ |
| 15 | UCI General Catalogue | UCI Catalog: Informatics (IN4MATX) | https://catalogue.uci.edu/allcourses/in4matx/ |
| 16 | UCI General Catalogue | UCI Catalog: Information and Computer Science (I&C SCI) | https://catalogue.uci.edu/allcourses/i_c_sci/ |
| 17 | UCI Course Listing | UCI Information and Computer Sciences (ICS) Course Offerings | https://ics.uci.edu/course_listing/ |
| 17 | UCI University Registrar | UCI Schedule of Classes | https://www.reg.uci.edu/perl/WebSoc |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
