import requests
from urllib.parse import quote

from google.adk import Agent
from google.adk.tools import exit_loop
from google.adk.agents import SequentialAgent, ParallelAgent, LoopAgent


# -----------------------------
# Wikipedia tool
# -----------------------------
def wikipedia_search(query: str) -> str:
    title = quote(query)
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"

    headers = {"User-Agent": "historical-court/1.0"}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            return "No page found."
        data = r.json()
        return data.get("extract", "")
    except Exception as e:
        return str(e)


# -----------------------------
# Save verdict tool
# -----------------------------
def save_verdict(text: str) -> str:
    with open("verdict.txt", "w", encoding="utf-8") as f:
        f.write(text)
    return "saved"


# -----------------------------
# Step 1 : Inquiry
# -----------------------------
inquiry = Agent(
    name="inquiry",
    instruction="""
Ask the user for a historical person or event.
Store it into session state with key: topic.
""",
)


# -----------------------------
# Step 2A : Admirer
# -----------------------------
admirer = Agent(
    name="admirer",
    instruction="""
You are the admirer.

Search Wikipedia.
Focus ONLY on achievements, positive impact, and contributions.

Always extend the query with words like:
achievements, reforms, success, contribution.

Topic:
{ topic? }

Store results into state key: pos_data.
""",
    tools=[wikipedia_search],
)


# -----------------------------
# Step 2B : Critic
# -----------------------------
critic = Agent(
    name="critic",
    instruction="""
You are the critic.

Search Wikipedia.
Focus ONLY on criticism, failures, controversies and negative impact.

Always extend the query with words like:
controversy, criticism, failure, abuse.

Topic:
{ topic? }

Store results into state key: neg_data.
""",
    tools=[wikipedia_search],
)


# -----------------------------
# Parallel investigation
# -----------------------------
investigation = ParallelAgent(
    name="investigation",
    sub_agents=[
        admirer,
        critic,
    ],
)


# -----------------------------
# Judge (inside loop)
# -----------------------------
judge = Agent(
    name="judge",
    instruction="""
You are the judge.

Positive data:
{ pos_data? }

Negative data:
{ neg_data? }

After one review, call exit_loop.
""",
    tools=[exit_loop],
)


# -----------------------------
# Step 3 : Loop
# -----------------------------
trial_loop = LoopAgent(
    name="trial_and_review",
    sub_agents=[
        investigation,
        judge,
    ],
)


# -----------------------------
# Step 4 : Verdict
# -----------------------------
verdict_writer = Agent(
    name="verdict_writer",
    instruction="""
Create a neutral and balanced report in English.

Topic:
{ topic? }

Positive information:
{ pos_data? }

Negative information:
{ neg_data? }

After writing the full report,
call save_verdict with the entire report text.

Clearly separate positive and negative sections.
""",
    tools=[save_verdict],
)


# -----------------------------
# Root app
# -----------------------------
root_agent = SequentialAgent(
    name="historical_court_app",
    sub_agents=[
        inquiry,
        trial_loop,
        verdict_writer,
    ],
)
