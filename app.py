import streamlit as st
import openai
import json
import logging

# Configure OpenAI
client = openai.OpenAI(api_key=st.secrets["OPENAI_KEY"])

# Custom CSS
def local_css():
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
            background-color: #f8f9fa;
        }
        .stButton > button {
            width: 100%;
            padding: 0.5rem;
            border-radius: 15px;
            font-size: 1.2rem;
        }
        .story-container {
            background-color: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-top: 1rem;
        }
        .title-container {
            background: linear-gradient(90deg, #70a1ff, #7bed9f);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            text-align: center;
        }
        .parameter-card {
            background-color: white;
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }
        .sidebar-content {
            background-color: white;
            padding: 1.5rem;
            border-radius: 15px;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)

def generate_story(language, setting, moral, culture):
    """
    Generate a bedtime story based on given parameters using OpenAI's GPT-4.
    
    Args:
        language (str): The language to generate the story in
        setting (str): The story setting (Animals/People/Both)
        moral (str): The moral lesson to convey
        culture (str): The cultural context for the story
    
    Returns:
        str: Generated story text or None if generation fails
    """
    # Construct the prompt
    prompt = f"""Generate a bedtime story for children up to 5 years old with the following parameters:
    Language: {language}
    Setting: {setting}
    Moral: {moral}
    Cultural Context: {culture}
    
    The story should be:
    1. Simple and easy to understand
    2. Not more than 5-7 minutes when read aloud
    3. Age-appropriate (0-5 years)
    4. Have a clear moral lesson
    5. Include engaging characters and simple dialogue
    6. Use culturally appropriate names, settings, and references for {culture} culture
    7. Include relevant cultural elements without being stereotypical
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a specialized children's bedtime story writer. Follow these strict guidelines:
                        1. Keep stories between 250-350 words
                        2. Use simple vocabulary suitable for 2-5 year olds
                        3. Structure each story with:
                           - A clear beginning introducing main character(s)
                           - A simple problem or situation
                           - A resolution that teaches the moral lesson
                        4. Use repetitive elements and simple patterns
                        5. Include 2-3 characters maximum
                        6. Avoid complex plots or scary elements
                        7. Use short sentences and paragraphs
                        8. Include gentle, soothing language appropriate for bedtime
                        9. End with a clear, simple conclusion that reinforces the moral
                        10. Incorporate culturally authentic elements naturally into the story"""
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating story: {str(e)}")
        return None

def main():
    """Main function to run the Streamlit application."""
    
    # Page configuration
    st.set_page_config(
        page_title="Magical Bedtime Stories",
        page_icon="🌙",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS
    local_css()
    
    # Main title with styling
    st.markdown("""
        <div class="title-container">
            <h1 style='color: white; margin-bottom: 0.5rem;'>
                🌙 Magical Bedtime Stories ✨
            </h1>
            <p style='color: white; font-size: 1.2rem; margin: 0;'>
                Create enchanting stories for your little ones
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-content">
                <h3>📖 About</h3>
                <p style='font-size: 0.9rem; color: #666;'>
                    Welcome to Magical Bedtime Stories! This story generator creates 
                    personalized bedtime stories perfect for children aged 2-5 years. 
                    Each story teaches valuable life lessons while being engaging and fun!
                </p>
            </div>
            <div class="sidebar-content">
                <h3>✨ How to Use</h3>
                <p style='font-size: 0.9rem; color: #666;'>
                    1. Choose your preferred language<br>
                    2. Select the story setting<br>
                    3. Pick a moral lesson<br>
                    4. Click 'Create Magical Story'<br>
                    5. Save or generate new stories!
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Main content
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        # Input parameters
        language = st.selectbox(
            "Choose Your Story Language 🗣️",
            ["English", "Hindi", "Hinglish"],
            help="Select the language for your story"
        )

        setting = st.selectbox(
            "Pick Your Story World 🎭",
            ["Animals", "People", "Both"],
            help="Choose who the story will be about"
        )

        moral = st.selectbox(
            "Choose the Life Lesson 🌟",
            [
                "Kindness", "Honesty", "Sharing", "Patience",
                "Courage", "Friendship", "Love", "Respect",
                "Responsibility", "Gratitude", "Empathy",
                "Hard Work", "Consistency"
            ],
            help="Select the moral lesson for your story"
        )

        culture = st.selectbox(
            "Choose Cultural Context 🌍",
            ["American", "British", "Indian", "French", "Spanish"],
            help="Select the cultural context for your story"
        )
    
    with col2:
        # Generate story button
        if st.button("✨ Create Magical Story ✨", type="primary"):
            with st.spinner("🪄 Weaving your magical bedtime story..."):
                story = generate_story(language, setting, moral, culture)
                
                if story:
                    st.success("✨ Your magical story is ready!")
                    st.markdown(story)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 Generate New Story"):
                            st.rerun()
                    with col2:
                        st.download_button(
                            label="📥 Save Story",
                            data=story,
                            file_name=f"bedtime_story_{moral.lower()}.txt",
                            mime="text/plain"
                        )
                else:
                    st.error("❌ Oops! Something went wrong. Let's try again!")

if __name__ == "__main__":
    main()
