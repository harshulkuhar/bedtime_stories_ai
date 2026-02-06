"""LangGraph workflow for story generation."""
import functools
from typing import Optional

from langgraph.graph import StateGraph, END

from .state import GraphState, StoryParameters
from .nodes import plan_story, write_story, review_story, enhance_story


def should_revise(state: GraphState) -> str:
    """Conditional edge: determine if story needs revision."""
    review = state.get("review")
    
    if review is None:
        return "enhance"  # No review yet, shouldn't happen
    
    if review.approved:
        return "enhance"
    else:
        return "revise"


def create_story_graph(api_key: str) -> StateGraph:
    """Create and compile the story generation graph."""
    
    # Bind api_key to node functions
    plan_node = functools.partial(plan_story, api_key=api_key)
    write_node = functools.partial(write_story, api_key=api_key)
    review_node = functools.partial(review_story, api_key=api_key)
    enhance_node = functools.partial(enhance_story, api_key=api_key)
    
    # Create the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("planner", plan_node)
    workflow.add_node("writer", write_node)
    workflow.add_node("reviewer", review_node)
    workflow.add_node("enhancer", enhance_node)
    
    # Define edges
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "writer")
    workflow.add_edge("writer", "reviewer")
    
    # Conditional edge from reviewer
    workflow.add_conditional_edges(
        "reviewer",
        should_revise,
        {
            "revise": "writer",  # Loop back for revision
            "enhance": "enhancer"  # Move to enhancement
        }
    )
    
    workflow.add_edge("enhancer", END)
    
    return workflow.compile()


def generate_story_with_agents(
    language: str,
    setting: str,
    moral: str,
    culture: str,
    api_key: str
) -> Optional[str]:
    """
    Generate a bedtime story using the multi-agent pipeline.
    
    Args:
        language: Story language (English, Hindi, Hinglish)
        setting: Story setting (People, Animals, Both People & Animals)
        moral: Moral lesson to convey
        culture: Cultural context
        api_key: OpenAI API key
    
    Returns:
        Generated story text or None if generation fails
    """
    try:
        # Create the graph
        graph = create_story_graph(api_key)
        
        # Initialize state
        initial_state: GraphState = {
            "parameters": StoryParameters(
                language=language,
                setting=setting,
                moral=moral,
                culture=culture
            ),
            "plan": None,
            "draft": None,
            "review": None,
            "final_story": None,
            "current_stage": "starting",
            "error": None
        }
        
        # Run the graph
        final_state = graph.invoke(initial_state)
        
        if final_state.get("error"):
            return None
        
        return final_state.get("final_story")
    
    except Exception as e:
        import logging
        logging.error(f"Error in story generation: {str(e)}")
        return None


def generate_story_with_streaming(
    language: str,
    setting: str,
    moral: str,
    culture: str,
    api_key: str
):
    """
    Generate a bedtime story with intermediate state streaming.
    
    Yields intermediate states for UI progress display.
    
    Args:
        language: Story language
        setting: Story setting
        moral: Moral lesson
        culture: Cultural context
        api_key: OpenAI API key
    
    Yields:
        Tuple of (stage_name, state_dict)
    """
    try:
        graph = create_story_graph(api_key)
        
        initial_state: GraphState = {
            "parameters": StoryParameters(
                language=language,
                setting=setting,
                moral=moral,
                culture=culture
            ),
            "plan": None,
            "draft": None,
            "review": None,
            "final_story": None,
            "current_stage": "starting",
            "error": None
        }
        
        # Stream graph execution
        for state in graph.stream(initial_state):
            # state is a dict with node name as key
            for node_name, node_state in state.items():
                yield (node_name, node_state)
    
    except Exception as e:
        import logging
        logging.error(f"Error in streaming story generation: {str(e)}")
        yield ("error", {"error": str(e)})
