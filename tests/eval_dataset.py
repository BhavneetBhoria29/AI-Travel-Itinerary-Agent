# Evaluation Dataset for AI Travel Planner
# This contains test cases to verify 
# agent reliability across different geographies and interests

EVAL_DATASET = [
    {
        "name": "Paris Art & Food",
        "inputs": {
            "city": "Paris",
            "days": 3,
            "interests": ["Impressionist Art", "Michelin Star Dining", "Seine River Cruises"],
            "style": "Luxury",
            "pace": "Relaxed",
            "month": "June"
        },
        "expected_tool_usage": ["tavily_search_tool"],
    },
    {
        "name": "Tokyo Tech & Street Food",
        "inputs": {
            "city": "Tokyo",
            "days": 5,
            "interests": ["Robotics & AI Hubs", "Tsukiji Outer Market", "Anime Culture"],
            "style": "Mid-range",
            "pace": "Packed",
            "month": "October"
        },
        "expected_tool_usage": ["tavily_search_tool"],
    },
    {
        "name": "Mumbai History & Nightlife",
        "inputs": {
            "city": "Mumbai",
            "days": 3,
            "interests": ["UNESCO Heritage Sites", "Marine Drive Seafront", "Bollywood Tours"],
            "style": "Mid-range",
            "pace": "Balanced",
            "month": "January"
        },
        "expected_tool_usage": ["tavily_search_tool"],
    },
    {
        "name": "Kerala Nature & Ayurveda",
        "inputs": {
            "city": "Kerala",
            "days": 4,
            "interests": ["Alleppey Houseboats", "Ayurvedic Massages", "Munnar Tea Plantations"],
            "style": "Budget",
            "pace": "Relaxed",
            "month": "September"
        },
        "expected_tool_usage": ["tavily_search_tool"],
    },
    # {
    #     "name": "Varanasi Spiritual & Ghats",
    #     "inputs": {
    #         "city": "Varanasi",
    #         "days": 2,
    #         "interests": ["Spirituality", "Ghats", "Old City", "Rituals"],
    #         "style": "Budget",
    #         "pace": "Relaxed",
    #         "month": "November"
    #     },
    #     "expected_tool_usage": ["tavily_search_tool"],
    # },
    # {
    #     "name": "Kyoto Temples & Zen",
    #     "inputs": {
    #         "city": "Kyoto",
    #         "days": 3,
    #         "interests": ["Temples", "Zen Gardens", "Traditional Tea"],
    #         "style": "Mid-range",
    #         "pace": "Relaxed",
    #         "month": "April"
    #     },
    #     "expected_tool_usage": ["tavily_search_tool"],
    # },
    # {
    #     "name": "New York Urban Explorer",
    #     "inputs": {
    #         "city": "New York",
    #         "days": 4,
    #         "interests": ["Shopping", "Museums", "Central Park", "Skyline Views"],
    #         "style": "Luxury",
    #         "pace": "Packed",
    #         "month": "May"
    #     },
    #     "expected_tool_usage": ["tavily_search_tool", "google_serper_search_tool"],
    # },
    # {
    #     "name": "Rome Ancient & Pasta",
    #     "inputs": {
    #         "city": "Rome",
    #         "days": 3,
    #         "interests": ["Coliseum", "Vatican", "Pasta", "Ancient History"],
    #         "style": "Mid-range",
    #         "pace": "Balanced",
    #         "month": "September"
    #     },
    #     "expected_tool_usage": ["tavily_search_tool"],
    # }
]