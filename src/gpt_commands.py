import openai
import logging
import streamlit as st

# Configure OpenAI
client = openai.OpenAI(
    api_key=st.secrets["OPENAI_KEY"]
    )

def get_story_requirements(setting):
    """Get specific requirements based on story setting."""
    if setting == "Both People & Animals":
        return """
    Setting Requirements:
    - Include at least one human character and one animal character as main characters
    - Create meaningful interaction between the human and animal character
    - Both the human and animal should contribute to the story's resolution"""
    return ""

def get_story_prompt(language, setting, moral, culture):
    """Construct the story generation prompt."""
    setting_requirements = get_story_requirements(setting)
    
    return f"""Generate a bedtime story for children up to 5 years old with the following parameters:
    Language: {language}
    Setting: {setting}
    Moral: {moral}
    Cultural Context: {culture}{setting_requirements}
    
    The story should be:
    1. Simple and easy to understand
    2. Not more than 5-7 minutes when read aloud
    3. Age-appropriate (0-5 years)
    4. Have a clear moral lesson
    5. Include engaging characters and simple dialogue
    6. Incorporate authentic cultural elements, traditions, and values
    7. Use culturally appropriate storytelling styles and themes
    8. Be respectful and inclusive in its representation
    """

def get_system_prompt():
    """Get the system prompt for story generation."""
    return """You are a specialized children's bedtime story writer. Follow these strict guidelines:
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

def generate_story(language, setting, moral, culture):
    """
    Generate a bedtime story based on given parameters using OpenAI's GPT-4.
    
    Args:
        language (str): The language to generate the story in
        setting (str): The story setting (People/Animals/Both People & Animals)
        moral (str): The moral lesson to convey
        culture (str): The cultural context for the story
    
    Returns:
        str: Generated story text or None if generation fails
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": get_system_prompt()},
                {"role": "user", "content": get_story_prompt(language, setting, moral, culture)}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating story: {str(e)}")
        return None
