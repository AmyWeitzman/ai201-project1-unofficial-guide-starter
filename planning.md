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
| 18 | UCI University Registrar | UCI Schedule of Classes | https://www.reg.uci.edu/perl/WebSoc |

---

## Chunking Strategy

**Chunk size:** 800 characters

**Overlap:** 100 characters

**Reasoning:** My documents are a mix of different structures. The social media (Reddit, Quora) comments are short, but the course listings are long. Using a chunk size of 800 characters will help ensure I have a balance of capturing an entire thought (not cutting off mid-sentence) while not having too much additional content that confuses the LLM. The overlap of 100 characters will help me capture any longer comments so they don't get cut off. Also, I should use a recursive chunking strategy because my content is already naturally broken up into distinct sections by course title, post author, etc. A fixed size chunking strategy might include extra info from additional comments or cut off pat of the course listing while a semantic strategy isn't really necessary since my content is already structured such that similar topics are together.

---

## Retrieval Approach

**Embedding model:** `all-MiniLM-L6-v2` via `sentence-transformers`

**Top-k:** 5

**Production tradeoff reflection:** Using  `all-MiniLM-L6-v2` is fast and free, which is fine for the development phase, especially when I have a small corpus of documents that I can thoroughly review beforehand and determine best chunk size and overlap, and more easily debug if it's not performing well due to the limited number of users of this app. 

However, this model has a context length limit of 256 tokens so chunks longer than will get truncated automatically, which could cut off the end of a longer piece of text. In production, I'd probably want to use a model with a bigger context window such as `text-embedding-3-large`, which has a limit of 8,191 tokens. 

Another thing to consider is that my documents contain some domain-specific info and are written very informally. For instance, there is a lot of technical jargon that a general LLM may not have been trained on so it might not understand if a students asks what courses cover XYZ topic or it might not make the connection that certain topics are related so certain courses could be substitutes for each other. Also, students tends to write in informal language, so man of my documents contain slang, abbreviations, etc so the LLM might not understand those or interpret people's reviews of courses properly. 

It is also important to consider latency since larger models take longer to respond, which could make for a bad user experience, especially in a chat-style application. I'd want to balance picking models that perform well with ones that perform efficiently.

Finally, since all my sources are in English, multilingual support is not needed for this use case. If that was relevant however, I'd want to pick a model that has multi-lingual support.

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Which electives are recommended for undergrad CS majors interested in machine learning? | COMPSCI 178: Machine Learning and Data-Mining, IN4MATX 119: Engineering Artificial Intelligence Software, IN4MATX 141: Information Retrieval, COMPSCI 111: Digital Image Processing, COMPSCI 117: Project in Computer Vision, COMPSCI 172B: Neural Networks and Deep Learning. *(Sources: 1 — Reddit elective review, 9 — CS Courses Tier List, 14 — UCI Catalog COMPSCI, 15 — UCI Catalog IN4MATX)* |
| 2 | What is the best order to take the math course requirements (ex: ICS 6B, ICS 6D) and what is a sample schedule based on the course offerings? | Since MATH 2B is a prerequisite for most of the other math course requirements and MATH 2A is a prerequisite for that, you should start with MATH 2A as soon as possible. Note: MATH 2A/2B, MATH 3A, and STATS 67 are not included in the ICS/CS/INF schedule documents so specific section times cannot be retrieved from the available sources for those courses. For ICS math requirements, per the Fall 2026 schedule: ICS 6B is offered MWF 11:00â€“11:50am or MWF 3:00â€“3:50pm (both with Irene Gassko); ICS 6D is offered TuTh 11:00amâ€“12:20pm (with Jing Zhang); ICS 6N is not offered in Fall 2026. Based on the UCI BS CS sample program, a sample schedule for the math requirements is: Fall Yr1 — MATH 2A; Winter Yr1 — MATH 2B; Spring Yr1 — ICS 6B; Fall Yr2 — ICS 6D; Winter Yr2 — ICS 6N; Spring Yr2 — STATS 67. *(Sources: 12 — UCI BS CS Degree Requirements, 13 — UCI BS CS Sample Program, 16 — UCI Catalog I&C SCI, 18 — UCI Schedule of Classes)* |
| 3 | What are some upper-div project-based courses that are considered easy? | CS 145 (Embedded Systems) is described as "one of the most fun and easiest class I've taken at UCI"; CS 165 with Goodrich is described as "pretty chill"; INF 131 is described as an "easy A+". Notably, CS 125 is explicitly warned against ("stay far away") despite being a project course, due to little guidance and excessive concurrent workload. *(Sources: 6 — Reddit upper div project courses, 8 — Reddit low stress CS electives)* |
| 4 | Who is the best professor for ICS 32? I want someone with who does engaging lectures and doesn't grade hard. | Per the Fall 2026 schedule and RateMyProfessor: the regular ICS 32 section is taught by Thomas Yeh (MW 12:30â€“1:50p, quality 2.3/5, difficulty 3.8/5); the honors section (ICS H32) is taught by Alex Thornton (TuTh 6:30â€“7:50p, quality 4.2/5, difficulty 3.7/5). For engaging lectures and lenient grading, Alex Thornton is the significantly better-rated option. *(Sources: 11 — RateMyProfessor UCI CS, 17 — UCI ICS Course Offerings, 18 — UCI Schedule of Classes)* |
| 5 | I am deciding between COMPSCI 125, COMPSCI 163, and COMPSCI 179 electives. I want to take one in Fall 2026. I am available Tuesday/Thursday afternoons and Wednesday/Friday mornings. What class works with my schedule? | None of COMPSCI 125 (Next Generation Search Systems), COMPSCI 163 (Graph Algorithms), or COMPSCI 179 (Algorithms for Probabilistic and Deterministic Graphical Models) are offered in Fall 2026 per the UCI Schedule of Classes. The system should accurately report that none of the three are available in Fall 2026 rather than hallucinating schedule information. *(Source: 18 — UCI Schedule of Classes)* |

