import pandas as pd
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def readJobData(csv_path: str) -> pd.DataFrame:
    """Read CSV containing job postings."""
    return pd.read_csv(csv_path)

def scrapeJobDescription(url: str) -> str:
    """Scrape job description text from given URL."""
    try:
        response = requests.get(url, timeout=180)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        return text[:8000]  # limit to avoid token overflow
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return ""

def generateDomainInsight(job_text: str) -> str:
    """Generate domain insight from job description using GPT."""
    try:
        prompt = f"""
        Analyze the following job description and summarize in one short sentence what professional domain or industry this job belongs to:\n\n{job_text}.
        Specifically what aspect of domain is that in, like if healthcare, then in what claims? or non-claims. I want precise insights per
        domain analyzed
        
        Write all these points in 250 characters or less.
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"GPT error: {e}")
        return "Insight unavailable"

def addDomainInsights(df: pd.DataFrame) -> pd.DataFrame:
    """Loop through DataFrame, scrape job descriptions, and add domain insights."""
    insights = []
    for _, row in df.iterrows():
        job_text = scrapeJobDescription(row['url'])
        insight = generateDomainInsight(job_text)
        insights.append(insight)
    df["domain_insight"] = insights
    return df
