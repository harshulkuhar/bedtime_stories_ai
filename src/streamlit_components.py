import streamlit as st
import time

def render_story_parameters():
    """Render the story parameter selection components."""
    language = st.selectbox(
        "Choose Your Story Language 🗣️",
        ["English", "Hindi", "Hinglish"],
        help="Select the language for your story"
    )

    setting = st.selectbox(
        "Choose the Characters of the Story 🎭",
        ["People", "Animals", "Both People & Animals"],
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
        "Choose your Culture 🌍",
        ["American", "British", "Indian", "French", "Spanish"],
        help="Select the cultural context for your story"
    )

    return language, setting, moral, culture

def render_story_output(story):
    """Render the story output and action buttons."""
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
            file_name=f"bedtime_story.txt",
            mime="text/plain"
        )

def render_story_generator():
    """Render the story generator section."""
    return st.button("✨ Create Magical Story ✨", type="primary")