from agents import Agent, Runner, RunConfig, OpenAIChatCompletionsModel, AsyncOpenAI
import streamlit as st
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please check your .env file.")

# Gemini Client Setup
external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-1.5-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Makeup-specific Agent
MakeupAgent = Agent(
    name="Makeup Advisor",
    instructions="You are a beauty and makeup expert. Help users discover, compare, and understand makeup products based on their query. Be helpful, trendy, and concise."
)

async def get_makeup_suggestion(prompt):
    try:
        response = await Runner.run(MakeupAgent, input=prompt, run_config=config)
        return response.final_output
    except Exception as e:
        return f"❌ Error: {e}"

# Streamlit UI setup
st.set_page_config(page_title="MakeupMate AI 💄", page_icon="💋")

if "makeup_history" not in st.session_state:
    st.session_state.makeup_history = []

# Sidebar
st.sidebar.title("💄 MakeupMate AI")
st.sidebar.markdown("## 💋 Past Looks & Searches")

for i, item in enumerate(reversed(st.session_state.makeup_history), 1):
    st.sidebar.markdown(f"**{i}.** {item['query'][:25]}...")
    if st.sidebar.button(f"View {i}", key=f"view_{i}"):
        st.session_state["viewed_search"] = item

# Viewed search result
if "viewed_search" in st.session_state:
    viewed = st.session_state["viewed_search"]
    st.markdown("## 🔍 Search Result")
    st.markdown(f"**Query:** {viewed['query']}")
    st.markdown("**MakeupMate's Response:**")
    st.success(viewed['response'])

# Main title
st.title("💋 MakeupMate AI - Your Personal Beauty Advisor")

query = st.text_input("💄 What makeup product are you looking for?", placeholder="e.g. best matte lipstick under 1000")

if st.button("Search Makeup"):
    if not query.strip():
        st.warning("Please enter a makeup product or concern.")
    else:
        with st.spinner("Glamming up your recommendations..."):
            full_prompt = f"Suggest makeup products for: {query}"
            answer = asyncio.run(get_makeup_suggestion(full_prompt))

            st.session_state.makeup_history.append({
                "query": query,
                "response": answer
            })

            st.subheader("✅ MakeupMate's Recommendation:")
            st.success(answer)

# Divider
st.markdown("---")

# Featured Makeup Products
st.markdown("### ✨ Trending Makeup Picks")

makeup_products = [
    {"name": "Maybelline Fit Me Foundation", "price": "Rs 1,199", "emoji": "🧴"},
    {"name": "Lakmé Eyeconic Kajal", "price": "Rs 299", "emoji": "👁️"},
    {"name": "MAC Matte Lipstick", "price": "Rs 2,300", "emoji": "💄"},
    {"name": "L'Oréal Paris Voluminous Mascara", "price": "Rs 899", "emoji": "🌟"},
    {"name": "Nykaa Matte Lip Crayon", "price": "Rs 799", "emoji": "🖍️"},
    {"name": "Huda Beauty Highlighter", "price": "Rs 3,200", "emoji": "✨"},
]

cols = st.columns(3)
for col, product in zip(cols * (len(makeup_products) // 3 + 1), makeup_products):
    col.markdown(f"**{product['emoji']} {product['name']}**\n\n💰 {product['price']}")

# Footer
st.markdown("---")
st.markdown("💄 **MakeupMate AI** &copy; 2025 | Created by Rahat Bano")



