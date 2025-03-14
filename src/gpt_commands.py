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
    
    language_requirements = ""
    if language.lower() == "hinglish":
        language_requirements = """
    Language Requirements:
    - Write the ENTIRE story in Hinglish using Roman script
    - Both narrative parts and dialogues should be in Hinglish
    - Use natural Hindi-English word mixing that Indian children commonly use
    - Example format:
      "Ek time ki baat hai, jab ek chota sa boy Rahul apne grandparents ke ghar gaya. Wahan usko ek magical garden mila. 'Wow!' Rahul bola, 'Kitna beautiful garden hai!'"
    """
    
    return f"""Generate a bedtime story for children up to 5 years old with the following parameters:
    Language: {language}
    Setting: {setting}
    Moral: {moral}
    Cultural Context: {culture}
    {setting_requirements}
    {language_requirements}
    
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
        8. Use gentle, soothing language appropriate for bedtime
        9. End with a clear, simple conclusion that reinforces the moral
        10. Incorporate culturally authentic elements naturally into the story
        11. When writing about animal characters:
            - Keep animal behavior realistic and natural
            - Animals should not perform human activities (no cooking, cleaning, going to school, etc.)
            - Focus on natural animal behaviors like hunting, foraging, building nests, etc.
        12. For Hinglish stories:
            - Write the ENTIRE story in Hinglish (both narration and dialogues)
            - Use Roman script throughout
            - Use natural Hindi-English mixed language that Indian children commonly use and understand
            - Example: "Ek choti si ladki Priya rehti thi. Uske paas ek cute sa puppy tha. Wo har roz uske saath park mein play karti thi."""

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
