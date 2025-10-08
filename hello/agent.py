import os
import random
import dotenv
import google.auth
from google.adk.agents import Agent

dotenv.load_dotenv()

def greet(name: str) -> str:
    """Greets a user by name.
    Args:
        name: A string denoting the user's name.
    Returns:
        A string greeting the user.
    """
    return f"Hello, {name}!"

def roll_dice(n_dice: int) -> list[int]:
    """Rolls n_dice 6-sided dice and returns the results.
    Args:
        n_dice: An integer denoting the number of dice to be rolled.
    Returns:
        A list of integers denoting the results of the rolled dice.
    """
    return [random.randint(1, 6) for _ in range(n_dice)]

class RootAgent(Agent):
    """The root agent for the application."""

def __init__(self, **kwargs):
    super().__init__(
        **kwargs
    )
    
    self.set_config(
        name="root_agent",
        model="gemini-2.5-flash",
        instruction="You are an AI assistant designed to provide helpful information.",
        tools=[greet, roll_dice],
)

root_agent = RootAgent
