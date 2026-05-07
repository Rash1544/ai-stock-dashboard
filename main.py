import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

print("🚀 Autonomous AI Data Analyst Agent Started")

# Load dataset
df = pd.read_csv("sales.csv")

# Show dataset preview
print("\nDataset Preview:")
print(df.head())

# Smaller dataset summary
summary = str(df.head())

# Prompt
prompt = f"""
You are an expert AI Data Analyst.

Analyze this dataset and provide:
1. Key insights
2. Trends
3. Business recommendations

Dataset:
{summary}
"""

# Generate AI response
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

# Print AI insights
print("\n🧠 AI GENERATED INSIGHTS:\n")
print(response.choices[0].message.content)