"""Agent node functions for the story generation graph."""
import json
import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from .state import GraphState, StoryPlan, ReviewFeedback
from .prompts import (
    PLANNER_SYSTEM_PROMPT,
    WRITER_SYSTEM_PROMPT,
    REVIEWER_SYSTEM_PROMPT,
    ENHANCER_SYSTEM_PROMPT
)


def get_llm(api_key: str, model: str = "gpt-5-mini", temperature: float = 0.7) -> ChatOpenAI:
    """Get a configured LLM instance."""
    return ChatOpenAI(
        api_key=api_key,
        model=model,
        temperature=temperature
    )


def get_setting_requirements(setting: str) -> str:
    """Get specific requirements based on story setting."""
    if setting == "Both People & Animals":
        return """
Setting Requirements:
- Include at least one human character and one animal character as main characters
- Create meaningful interaction between the human and animal character
- Both the human and animal should contribute to the story's resolution"""
    return ""


def get_language_requirements(language: str) -> str:
    """Get language-specific requirements."""
    if language.lower() == "hinglish":
        return """
Language Requirements:
- Write the ENTIRE story in Hinglish using Roman script
- Both narrative parts and dialogues should be in Hinglish
- Use natural Hindi-English word mixing that Indian children commonly use
- Example: "Ek time ki baat hai, jab ek chota sa boy Rahul apne grandparents ke ghar gaya."
"""
    return ""


def plan_story(state: GraphState, api_key: str) -> dict:
    """Planner agent: Creates story outline and character profiles."""
    try:
        params = state["parameters"]
        llm = get_llm(api_key, temperature=0.8)
        
        user_prompt = f"""Create a story plan with these parameters:
Language: {params.language}
Setting: {params.setting}
Moral: {params.moral}
Cultural Context: {params.culture}
{get_setting_requirements(params.setting)}
{get_language_requirements(params.language)}

Respond with a JSON object containing:
- title: string
- main_characters: array of character descriptions
- setting_description: string
- plot_outline: string with beginning, middle, end
- moral_integration: how the moral will emerge naturally"""

        messages = [
            SystemMessage(content=PLANNER_SYSTEM_PROMPT),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        content = response.content
        
        # Parse JSON from response
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        plan_data = json.loads(content.strip())
        plan = StoryPlan(**plan_data)
        
        return {
            "plan": plan,
            "current_stage": "planned"
        }
    except Exception as e:
        logging.error(f"Error in planner: {str(e)}")
        return {
            "error": f"Planning failed: {str(e)}",
            "current_stage": "error"
        }


def write_story(state: GraphState, api_key: str) -> dict:
    """Writer agent: Generates the full story based on the plan."""
    try:
        params = state["parameters"]
        plan = state["plan"]
        review = state.get("review")
        llm = get_llm(api_key, temperature=0.7)
        
        revision_context = ""
        if review and not review.approved:
            revision_context = f"""
REVISION NEEDED - Previous feedback:
{review.feedback}

Please address this feedback while writing the story."""
        
        user_prompt = f"""Write a bedtime story based on this plan:

Title: {plan.title}
Characters: {', '.join(plan.main_characters)}
Setting: {plan.setting_description}
Plot: {plan.plot_outline}
Moral Integration: {plan.moral_integration}

Language: {params.language}
Cultural Context: {params.culture}
{get_language_requirements(params.language)}
{revision_context}

Write the complete story now (250-350 words)."""

        messages = [
            SystemMessage(content=WRITER_SYSTEM_PROMPT),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        
        return {
            "draft": response.content,
            "current_stage": "written"
        }
    except Exception as e:
        logging.error(f"Error in writer: {str(e)}")
        return {
            "error": f"Writing failed: {str(e)}",
            "current_stage": "error"
        }


def review_story(state: GraphState, api_key: str) -> dict:
    """Reviewer agent: Evaluates story quality and provides feedback."""
    try:
        params = state["parameters"]
        draft = state["draft"]
        current_review = state.get("review")
        revision_count = current_review.revision_count if current_review else 0
        
        llm = get_llm(api_key, temperature=0.3)  # Lower temperature for consistent evaluation
        
        user_prompt = f"""Review this bedtime story:

---
{draft}
---

Story Parameters:
- Language: {params.language}
- Setting: {params.setting}
- Moral: {params.moral}
- Culture: {params.culture}

Current revision count: {revision_count}

Respond with a JSON object:
{{
    "approved": boolean,
    "age_appropriate": boolean,
    "moral_clarity": boolean,
    "length_ok": boolean,
    "feedback": "specific feedback if not approved, or brief praise if approved"
}}

Note: You MUST approve after 2 revision attempts to avoid endless loops."""

        messages = [
            SystemMessage(content=REVIEWER_SYSTEM_PROMPT),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        content = response.content
        
        # Parse JSON from response
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        review_data = json.loads(content.strip())
        review_data["revision_count"] = revision_count + 1
        
        # Force approval after 2 attempts
        if revision_count >= 2:
            review_data["approved"] = True
            review_data["feedback"] = "Approved after maximum revision attempts."
        
        review = ReviewFeedback(**review_data)
        
        return {
            "review": review,
            "current_stage": "reviewed"
        }
    except Exception as e:
        logging.error(f"Error in reviewer: {str(e)}")
        # On error, approve to avoid blocking
        return {
            "review": ReviewFeedback(
                approved=True,
                age_appropriate=True,
                moral_clarity=True,
                length_ok=True,
                feedback="Auto-approved due to review error",
                revision_count=revision_count + 1
            ),
            "current_stage": "reviewed"
        }


def enhance_story(state: GraphState, api_key: str) -> dict:
    """Enhancer agent: Polishes the approved story."""
    try:
        params = state["parameters"]
        draft = state["draft"]
        llm = get_llm(api_key, temperature=0.5)
        
        user_prompt = f"""Polish this approved bedtime story with subtle enhancements:

---
{draft}
---

Add gentle sensory details, ensure smooth transitions, and make sure the ending is satisfying and sleep-inducing.
Language: {params.language}
{get_language_requirements(params.language)}

Return ONLY the enhanced story, nothing else."""

        messages = [
            SystemMessage(content=ENHANCER_SYSTEM_PROMPT),
            HumanMessage(content=user_prompt)
        ]
        
        response = llm.invoke(messages)
        
        return {
            "final_story": response.content,
            "current_stage": "complete"
        }
    except Exception as e:
        logging.error(f"Error in enhancer: {str(e)}")
        # Fall back to draft on error
        return {
            "final_story": state["draft"],
            "current_stage": "complete"
        }
