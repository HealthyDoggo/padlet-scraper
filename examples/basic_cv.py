from google import genai
from padlet_scraper import scrape_padlet, Padlet
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

padlet_url = os.getenv("PADLET_LINK")
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

PROMPT = """
You are a skilled personal-statement writer.

You will be given a markdown export of a Padlet containing a person’s experiences, reflections, achievements, challenges, and interests.

This person is applying to {application_name}.

Your task is to:

Synthesize this information into a cohesive personal statement

Write in the first person

Maintain an authentic, reflective, and confident tone

Focus on growth, motivation, values, and impact, not just listing experiences

Learnings and insights from experiences are more important than the experiences themselves.

Smoothly connect ideas even if the source notes are fragmented or repetitive

Guidelines:

Do not copy the Padlet text verbatim; rewrite and synthesize

Prioritize clarity, narrative flow, and personal insight

Highlight key themes that emerge across multiple experiences

If dates or specifics are missing, infer connections but do not invent facts

Aim for a length of [250-300 words]

Attempt to balance roughly 80-90% on subject-related experience and 10-20% on other experiences that can still be related to relevant skills and motivations.

Output:

A single, polished personal statement suitable for applications (education, programs, or opportunities)

No bullet points, headings, or markdown — plain prose only
"""

async def produce_cv(padlet_link: str, application_name: str):
    padlet: Padlet = await scrape_padlet(padlet_link)
    markdown = padlet.to_markdown()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=PROMPT.format(application_name=application_name) + "\n\n" + "Input:\n" + markdown
    )
    return response.text

if __name__ == "__main__":
    print(asyncio.run(produce_cv(padlet_url, "Cambridge University Computer Science BSc")))