import requests
import json
import datetime
from dotenv import load_dotenv
import os
import openai

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)


# Fetch recent CVEs from NVD (from yesterday to today)
def fetch_recent_cves():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    pub_start = yesterday.strftime('%Y-%m-%dT00:00:00.000Z')
    pub_end = today.strftime('%Y-%m-%dT23:59:59.999Z')

    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?pubStartDate={pub_start}&pubEndDate={pub_end}"
    headers = {"User-Agent": "OutbreakWatchBot/1.0"}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch CVEs: {response.status_code}")
        return []

    return response.json().get("vulnerabilities", [])


# Use OpenAI to summarize a CVE description
def summarize(text):
    prompt = (
        "Summarize this CVE for a non-expert. "
        "Include what the threat is, who it affects, and what action should be taken:\n\n"
        f"{text}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error summarizing CVE: {e}")
        return "Summary not available."


# Main logic
def main():
    cves = fetch_recent_cves()
    summaries = []

    if not os.path.exists("summaries"):
        os.makedirs("summaries")

    for item in cves[:5]:  # Limit to first 5 for now
        cve_id = item["cve"]["id"]
        description = item["cve"]["descriptions"][0]["value"]
        summary = summarize(description)

        summaries.append({
            "cve_id": cve_id,
            "description": description,
            "summary": summary
        })

    with open("summaries/today.json", "w") as f:
        json.dump(summaries, f, indent=2)

    print("✅ Summaries saved to summaries/today.json")


if __name__ == "__main__":
    main()
