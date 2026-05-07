import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

print("🚀 Multi-Agent AI System Started")

# Load dataset
df = pd.read_csv("sales.csv")

# =========================
# AGENT 1 — DATA CLEANING
# =========================

print("\n🧹 Data Cleaning Agent Running...")

df = df.dropna()

print("✅ Missing values removed")

# =========================
# AGENT 2 — ANALYSIS AGENT
# =========================

print("\n📊 Analysis Agent Running...")

summary = str(df.describe())

analysis_prompt = f"""
You are a Data Analysis Agent.

Analyze this dataset statistics:

{summary}

Provide:
1. Key insights
2. Trends
3. Important observations
"""

analysis_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": analysis_prompt}
    ]
)

analysis_text = analysis_response.choices[0].message.content

print("\n🧠 ANALYSIS INSIGHTS:\n")
print(analysis_text)

# =========================
# AGENT 3 — VISUALIZATION AGENT
# =========================

print("\n📈 Visualization Agent Running...")

plt.plot(df["Sales"])
plt.title("Sales Trend")
plt.xlabel("Days")
plt.ylabel("Sales")

plt.savefig("sales_chart.png")

print("✅ Chart saved as sales_chart.png")

# =========================
# AGENT 4 — REPORT AGENT
# =========================

print("\n📝 Report Agent Running...")

report_prompt = f"""
You are a Business Report Agent.

Using these insights:

{analysis_text}

Generate a professional business report.
"""

report_response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": report_prompt}
    ]
)

final_report = report_response.choices[0].message.content

print("\n📄 FINAL BUSINESS REPORT:\n")
print(final_report)