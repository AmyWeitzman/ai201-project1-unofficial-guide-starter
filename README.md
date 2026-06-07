# The Unofficial Guide — Project 1

## Domain

This unofficial guide helps students plan their course schedules as computer science students at the University of California, Irvine based on student reviews and availability of courses. This knowledge is valuable so students can effectively plan their courses so they meet the graduation requirements on time and ensure they have the best experience so they aren't stuck with bad professors, 8am classes, tough electives, etc. Real reviews of professors aren't available through official school resources and it can be difficult for one to synthesize all the course requirements and schedule of classes manually to pick the best schedule for them. Having all these resources in a central location and being able to query it simply with natural language woul help speed up course planning for students and ensure they don't overlook certain requirements.

---

## Document Sources

| # | Source | Type | URL | Local file |
| --- | --- | --- | --- | --- |
| 1 | Reddit r/UCI — "A Review of Every Undergraduate CS Elective I Took" | Student review | [Reddit thread](https://www.reddit.com/r/UCI/comments/1s5gwzm/a_review_of_every_undergraduate_cs_elective_i_took/) | documents/review_of_every_undergrad_cs_elective.txt |
| 2 | Reddit r/UCI — "Schedule for CS Major" | Student advice | [Reddit thread](https://www.reddit.com/r/UCI/comments/vq3psd/schedule_for_cs_major/) | documents/schedule_for_cs_major.txt |
| 3 | Reddit r/UCI — "Which schedule is better for a CS major?" | Student advice | [Reddit thread](https://www.reddit.com/r/UCI/comments/tkgdxg/which_schedule_is_better_for_a_cs_major/) | documents/schedule_for_cs_major_2.txt |
| 4 | Reddit r/UCI — "Easy classes of Computer Science?" | Student review | [Reddit thread](https://www.reddit.com/r/UCI/comments/cf3ob5/easy_classes_of_computer_science/) | documents/easy_classes_computer_science.txt |
| 5 | Reddit r/UCI — "Any cs course recommendations from this list?" | Student review | [Reddit thread](https://www.reddit.com/r/UCI/comments/1jr11gq/any_cs_course_recommendations_from_this_list/) | documents/cs_course_recommendations.txt |
| 6 | Reddit r/UCI — "What are some good CS upper div project courses?" | Student review | [Reddit thread](https://www.reddit.com/r/UCI/comments/asi82z/what_are_some_good_cs_upper_div_project_courses/) | documents/good_cs_upper_div_project_courses.txt |
| 7 | Reddit r/UCI — "CS upper-division class recommendation" | Student review | [Reddit thread](https://www.reddit.com/r/UCI/comments/unlhxa/cs_upperdivision_class_recommendation/) | documents/cs_upper_division_class_recommendation.txt |
| 8 | Reddit r/UCI — "Low stress CS electives" | Student review | [Reddit thread](https://www.reddit.com/r/UCI/comments/jw4csm/low_stress_cs_electives/) | documents/low_stress_cs_electives.txt |
| 9 | Reddit r/UCI — "CS Courses Tier List" | Student review | [Reddit thread](https://www.reddit.com/r/UCI/comments/13866f3/cs_courses_tier_list/) | documents/cs_courses_tier_list.txt |
| 10 | Quora — Good courses at UCI ICS | Student review | [Quora thread](https://www.quora.com/What-are-some-good-courses-to-take-at-the-Donald-Bren-School-of-Information-and-Computer-Science-in-the-University-of-California-Irvine) | documents/good_courses_uci_ics.txt |
| 11 | RateMyProfessors — UCI CS department | Professor ratings | [RateMyProfessors](https://www.ratemyprofessors.com/search/professors/1074?q=*&did=11) | documents/rate_my_professor.txt |
| 12 | UCI General Catalogue — BS CS Degree Requirements | Official requirements | [UCI Catalogue](https://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/computerscience_bs/#requirementstext) | documents/cs_requirements.txt |
| 13 | UCI General Catalogue — BS CS Sample Program | Official sample plan | [UCI Catalogue](https://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/computerscience_bs/#sampleprogramtext) | documents/cs_sample_plan.txt |
| 14 | UCI General Catalogue — Computer Science (COMPSCI) courses | Official catalog | [UCI Catalogue](https://catalogue.uci.edu/allcourses/compsci/) | documents/courses_cs.txt |
| 15 | UCI General Catalogue — Informatics (IN4MATX) courses | Official catalog | [UCI Catalogue](https://catalogue.uci.edu/allcourses/in4matx/) | documents/courses_inf.txt |
| 16 | UCI General Catalogue — I&C SCI courses | Official catalog | [UCI Catalogue](https://catalogue.uci.edu/allcourses/i_c_sci/) | documents/courses_ics.txt |
| 17 | UCI ICS Course Offerings | Schedule | [ICS Course Listing](https://ics.uci.edu/course_listing/) | documents/course_offerings_cs.txt / course_offerings_ics.txt / course_offerings_inf.txt |
| 18 | UCI Schedule of Classes (WebSoc) — CS, ICS, INF | Schedule | [WebSoc](https://www.reg.uci.edu/perl/WebSoc) | documents/course_offerings_cs_reg.txt / course_offerings_ics_reg.txt / course_offerings_inf_reg.txt |

---

## Chunking Strategy

**Chunk size:** 800 characters

**Overlap:** 100 characters

**Why these choices fit your documents:** 

 My documents are a mix of different structures. The social media (Reddit, Quora) comments are short, unstructured text, typically just 1-2 sentences each. However, the course listings are longer (1-2 pages) and structured as tables. Using a chunk size of 800 characters will help ensure I have a balance of capturing an entire thought (not cutting off mid-sentence) while not having too much additional content that confuses the LLM. The overlap of 100 characters will help me capture any longer text portions so they don't get cut off, such as a course description describing prerequisite courses ot a student commenting on multiple courses. Also, I used a recursive chunking strategy because my content is already naturally broken up into distinct sections (comments, tables). A fixed size chunking strategy might have included extra info from additional comments or cut off part of the course listing while a semantic strategy isn't really necessary since my content is already structured such that similar topics are together.

**Final chunk count:** 524

**Sample Chunks:**

| # | Source | Sample text (first 200 chars) |
| --- | --- | --- |
| 1 | course_offerings_cs.txt | Title Fall 2026 Winter 2027 Spring 2027 CS 111 Digital Image Processing Aditi Majumder CS 112 Computer Graphics Aditi Majumder CS 116 Computational Photography & Vision Alexander Berg... |
| 2 | course_offerings_cs_reg.txt | 35005 RES 5 2-12 BIC, L. In-Person *TBA* *TBA* TBA 30 0 0 0 0 K&N OPEN 35006 RES 6 2-12 BOZORGZADEH, E. In-Person *TBA*... |
| 3 | course_offerings_inf_reg.txt | WAITLIST: Students on the waitlist for an ICS course should be in communication with that course's instructor to arrange for access to course materials and submission of any assignment... |
| 4 | courses_cs.txt | Individual research or investigation with Computer Science faculty. Repeatability: May be taken unlimited times. COMPSCI 200S. Seminar in Computer Science Research. 1 Unit. Graduate colloquium series... |
| 5 | schedule_for_cs_major_2.txt | Suggestion: Fall: ICS 51, IN4MTX 43, ICS 6D or Stats 67 Winter: ICS 45C, ICS 53 and 53L (taken together), Spring: ICS 46, ICS 6D or Stat 67 (whichever you didn't take in Fall, obviously) You might... |

### Chunking Strategy Comparison

Three chunk sizes were evaluated against the same 5-query test set using in-memory ChromaDB collections built from the same source documents. The metric is average cosine distance across the top-5 retrieved chunks per query (lower = more relevant to the query).

| Strategy | Chunk size | Overlap | Total chunks | Avg cosine distance |
| --- | --- | --- | --- | --- |
| Small | 400 | 50 | 891 | 0.4387 |
| Medium | 800 | 100 | 524 | 0.4198 |
| Large | 1200 | 150 | 367 | 0.4461 |

**Per-query breakdown:**

| Query | Small | Medium | Large |
| --- | --- | --- | --- |
| Easy upper-division project-based CS courses? | 0.3954 | 0.3812 | 0.4103 |
| Who teaches ICS 32 and what do students think? | 0.4711 | 0.4823 | 0.4900 |
| CS electives recommended for machine learning? | 0.4103 | 0.3920 | 0.4215 |
| Lower division requirements for the CS major? | 0.4502 | 0.4317 | 0.4289 |
| Which courses are high workload or difficult? | 0.4415 | 0.4298 | 0.4536 |

**Winner: Medium (800/100)** with the lowest average cosine distance (0.4198).

**Analysis:** Medium performed best on 4 of 5 queries. The one exception is "lower division requirements for the CS major," where Large (0.4289) slightly outperforms Medium (0.4317) because the official requirements document (`cs_requirements.txt`) contains multi-line structured entries (course code, units, prerequisite) that benefit from a wider context window so that related requirements appear together in one chunk. For all other queries, 800 characters is long enough to capture a complete Reddit comment or course description without truncating, and short enough to avoid merging unrelated entries into the same chunk. Large chunks (1,200 chars) consistently underperformed because at that size, a single chunk frequently spans two separate Reddit comments or multiple adjacent course catalog entries, so retrieved chunks are  broader and less precisely matched to the query. Small chunks (400 chars) occasionally fragment longer course catalog entries mid-description, reducing retrieval quality for structured documents while slightly improving it for short, opinion-based comments.

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`

**Production tradeoff reflection:** Using  `all-MiniLM-L6-v2` is fast and free, which is fine for the development phase, especially when I have a small corpus of documents that I can thoroughly review beforehand and determine best chunk size and overlap, and more easily debug if it's not performing well due to the limited number of users of this app. 

However, this model has a context length limit of 256 tokens so chunks longer than will get truncated automatically, which could cut off the end of a longer piece of text. In production, I'd probably want to use a model with a bigger context window such as `text-embedding-3-large`, which has a limit of 8,191 tokens. 

Another thing to consider is that my documents contain some domain-specific info and are written very informally. For instance, there is a lot of technical jargon that a general LLM may not have been trained on so it might not understand if a students asks what courses cover XYZ topic or it might not make the connection that certain topics are related so certain courses could be substitutes for each other. Also, students tends to write in informal language, so man of my documents contain slang, abbreviations, etc so the LLM might not understand those or interpret people's reviews of courses properly. 

It is also important to consider latency since larger models take longer to respond, which could make for a bad user experience, especially in a chat-style application. I'd want to balance picking models that perform well with ones that perform efficiently.

Finally, since all my sources are in English, multilingual support is not needed for this use case. If that was relevant however, I'd want to pick a model that has multi-lingual support.

---

## Hybrid Search

**Approach:** The system combines semantic vector search with BM25 keyword search and merges the two ranked lists using Reciprocal Rank Fusion (RRF).

- **Semantic search:** The query is encoded by `all-MiniLM-L6-v2` and the top-k chunks are retrieved from ChromaDB by cosine distance. Captures conceptual similarity even when exact words differ (e.g., "easy" retrieves chunks about "low-stress").
- **BM25 keyword search:** All 524 chunks are scored against the tokenized query using `BM25Okapi` from the `rank_bm25` library. Chunks are loaded from a flat `chunks.json` file rather than ChromaDB because BM25 must score the entire corpus at once and ChromaDB only returns top-k results. BM25 excels at exact keyword matches and domain-specific terms like course codes.
- **RRF merge:** Both ranked lists are combined with the formula `score = Σ 1 / (60 + rank + 1)`. A chunk that appears in both lists accumulates a score contribution from each ranking. `RRF_K = 60` is a standard default that dampens top-rank dominance (a chunk ranked 1 in one list but missing from the other still competes with chunks ranked average in both lists).

**Comparison on 3 queries:**

### Query A: "What are some low-stress CS electives?"

| Method | Top sources returned |
| --- | --- |
| Semantic only | low_stress_cs_electives.txt · easy_classes_computer_science.txt · review_of_every_undergrad_cs_elective.txt |
| BM25 only | low_stress_cs_electives.txt · easy_classes_computer_science.txt · cs_courses_tier_list.txt · cs_upper_division_class_recommendation.txt |
| Hybrid (RRF) | low_stress_cs_electives.txt · easy_classes_computer_science.txt · review_of_every_undergrad_cs_elective.txt · cs_courses_tier_list.txt |

**Winner: Hybrid.** Both methods agreed on the top 2 sources. Semantic added `review_of_every_undergrad_cs_elective.txt` (workload discussions phrased differently from the query). BM25 added `cs_courses_tier_list.txt` (contains "electives" and "stress" explicitly). The hybrid merged set is more diverse than either method alone.

### Query B: "Which courses are offered on Tuesday and Thursday in Fall 2026?"

| Method | Top sources returned |
| --- | --- |
| Semantic only | course_offerings_ics_reg.txt · course_offerings_cs_reg.txt · course_offerings_inf_reg.txt |
| BM25 only | schedule_for_cs_major.txt · course_offerings_cs_reg.txt · cs_requirements.txt |
| Hybrid (RRF) | course_offerings_ics_reg.txt · course_offerings_cs_reg.txt · course_offerings_inf_reg.txt · schedule_for_cs_major.txt |

**Winner: Semantic (marginal).** Semantic correctly prioritized all three schedule-of-classes files (`*_reg.txt`), which contain the actual meeting day/time data. BM25 surfaced `schedule_for_cs_major.txt` (a Reddit post about which quarters to take courses, not actual meeting times) and `cs_requirements.txt` as false positives due to the keyword "Fall" appearing in those documents. The hybrid result carries in these BM25 false positives alongside the correct sources.

### Query C: "What are the lower division requirements for the CS major?"

| Method | Top sources returned |
| --- | --- |
| Semantic only | schedule_for_cs_major_2.txt · courses_ics.txt · cs_upper_division_class_recommendation.txt · low_stress_cs_electives.txt |
| BM25 only | cs_requirements.txt · schedule_for_cs_major_2.txt · schedule_for_cs_major.txt |
| Hybrid (RRF) | cs_requirements.txt · schedule_for_cs_major_2.txt · courses_ics.txt |

**Winner: Hybrid.** This is the clearest case where BM25 adds measurable value. `cs_requirements.txt`, the official UCI degree requirements document, repeatedly uses the phrase "lower division" and is the authoritative source for this query yet semantic search missed it entirely. The formal catalog language ("Units: 4", "Prerequisite: none") embeds very differently from the conversational query phrasing, pushing the document below the cosine-distance threshold. BM25's exact keyword matching correctly ranked `cs_requirements.txt` first. The hybrid result elevated it into the final top-5 where semantic alone could not.

---

## Metadata Filtering

The UI supports filtering retrieved chunks by document source category. Users select one or more of four source categories (Student Reviews, Course Catalog, Course Offerings, Requirements & Planning). These categories are mapped to a list of source doc file names which are passed to ChromaDB as a `where` clause and to BM25 as an index-level inclusion filter.

**Example query:** "What are some courses related to machine learning?"

**Without filter:**

| Rank | Source | Category | Cosine distance |
| --- | --- | --- | --- |
| 1 | review_of_every_undergrad_cs_elective.txt | Student Review | 0.31 |
| 2 | cs_upper_division_class_recommendation.txt | Student Review | 0.33 |
| 3 | courses_cs.txt | Course Catalog | 0.36 |
| 4 | cs_course_recommendations.txt | Student Review | 0.38 |
| 5 | cs_courses_tier_list.txt | Student Review | 0.41 |

**With filter: "Course Catalog" only** (`courses_cs.txt`, `courses_inf.txt`, `courses_ics.txt`):

| Rank | Source | Category | Cosine distance |
| --- | --- | --- | --- |
| 1 | courses_cs.txt | Course Catalog | 0.36 |
| 2 | courses_cs.txt | Course Catalog | 0.39 |
| 3 | courses_ics.txt | Course Catalog | 0.44 |
| 4 | courses_inf.txt | Course Catalog | 0.47 |
| 5 | courses_cs.txt | Course Catalog | 0.50 |

**Effect:** Filtering to Course Catalog completely replaced the retrieved set. The average cosine distance increased from 0.36 to 0.43 which is expected because the most semantically similar chunks for a this query are student reviews using the same informal language ("must-take for ML", "great if you like AI"), not formal catalog descriptions ("4 Units. Introduction to machine learning algorithms. Prerequisite: ICS 46"). The filter is useful when a student wants authoritative prerequisite and unit information rather than peer opinions, with the tradeoff that retrieval precision drops slightly because the most related chunks are in the student review files.

---

## Grounded Generation

**System prompt grounding instruction:** """...
Answer questions ONLY using the information in the context documents provided below.
Do NOT use any outside knowledge, training data, or general information — even if you are confident about the answer.
If the context documents do not contain enough information to answer the question, respond with exactly:
"I don't have enough information on that based on the available documents"

Do not make assumptions or inferences beyond what is explicitly stated in the documents.
Be specific: quote or paraphrase the relevant parts of the documents in your answer.
Always include citations. When citing information, refer to the source by its filename as it appears in the document header (e.g. "According to rate_my_professor.txt..." or "A student on low_stress_cs_electives.txt noted...").
...
"""

**How source attribution is surfaced in the response:** MY system prompt includes, "Always include citations. When citing information, refer to the source by its filename as it appears in the document header (e.g. "According to rate_my_professor.txt..." or "A student on low_stress_cs_electives.txt noted...")." In the query response, the LLM references file names wthin the response as it mentions content from that file. In the UI, I also have a panel with the all the source file names used in the response. Only file names that the model actually cited in its answer are shown in the sources list so I don't display sources for chunks the model retrieved but did not use. For instance, if model retrieved 5 chunks but only referenced 2 to generate the response, only those 2 are noted as sources for the response.

**Example grounded responses with source attribution:**

### Query: "Which electives are recommended for undergrad CS majors interested in machine learning?"

> According to cs_upper_division_class_recommendation.txt, CS 178 (ML and Datamining) is "great if you want a solid foundation in machine learning" and is recommended, especially if you are interested in ML. Additionally, review_of_every_undergrad_cs_elective.txt highly recommends CS 178, stating it's a "Must take for anyone interested in AI/ML" and that it will "truly broaden your perspectives." Furthermore, cs_upper_division_class_recommendation.txt mentions CS 175 (project in AI) as a "solid AI project class" that is worth considering.
>
> **Sources:** cs_upper_division_class_recommendation.txt · review_of_every_undergrad_cs_elective.txt

The filenames appear inline in the answer text and are also listed in the sources footer.

---

### Query: "What are some upper-div project-based courses that are considered easy?"

> According to easy_classes_computer_science.txt, some upper-div project-based courses that are considered easy include 143B and 175, which are "considered project courses." Specifically, 143B with Bic is described as "Super easy" with "no lectures at all, everything is posted on day one." On the other hand, 175 with Singh was "quite a bit of work, but one of the more fun, open-ended classes."
>
> **Sources:** easy_classes_computer_science.txt

---

**Out-of-scope query example - refusal response:**

### Query: "What is the weather like in Irvine?"

> I don't have enough information on that based on the available documents.
>
> **Sources:** *(none)*

The system returns the exact refusal phrase specified in the system prompt and suppresses the sources panel entirely. No documents are cited because the model is not drawing on any retrieved content - it recognized that the query falls outside the corpus and refused to answer rather than hallucinating.

---

## Query Interface

### Input and output fields

| Field | Type | Description |
| --- | --- | --- |
| User's query | Text input | The user's natural-language query about UCI CS courses, professors, schedules, or degree requirements |
| Filters & Settings | Collapsible panel | Contains checkbox filters for document-type (Student Reviews, Course Catalog, Course Offerings, Requirements & Planning) to optionally restrict retrieval to a subset of sources; also contains toggles for whether to use Hybrid Search and show Chunking Strategy Comparison |
| Hybrid Search | Checkbox | When checked, combines BM25 keyword search with semantic vector search and merges results via Reciprocal Rank Fusion; when unchecked, uses semantic search only |
| Compare Chunking Strategies | Checkbox | When checked, runs the query against Small/Medium/Large chunk-size variants and shows retrieval distances for each |
| Chat | Chatbot Panel | Displays the full multi-turn conversation history; each LLM response ends with a sources footer showing cited filenames and the retrieval method used |
| Chunking Strategy Comparison | Collapsible panel | Populated when the comparison setting checkbox is set; shows ranked chunk strategies with average cosine distances and top sources for the current query |
| Clear | Button | Resets the conversation history and all output fields to start a fresh chat session |

### Sample interaction transcript - single query/response

---

**User:** What are some upper-div project-based courses that are considered easy?

**ChatZOT:** According to easy_classes_computer_science.txt, some upper-div project-based courses that are considered easy include 143B and 175, which are "considered project courses." Specifically, 143B with Bic is described as "Super easy" with "no lectures at all, everything is posted on day one." On the other hand, 175 with Singh was "quite a bit of work, but one of the more fun, open-ended classes."

---
**Sources:** easy_classes_computer_science.txt
*hybrid (semantic + BM25, RRF merge)*

### Sample interaction transcript - multi-turn conversation

---

**User:** What are some low-stress CS electives?

**ChatZOT:** According to low_stress_cs_electives.txt, some low-stress CS electives include CS 121, CS 163, CS 145, CS 122, and CS 132 with Levorato, as well as CS 162, CS 164, and CS 165 with Goodrich. Additionally, a student on low_stress_cs_electives.txt noted that CS 145 is "pretty low stress" and another student mentioned that CS 122A is "not bad" and "not a lot of complex coding." Furthermore, easy_classes_computer_science.txt suggests that CS 121 is a "pretty easy and relatively low-stress upper div."

---
**Sources:** low_stress_cs_electives.txt · easy_classes_computer_science.txt
*hybrid (semantic + BM25, RRF merge)*

---

**User:** Which of those has the least amount of homework?

**ChatZOT:** According to the previous conversation, CS 145 was mentioned as one of the low-stress CS electives. A student on easy_classes_computer_science.txt noted that 145 with Givargis is "one of the easiest A+ I've gotten." This suggests that CS 145 may have a relatively manageable workload. However, there is no explicit information about the amount of homework for the other mentioned courses, such as CS 121, CS 163, CS 122, CS 132, CS 162, CS 164, and CS 165.

---
**Sources:** easy_classes_computer_science.txt
*hybrid (semantic + BM25, RRF merge)*

---

The follow-up question "which of those has the least amount of homework?" uses a pronoun ("those") referring to the courses listed in the prior response. The system uses the prior assistant message to filter retrieved chunks to only those mentioning the previously cited courses, then explicitly passes the conversation history to the LLM so it can reason across both turns.

---

## Retrieval Test Results

### Query 1: "What are some low-stress CS electives?"

| Rank | Source | Cosine distance | Chunk preview |
| --- | --- | --- | --- |
| 1 | low_stress_cs_electives.txt | 0.42 | "Hello. I'm almost done with my core CS classes, and I have to say, I'm feeling pretty burnt out... I'm looking for some fun or low stress CS electives to take for future quarters." |
| 2 | easy_classes_computer_science.txt | 0.45 | "I am in a hard probation right now... I have basically only 6 more classes to take and I really need to pass all of them. Does anyone know any easy CS classes?" |
| 3 | review_of_every_undergrad_cs_elective.txt | 0.46 | "CS 179 - Algorithms for Probabilistic and Deterministic Graphical Models. Ihler. Must take for anyone interested in AI/ML. This course effectively takes the Bayesian networks..." |
| 4 | low_stress_cs_electives.txt | 0.48 | "Following! Personally I'm planning on specializing in systems and software... I got recommended CS 125, CS 116, CS 117 as low-stress options." |
| 5 | review_of_every_undergrad_cs_elective.txt | 0.49 | "CS 122A - Introduction to Data Management. Nawab. If you intend to take CS 122B or CS 122C, sure. Otherwise, maybe not worth your time." |

*Why these chunks are relevant:* Chunks 1 and 4 are both from low_stress_cs_electives.txt, which is a Reddit thread specifically asking for low-stress elective recommendations - a near-exact match for the query. Chunk 2 (easy_classes_computer_science.txt) is also directly on-topic: a student explicitly asking for easy CS classes. Chunks 3 and 5 from review_of_every_undergrad_cs_elective.txt are slightly less targeted but still relevant — they provide workload context for specific electives that a student comparing stress levels would find useful. All 5 chunks come from student review sources, which is the correct document category for this query.

---

### Query 2: "What are the lower division requirements for the CS major?"

| Rank | Source | Cosine distance | Chunk preview |
| --- | --- | --- | --- |
| 1 | schedule_for_cs_major_2.txt | 0.39 | "Hello, I have to complete the following eight lower divs for a CS major: ICS 51, ICS 45c, ICS 6D, ICS 46, ICS 53, ICS 53L, Stats 67, IN4MTX 43..." |
| 2 | courses_ics.txt | 0.40 | "I&C SCI 168. Multiplayer Game Project. 4 Units. Design and develop a multiplayer game using Unity or similar engine..." |
| 3 | cs_upper_division_class_recommendation.txt | 0.43 | "Hi, I'm planning to choose my CS specialization to be general so that I can take all kinds of upper CS classes. Does anyone have any recommendation..." |
| 4 | courses_ics.txt | 0.40 | "I&C SCI 169B. Capstone Game Project II. 4 Units. Students continue work in teams to design and implement a unique game or interactive experience..." |
| 5 | low_stress_cs_electives.txt | 0.44 | "A majority of the INF classes are chill, more focused on group work, practical work, and writing..." |

*Why these chunks are relevant:* Chunk 1 is a Reddit post that explicitly lists all eight lower-division CS requirements by course code. However, chunks 2 and 4 (game project course descriptions from courses_ics.txt) are off-target - they appear because the ICS catalogue file has a low cosine distance to any ICS-related query, not because they discuss lower division requirements. One thing to note is cs_requirements.txt, the official UCI degree requirements document, did not appear in the top 5 at all. The formal language of the catalogue ("prerequisite: none", "units: 4") embeds differently from the informal phrasing of the query, pushing the authoritative source below the retrieval threshold. This is an example of the semantic mismatch challenge described in the Anticipated Challenges section.

---

### Query 3: "Which courses are offered on Tuesday and Thursday in Fall 2026?"

| Rank | Source | Cosine distance | Chunk preview |
| --- | --- | --- | --- |
| 1 | schedule_for_cs_major.txt | BM25 only | "I'd go for the schedule on top or 46/51/INF43 next fall to make your Winter 2023 really chill..." |
| 2 | course_offerings_ics_reg.txt | 0.45 | "UC Irvine Office of the Registrar. Schedule of Classes. Fall Quarter, 2026. Registration for term ends on Tuesday..." |
| 3 | course_offerings_cs_reg.txt | 0.47 | "UC Irvine Office of the Registrar. Schedule of Classes. Fall Quarter, 2026. Search Criteria: Department: IN4MATX..." |
| 4 | cs_requirements.txt | BM25 only | "and Single-Variable Calculus II I&C SCI 6B Boolean Logic and Discrete Structures I&C SCI 6D Discrete Mathematics..." |
| 5 | course_offerings_inf_reg.txt | 0.47 | "UC Irvine Office of the Registrar. Schedule of Classes. Fall Quarter, 2026. Search Criteria: Department: IN4MATX..." |

*Why these chunks are relevant:* Chunks 2, 3, and 5 are the schedule-of-classes documents for COMPSCI, I&C SCI, and IN4MATX departments, which are the best sources for this query and were correctly identified as the top results. Chunk 1 (a Reddit scheduling advice post) is partially off-target since it mentions scheduling by quarter but does not contain actual meeting times. Chunk 4 (cs_requirements.txt) is irrelevant noise, likely retrieved because it references the same course codes that appear in the schedule docs, producing a misleadingly high semantic similarity.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which electives are recommended for undergrad CS majors interested in machine learning? | CS 178, IN4MATX 119, IN4MATX 141, CS 111, CS 117, CS 172B | Recommended CS 178 (must-take for AI/ML), CS 175 (AI project class), CS 190 (medical DL), and CS 177 (probability). Cited cs_upper_division_class_recommendation.txt and review_of_every_undergrad_cs_elective.txt. | Partially relevant | Partially accurate |
| 2 | What is the best order to take the math course requirements (ICS 6B, ICS 6D) and what is a sample schedule based on course offerings? | MATH 2A → MATH 2B → ICS 6B → ICS 6D sequence; specific Fall 2026 section times for ICS 6B and 6D | Correctly identified that ICS 6B should precede ICS 6D. Did not retrieve MATH 2A/2B prerequisite chain or specific Fall 2026 section times. Response was vague and partial. | Partially relevant | Partially accurate |
| 3 | What are some upper-div project-based courses that are considered easy? | CS 145 (easiest class), CS 165 with Goodrich (chill), INF 131 (easy A+) | Identified CS 143B (super easy, two projects, no lectures) and CS 175 with Singh (fun open-ended Minecraft AI). Valid and grounded, but different courses than expected. | Relevant | Partially accurate |
| 4 | Who is the best professor for ICS 32? I want someone who does engaging lectures and does not grade hard. | Alex Thornton (ICS H32, quality 4.2/5) vs Thomas Yeh (regular ICS 32, quality 2.3/5); Thornton is the better-rated option | Refusal: "I don't have enough information on that based on the available documents." rate_my_professor.txt was not retrieved. | Off-target | Inaccurate |
| 5 | I am deciding between COMPSCI 125, COMPSCI 163, and COMPSCI 179. I want to take one in Fall 2026. What class works with my schedule? | None of the three are offered in Fall 2026; system should not hallucinate schedule info | Refusal: "I don't have enough information on that based on the available documents." Did not hallucinate any schedule data. | Partially relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:** "Who is the best professor for ICS 32? I want someone who does engaging lectures and does not grade hard."

**What the system returned:** "I don't have enough information on that based on the available documents."

**Root cause (tied to a specific pipeline stage):**  This is a retrieval failure caused by a cross-document reasoning gap. Answering this question requires linking two facts that live in separate documents: (1) which professor teaches ICS 32, which is in the schedule-of-classes files, and (2) what that professor's rating is, which is in rate_my_professor.txt. The embedding for "best professor for ICS 32 engaging lectures" semantically matches course recommendation posts (which talk about professors and courses together) more than it matches rate_my_professor.txt (which lists professors with numeric ratings but no course-specific language). As a result, the top-5 retrieved chunks came from good_cs_upper_div_project_courses.txt, course_offerings_cs_reg.txt, schedule_for_cs_major.txt, and easy_classes_computer_science.txt — none of which contained the correct professor's rating data. While the LLM did not find the correct answer, it did however correctly refuse to answer rather than hallucinating.

**What you would change to fix it:** To fix this issue, one thing I could do is increase top-k from 5 to 10 for instance to increase the chance that both the schedule chunk (professor to course mapping) and the RateMyProfessor chunk (professor to rating mapping) are both retrieved. Another way could be restructuring the rate_my_professor.txt file during preprocessing to explicitly annotate professors with the course codes they are known to teach. It would also be helpful to have a graph database with all this relational info and metadata so I could query that as part of the RAG pipeline instead of just relying on similarity scores for text embeddings in a vector store.

---

## Spec Reflection

**One way the spec helped you during implementation:** Creating the spec helped me learn more about my data beforehand so I could identify the best way to approach different parts of the pipeline and consider potential tradeoffs and challenges during development instead of building the whole pipeline and then realizing something wasn't going to work well. It also gave me an opportunity to include my own perspective of the domain and define my goal for the project so when I gave it to the AI for implementation, it built something that aligned with my expectations instead or going off on it's own and making key decisions itself.

**One way your implementation diverged from the spec, and why:** As I built out the pipeline and tested queries at each step, I realized some of my queries weren't actually answerable just from my chosen source docs (many of the responses were "I don't have enough info to answer that") so I had to adjust my queries to find ones that more effectively helped me gauge the performance of my pipeline. Since I used a limited set of source docs, it just wasn't realistic for them to contain info on all the courses and professors at UCI. I also hadn't accounted for the fact that some course requirements for CS are actually from other departments like MATH and STATS so I hadn't included source docs with those courses and schedules. This made me realize how important it is to have a large, diverse set of source docs that contain all the info you need since the LLM isn't going to be able to fill in the gaps otherwise, epecially when I gave it good grounding guidance so it wouldn't reference any other knowledge it had outside those source docs.

---

## AI Usage

### Instance 1: Generating the RAG pipeline code using Claude

- *What I gave the AI:* The Chunking Strategy section (chunk_size=800, overlap=100, RecursiveCharacterTextSplitter with separator list), the Retrieval Approach section (all-MiniLM-L6-v2, ChromaDB with cosine distance, top-k=5), and the Architecture diagram from planning.md. I also described the Groq API and the Gradio interface requirement.
- *What it produced:* A Python file for each pipeline step: ingest.py (chunking source docs), embed.py (embedding source docs), query.py (querying LLM) + app.py (UI). Having a separate file for each step made it easy for me to test the code after each milestone and helped me understand the process end-to-end better. I also knew where to look when I was reviewing code or needed to debug.
- *What I changed or overrode:* The initial citations displayed in the UI showed all 5 retrieved chunk sources regardless of whether they were actually used to generate the final response. I thought this would be confusing to the user (and a little misleading) so I asked Claude to change it to only show a source if it was referenced in the LLM's response. Also, originally in the LLM response, it referenced sources as "Document 1", "Document 2", etc but in the Sources panel on the UI it displayed file names (ex: courses_cs.txt) so a user wouldn't be able to identify which source was which so I asked Claude to change it so that both the source citations in the LLM response and the Sources panel in the UI showed the file names.

### Instance 2: Debugging conversational memory issue

- *What I gave the AI:* The existing query.py and app.py files, a description of the conversational memory stretch feature, and an example set of queries I used that demonstrated that the memory feature wasn't working. 
- *What it produced:* The issue I had encountered was that when I used a pronoun in the next query that was meant to reference something from the previous chat messages, the LLM didn't understand that connection and just answered like it was a brand new, standalone query. To fix this, Claude added functionality to intercept subsequent queries in a chat and replace the pronouns with the subjects from the previous message. For instance, if I asked what courses are good for students interested in machine learning and then asked which of those is easiest, at first it just gave me a list of easy courses regardless of if they were machine learning-related, but after the fix it did only reference machine learning courses in the second response.
- *What I changed or overrode:* At first the query rewriting approach caused the LLM to refuse to answer because the rewritten query ("which of CS 178, CS 171 has the least workload?") was too specific and failed to retrieve relevant chunks. I replaced it with a chunk filtering approach: retrieve using the original question which was broader, and then filter retrieved chunks to only those mentioning course codes extracted from the prior answer, with a fallback to all chunks if no match is found. 
