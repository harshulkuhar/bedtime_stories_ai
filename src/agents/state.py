"""State definitions for the story generation graph."""
from typing import Optional, Literal
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class StoryParameters(BaseModel):
    """Input parameters for story generation."""
    language: str = Field(description="Language for the story (English, Hindi, Hinglish)")
    setting: str = Field(description="Story setting (People, Animals, Both People & Animals)")
    moral: str = Field(description="Moral lesson to convey")
    culture: str = Field(description="Cultural context for the story")


class StoryPlan(BaseModel):
    """Story outline created by the planner agent."""
    title: str = Field(description="Title of the story")
    main_characters: list[str] = Field(description="List of main characters with brief descriptions")
    setting_description: str = Field(description="Description of the story setting")
    plot_outline: str = Field(description="Brief outline of beginning, middle, and end")
    moral_integration: str = Field(description="How the moral lesson will be woven into the story")


class ReviewFeedback(BaseModel):
    """Feedback from the reviewer agent."""
    approved: bool = Field(description="Whether the story passes quality checks")
    age_appropriate: bool = Field(description="Whether content is suitable for 2-5 year olds")
    moral_clarity: bool = Field(description="Whether the moral lesson is clear")
    length_ok: bool = Field(description="Whether the story length is appropriate (250-350 words)")
    feedback: str = Field(description="Detailed feedback for improvements")
    revision_count: int = Field(default=0, description="Number of revision attempts")


class GraphState(TypedDict):
    """Complete state for the story generation graph."""
    # Input
    parameters: StoryParameters
    
    # Intermediate states
    plan: Optional[StoryPlan]
    draft: Optional[str]
    review: Optional[ReviewFeedback]
    
    # Output
    final_story: Optional[str]
    
    # Metadata
    current_stage: str
    error: Optional[str]
