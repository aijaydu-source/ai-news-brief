import feedparser
import os
from datetime import date
from openai import OpenAI

# Config
RSS_FEEDS = ["https://hnrss.org/frontpage", "https://www.reddit.com/r/artificial/.rss"]
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def fetch_entries():
    items = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            items.append(entry.get('title', ''))
    return items[:10]

def generate_brief(titles):
    prompt = "Today's headline: " + "; ".join(titles) + "\nWrite a concise 3-sentence daily digest."
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return resp.choices[0].message.content

def main():
    titles = fetch_entries()
    if not titles:
        print("No RSS entries found.")
        return
    brief = generate_brief(titles)
    with open(f"digest_{date.today()}.md", "w") as f:
        f.write(f"# Daily AI/Dev Digest - {date.today()}\n\n")
        f.write(brief + "\n\n## Sources\n" + "\n".join(f"- {t}" for t in titles))
    print("Saved", f"digest_{date.today()}.md")

if __name__ == "__main__":
    main()
