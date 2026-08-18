import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# Configure APIs
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

MODEL_INFO = "gemini-2.0-flash"
MODEL_SCRIPT = "gemini-2.0-flash"

# Streamlit page setup
st.set_page_config(
    page_title="StoryForge Agent",
    page_icon="🌐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Custom modern CSS theme ---
st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: #f5f5f5;
        }
        h1, h2, h3 {
            text-align: center;
            color: #F9FAFB !important;
        }
        .stTextInput>div>div>input {
            border: 1px solid #6EE7B7 !important;
            border-radius: 10px;
            padding: 12px;
            background-color: #111827;
            color: white !important;
        }
        div.stButton > button {
            background: linear-gradient(90deg, #06b6d4, #3b82f6);
            color: white;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            border: none;
            transition: 0.3s ease-in-out;
        }
        div.stButton > button:hover {
            transform: scale(1.05);
            background: linear-gradient(90deg, #2563eb, #06b6d4);
        }
        .card {
            background-color: rgba(255, 255, 255, 0.05);
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            margin-top: 20px;
        }
        .stRadio > div {
            justify-content: center;
        }
        footer, .stCaption {
            text-align: center;
            color: #9CA3AF;
        }
    </style>
""", unsafe_allow_html=True)


# --- Main function for real-time info fetching ---
def get_realtime_info(query):
    """
    Fetches up-to-date information about any topic using Tavily Search API
    and summarizes it using Gemini.
    """
    try:
        resp = tavily_client.search(
            query=query,
            max_results=3,
            topic="general"
        )

        if resp and resp.get("results"):
            summaries = []
            for r in resp["results"]:
                title = r.get("title", "")
                snippet = r.get("snippet", "")
                url = r.get("url", "")
                summaries.append(f"**{title}**\n\n{snippet}\n\n🔗 {url}")
            source_info = "\n\n---\n\n".join(summaries)
        else:
            source_info = f"No recent updates found on '{query}'."
    except Exception as e:
        st.error(f"❌ Error fetching info: {e}")
        return None

    # Refine & summarize the content via Gemini
    prompt = f"""
You are a professional researcher and content creator with expertise in multiple fields.
Using the following real-time information, write an accurate, engaging, and human-like summary
for the topic: '{query}'.

Requirements:
- Keep it factual, insightful, and concise (around 200 words).
- Maintain a smooth, natural tone.
- Highlight key takeaways or trends.
- Avoid greetings or self-references.

Source information:
{source_info}

Output only the refined, human-readable content.
"""
    try:
        model = genai.GenerativeModel(MODEL_INFO)
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else source_info
    except Exception as e:
        st.error(f"❌ Error generating summary: {e}")
        return source_info


# --- Generate video transcription ---
def generate_video_transcription(info_text):
    prompt = f"""
You are a creative scriptwriter.
Turn this real-time information into an engaging short video script (for YouTube Shorts or Instagram Reels).
Use a conversational tone with a strong hook and a clear call to action at the end.
Keep it around 100–120 words.

{info_text}
"""
    try:
        model = genai.GenerativeModel(MODEL_SCRIPT)
        response = model.generate_content(prompt)
        return response.text.strip() if response and response.text else "⚠️ Could not generate video script."
    except Exception as e:
        st.error(f"❌ Error generating video script: {e}")
        return None


# --- Streamlit UI ---
def main():
    st.markdown("<h1>🌐StoryForge Agent</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#D1D5DB;'>Search any topic — from world news to research trends — and get AI-powered insights & video scripts instantly 🚀</p>", unsafe_allow_html=True)

    query = st.text_input("🔎 Enter your topic or question:")

    if query:
        with st.spinner('🌍 Gathering latest information...'):
            info_result = get_realtime_info(query)

        if info_result:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("📚 AI-Generated Summary")
            st.write(info_result)
            st.markdown("</div>", unsafe_allow_html=True)

            generate_script = st.radio(
                "🎬 Generate a short video script?",
                ("No", "Yes"),
                index=0,
                horizontal=True
            )

            if generate_script == "Yes":
                with st.spinner('🎥 Crafting your video script...'):
                    script = generate_video_transcription(info_result)

                if script:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.subheader("🎥 Video Script")
                    st.write(script)
                    st.download_button(
                        label="📥 Download Script",
                        data=script,
                        file_name="video_script.txt",
                        mime="text/plain"
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Could not generate transcription.")
        else:
            st.warning("⚠️ No valid information found. Please try another query.")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.caption("Made with 💖")

if __name__ == "__main__":
    main()
