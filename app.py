import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities import WikipediaAPIWrapper

st.set_page_config(
    page_title="Text To Math Problem Solver And Data Search Assistant",
    page_icon="🧮"
)

st.title("Text To Math Problem Solver")

groq_api_key = st.sidebar.text_input(
    "Groq API Key",
    type="password"
)

if not groq_api_key:
    st.info("Please add your Groq API Key to continue.")
    st.stop()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=groq_api_key,
    temperature=0
)

wiki = WikipediaAPIWrapper()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi! I can solve mathematics, logical reasoning, and general knowledge questions."
        }
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

question = st.text_area(
    "Enter your question:",
    "I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries. Each pack contains 25 berries. How many total pieces of fruit do I have?"
)

if st.button("Find My Answer"):

    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    st.chat_message("user").write(question)

    with st.spinner("Generating response..."):

        try:

            wiki_result = ""

            try:
                wiki_result = wiki.run(question)
            except:
                wiki_result = ""

            prompt = f"""
You are an expert AI assistant.

Solve mathematical problems step by step.

For logical questions, explain your reasoning clearly.

If Wikipedia information is relevant, use it.

Wikipedia Information:
{wiki_result}

User Question:
{question}

Provide:

1. Step-by-step reasoning
2. Final answer
"""

            response = llm.invoke(prompt)

            answer = response.content

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

            st.chat_message("assistant").write(answer)

        except Exception as e:
            st.error(str(e))
