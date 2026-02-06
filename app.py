import streamlit as st
import logging
from styles.css import get_css
from styles.templates import get_title_section, get_sidebar_content
from src.gpt_commands import generate_story, generate_story_stream
from src.streamlit_components import render_story_parameters, render_story_output, render_story_generator


# Custom CSS
def local_css():
    st.markdown(get_css(), unsafe_allow_html=True)


def get_stage_display(stage: str) -> tuple[str, str]:
    """Get display emoji and text for each stage."""
    stages = {
        "planner": ("📋", "Planning your story..."),
        "writer": ("✍️", "Writing the story..."),
        "reviewer": ("🔍", "Reviewing for quality..."),
        "enhancer": ("✨", "Adding final polish..."),
        "error": ("❌", "Oops! Something went wrong"),
    }
    return stages.get(stage, ("🔄", "Processing..."))


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
        
        # Add mode toggle
        st.markdown("---")
        st.markdown("### ⚙️ Generation Mode")
        use_agents = st.toggle(
            "Use AI Agents",
            value=True,
            help="Enable multi-agent pipeline for higher quality stories"
        )
        show_progress = st.toggle(
            "Show Progress",
            value=True,
            help="Display agent progress during generation"
        ) if use_agents else False
    
    # Main content
    col1, col2 = st.columns([1, 1.5])
    with col1:
        # Input parameters
        language, setting, moral, culture = render_story_parameters()
    with col2:
        # Generate story button
        if render_story_generator():
            if use_agents and show_progress:
                # Streaming mode with progress display
                progress_container = st.empty()
                story_container = st.empty()
                final_story = None
                
                with st.spinner("🪄 Weaving your magical bedtime story..."):
                    for stage, state in generate_story_stream(language, setting, moral, culture):
                        emoji, text = get_stage_display(stage)
                        progress_container.info(f"{emoji} **{text}**")
                        
                        # Show intermediate outputs
                        if stage == "planner" and state.get("plan"):
                            plan = state["plan"]
                            with st.expander("📋 Story Plan", expanded=False):
                                st.write(f"**Title:** {plan.title}")
                                st.write(f"**Characters:** {', '.join(plan.main_characters)}")
                                st.write(f"**Setting:** {plan.setting_description}")
                        
                        if stage == "enhancer" and state.get("final_story"):
                            final_story = state["final_story"]
                
                progress_container.empty()
                
                if final_story:
                    render_story_output(final_story)
                else:
                    st.error("❌ Oops! Something went wrong. Let's try again!")
            else:
                # Simple mode
                with st.spinner("🪄 Weaving your magical bedtime story..."):
                    story = generate_story(language, setting, moral, culture, use_agents=use_agents)
                    if story:
                        render_story_output(story)
                    else:
                        st.error("❌ Oops! Something went wrong. Let's try again!")


if __name__ == "__main__":
    main()

