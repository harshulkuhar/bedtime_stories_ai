import streamlit as st
import logging
from styles.css import get_css
from styles.templates import get_title_section, get_sidebar_content
from src.gpt_commands import generate_story
from src.streamlit_components import render_story_parameters, render_story_output, render_story_generator

# Custom CSS
def local_css():
    st.markdown(get_css(), unsafe_allow_html=True)

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
    st.markdown(get_title_section(), unsafe_allow_html=True)
    # Sidebar configuration
    with st.sidebar:
        st.markdown(get_sidebar_content(), unsafe_allow_html=True)
    # Main content
    col1, col2 = st.columns([1, 1.5])
    with col1:
        # Input parameters
        language, setting, moral, culture = render_story_parameters()
    with col2:
        # Generate story button
        if render_story_generator():
            with st.spinner("🪄 Weaving your magical bedtime story..."):
                story = generate_story(language, setting, moral, culture) 
                if story:
                    render_story_output(story)
                else:
                    st.error("❌ Oops! Something went wrong. Let's try again!")

if __name__ == "__main__":
    main()
