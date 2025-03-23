import json
import datetime
import os


def load_summaries():
    try:
        with open("summaries/today.json", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading summaries: {e}")
        return []


def generate_html(summaries):
    date_str = datetime.date.today().strftime("%B %d, %Y")
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Outbreak Watch – {date_str}</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                padding: 30px;
                background-color: #121212;
                color: #e0e0e0;
            }}
            h1 {{
                color: #66ccff;
            }}
            .cve {{
                border: 1px solid #333;
                background: #1e1e1e;
                padding: 20px;
                margin-bottom: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            }}
            .cve h2 {{
                color: #ff6b6b;
                margin-top: 0;
            }}
            .desc, .summary {{
                margin-top: 12px;
                line-height: 1.5;
            }}
            .summary {{
                font-weight: bold;
                color: #ffffff;
            }}
            a {{
                color: #66ccff;
            }}
        </style>
    </head>
    <body>
        <h1>🛡️ Outbreak Watch – Threat Summary for {date_str}</h1>
        <p>Here's your daily dose of cyber doom, simplified. Stay patched. Stay alert. 😎</p>
    """

    for item in summaries:
        html += f"""
        <div class="cve">
            <h2>{item['cve_id']}</h2>
            <div class="desc"><strong>Description:</strong><br>{item['description']}</div>
            <div class="summary"><strong>Summary:</strong><br>{item['summary']}</div>
        </div>
        """

    html += """
    </body>
    </html>
    """
    return html


def save_html(html):
    if not os.path.exists("reports"):
        os.makedirs("reports")

    filename = f"reports/report_{datetime.date.today()}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Report saved to {filename}")


def main():
    summaries = load_summaries()
    if not summaries:
        print("No summaries found.")
        return
    html = generate_html(summaries)
    save_html(html)


if __name__ == "__main__":
    main()
