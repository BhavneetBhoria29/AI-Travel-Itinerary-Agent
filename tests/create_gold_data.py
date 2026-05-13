import json
import os
import re
import sys
import time
from datetime import datetime
from dotenv import load_dotenv

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from langchain.chat_models import init_chat_model
from src.utils.tavily_helper import get_tavily_context
from tests.eval_dataset import EVAL_DATASET

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLD_FILE = os.path.join(PROJECT_ROOT, "evals", "gold_standard.json")

def create_gold_standard():
    """
    Stage 0: Use real-time web search and a high-reasoning model
    to create the 'Correct Answer' key for our evaluation.
    """
    print("🌟 Initializing Gold Standard Creation...")

    gold_llm = init_chat_model(
        model="anthropic:claude-sonnet-4-6",
        temperature=0.1
    )
    
    gold_standard = {}

    for i, case in enumerate(EVAL_DATASET):
        city = case["inputs"]["city"]
        interests = ", ".join(case["inputs"]["interests"])
        month = case["inputs"]["month"]
        
        print(f"\n🔍 [{i+1}/{len(EVAL_DATASET)}] Researching {city} for {month}...")
        
        # 1. Real-time Web Search using helper
        search_query = f"top attractions, events, and food recommendations for {city} in {month} for interests: {interests}"
        raw_search_results = get_tavily_context(search_query)
        
        # 2. Distill into Gold Standard with enhanced prompt
        prompt = f"""
        You are a world-class travel expert. I have search results about {city} for the month of {month}.
        Interests: {interests}
        
        Search Results:
        {str(raw_search_results)}
        
        Based on these ACTUAL search results, create a 'Gold Standard' reference for this trip.
        Identify:
        1. GROUND TRUTH: A concise summary (200 words) of the 5 absolute must-include attractions/events.
        2. ESSENTIAL SEARCH TOPICS: 3 core topics that MUST be searched to plan this trip (e.g. 'Versailles ticket availability').
        3. IDEAL SEARCH QUERIES: 3 specific, high-intent queries a professional agent would use.
        
        FORMAT YOUR RESPONSE AS VALID JSON ONLY:
        {{
            "ground_truth": "...",
            "essential_topics": ["topic1", "topic2", "topic3"],
            "expected_queries": ["query1", "query2", "query3"]
        }}
        """
        
        try:
            response = gold_llm.invoke(prompt)

            # response.content can be a list of blocks (Claude) or a plain string
            raw = response.content
            if isinstance(raw, list):
                clean_content = "".join(
                    b["text"] for b in raw
                    if isinstance(b, dict) and b.get("type") == "text"
                )
            else:
                clean_content = raw

            # Strip markdown code fences Claude may wrap around JSON
            clean_content = re.sub(r"```(?:json)?\s*|\s*```", "", clean_content).strip()

            start_index = clean_content.find('{')
            end_index = clean_content.rfind('}')
            if start_index == -1 or end_index == -1:
                raise ValueError(f"No JSON found in response: {clean_content[:200]}")
            clean_content = clean_content[start_index:end_index + 1]

            distilled_data = json.loads(clean_content)
            
            gold_standard[city] = {
                "input": case["inputs"],
                "ground_truth": distilled_data.get("ground_truth", "N/A"),
                "essential_topics": distilled_data.get("essential_topics", []),
                "expected_queries": distilled_data.get("expected_queries", []),
                "raw_context": str(raw_search_results)[:1500] 
            }
            print(f"✨ Gold Data generated for {city}.")
            
            time.sleep(2)  # brief pause between API calls
            
        except Exception as e:
            print(f"❌ Error distilling data for {city}: {str(e)}")
            continue

    # Save to JSON
    os.makedirs(os.path.dirname(GOLD_FILE), exist_ok=True)
    with open(GOLD_FILE, "w", encoding="utf-8") as f:
        json.dump(gold_standard, f, indent=2)

    print(f"\n🏆 Gold Standard successfully saved to {GOLD_FILE}")

if __name__ == "__main__":
    create_gold_standard()