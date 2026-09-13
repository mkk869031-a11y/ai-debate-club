import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# load env variables
load_dotenv()

# get api key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is not set in the environment variables.")
    st.stop()

# create a Groq client
client = Groq(api_key=api_key)

# PAGE CONFIG
st.set_page_config(
    page_title="AI Debate Club",
    page_icon="🤖",
    layout="centered"
)

MODEL = "openai/gpt-oss-120b"


def ask_ai(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content


# PRO DEBATOR =================

def generate_pro_argument(topic):
    prompt = f"""
    You are the PRO debater in a debate.

    Debate Topic:
    {topic}

    Your job is to strongly support the topic.

    Give:
    1. Opening statement
    2. Three strong arguments with examples
    3. One real world example to support your argument
    4. A strong conclusion statement

    Rules:  
    - Acts as a boy
    - be entertaining and exciting
    - be  realistic 
    - Be logical and convincing
    - Use simple language
    - Do not repeat yourself
    - Do not mention that you are an AI model
    - Do not use unnecessary words or phrases
    """

    return ask_ai(prompt)


# CON DEBATOR =================

def generate_con_argument(topic):
    prompt = f"""
    You are the CON debater in a debate.

    Debate Topic:
    {topic}

    Your job is to strongly oppose the topic.

    Give:
    1. Opening statement
    2. Three strong arguments with examples
    3. One real world example to support your argument
    4. A strong conclusion statement

    Rules:
    - Acts as a girl
    - Be logical and convincing
    - be entertaining and exciting
    - be  realistic 
    - Use simple language
    - Do not repeat yourself
    - Do not mention that you are an AI model
    - Do not use unnecessary words or phrases
    """

    return ask_ai(prompt)


# HOST =================

def generate_host_summary(topic, pro_argument, con_argument):

    prompt = f"""
    You are the HOST of a live face-to-face debate.

    Debate Topic:
    {topic}

    PRO DEBATER:
    {pro_argument}

    CON DEBATER:
    {con_argument}

    Your job is NOT to simply summarize the arguments.

    Your job is to conduct a realistic face-to-face debate
    between the PRO and CON debaters.

    The debate should feel like two people are sitting
    opposite each other on a stage and directly responding
    to each other's arguments.

    Create the debate in this order:

    🎙️ HOST:
    Welcome the audience and introduce the debate topic.

    🟢 PRO:
    Give the opening statement and first argument.

    🔴 CON:
    Directly respond to the PRO's argument and present
    the opposing viewpoint.

    🟢 PRO:
    defend the PRO's position and counter the CON's argument.

    🔴 CON:
    Counter the PRO's rebuttal with strong reasoning.

    🎙️ HOST:
    Ask a challenging question related to the debate topic and from the above arguments.

    🟢 PRO:
    Answer the host's question and challenge the CON's position.

    🔴 CON:
    Answer the host's question and directly challenge
    the PRO's answer.

    🟢 PRO:
    Give a final rebuttal.

    🔴 CON:
    Give a final rebuttal.

    🎙️ HOST:
    Summarize the entire debate.

    Then compare both sides based on:
    - Logic
    - Strong arguments
    - Examples
    - Ability to answer questions

    Finally announce:

    🏆 WINNER: PRO or CON

    Explain clearly why that side won.

    Rules:
    - Make it feel like a real face-to-face conversation.
    - PRO and CON must directly respond to each other.
    - Do not simply copy the original arguments.
    - Keep the tone professional but entertaining.
    - Use simple language.
    - Do not mention that you are an AI.
    - Do not use unnecessary words.
    - HOST must remain neutral.
    - The winner must be decided based on argument quality,
      logic, evidence and example .
    """

    return ask_ai(prompt)


# UI

# ================= UI =================

st.title("🤖 AI Debate Club")

st.write(
    "Enter a topic and watch two debaters argue "
)

topic = st.text_input(
    "Debate Topic",
    placeholder="e.g. Should AI replace human jobs?"
)

if st.button("🚀 Start Debate"):

    if not topic:
        st.warning("Please enter a debate topic.")
        st.stop()

    # Pro Agent
    with st.spinner("🟢 Pro Agent is preparing arguments..."):
        pro_argument = generate_pro_argument(topic)

    # Con Agent
    with st.spinner("🔴 Con Agent is preparing arguments..."):
        con_argument = generate_con_argument(topic)

    # Host Agent
    with st.spinner("🎙️ Host is conducting the live debate..."):
        final_debate = generate_host_summary(
            topic,
            pro_argument,
            con_argument
        )

    # Display live debate
    st.subheader("🎙️ Live Face-to-Face Debate")
    st.write(final_debate)