---

## Anticipated Challenges

1. **Semantic mismatch between informal Reddit language and formal queries.** Reddit comments use slang, abbreviations, and informal wording ("this class is an easy W", "stay far away from 125", "Klefstad is rough") that a student using this tool is unlikely to write word-for-word in a query. For instance, if someone types "What are low-stress upper-division electives?", it may not retrieve a chunk that says "CS 145 is honestly one of the easiest classes I've taken".

2. **Prerequisite chains split across chunk boundaries.** Course requirements are described as chains spanning multiple sentences (e.g., "MATH 2A is a prerequisite for MATH 2B, which is a prerequisite for ICS 6B, which is required before ICS 6D"). With an 800-character chunk size and recursive splitting, these chains can be cut in the middle, leaving one chunk with the first half of a prerequisite sequence and another with the second half. A query like "What do I need to take before ICS 6D?" might retrieve only one of those chunks and return an incomplete prerequisite list.

3. **Conflicting opinions across sources may produce inconsistent answers.** Because most documents are student reviews, the same course or professor can be rated very differently by different people. When the LLM retrieves chunks with opposing opinions, it may hard to decide on a good recommendation to respnd with, and thus it could give different answers to different people or just be vague and not provide a concrete recommendation.

---

## Architecture

```text
  documents/ folder
  (.txt files — Reddit, Quora, RateMyProfessor, UCI Catalogue, Schedule)
        |
        v
+----------------------------------+
|       Document Ingestion         |
|   Python (open / pathlib)        |
|   reads each .txt into memory    |
+----------------------------------+
        |
        v
+----------------------------------+
|           Chunking               |
|  RecursiveCharacterTextSplitter  |
|  chunk_size=800, overlap=100     |
+----------------------------------+
        |
        v
+----------------------------------+
|   Embedding + Vector Store       |
|  all-MiniLM-L6-v2               |
|  (sentence-transformers)         |
|  --> stored in ChromaDB          |
+----------------------------------+
        |  user query (embedded)
        v
+----------------------------------+
|           Retrieval              |
|  ChromaDB similarity search      |
|  returns top-k=5 chunks          |
+----------------------------------+
        |  retrieved chunks + query
        v
+----------------------------------+
|           Generation             |
|  Groq API (LLM)                  |
|  Gradio interface   |
+----------------------------------+
        |
        v
   answer to user
```

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

I will use Claude and give it the Chunking Strategy section of this planning document (chunk_size=800, overlap=100, RecursiveCharacterTextSplitter) and the Architecture diagram (Document Ingestion → Chunking stages), along with the documents/ folder structure (all .txt files). I expect it to write Python code with a function that reads every .txt file from documents/ and returns a list of chunks using `RecursiveCharacterTextSplitter` with my specified parameters. I will verify the output by printing the total number of chunks produced, spot-checking a sample of chunks to confirm they stay under 800 characters, don't cut mid-sentence, and that overlap is present at boundaries.

**Milestone 4 — Embedding and retrieval:**

I will use Claude and give it the Retrieval Approach section of this planning document (all-MiniLM-L6-v2, top-k=5, ChromaDB), the Architecture diagram (Embedding + Vector Store → Retrieval stages), and the chunk list outputed in Milestone 3. I expect it to write code that embeds all chunks using `sentence-transformers` and stores them in ChromaDB, plus a `query(text, k=5)` function that embeds the query and returns the top-5 most similar chunks. I will verify by running one of my evaluation queries and manually inspecting the 5 returned chunks to confirm they contain relevant content from the right source documents.

**Milestone 5 — Generation and interface:**

I will use Claude and give it the Architecture diagram (Generation stage), the Groq API library name from requirements.txt, and my Evaluation Plan's 5 test questions and expected answers. I expect it to produce a RAG pipeline function that takes a user query, retrieves top-k chunks via the Milestone 4 function, formats them into a prompt with a system message instructing the LLM to answer only from the provided context, calls the Groq API, and returns the response along with a Gradio interface with a text input and output. I will verify by running all 5 evaluation questions through the interface and comparing the answers against my expected answers in the Evaluation Plan.
