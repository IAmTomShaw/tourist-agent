import json
from agents import Agent, Runner, WebSearchTool
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

load_dotenv()

class AgentRecommendation(BaseModel):
  name: str = Field(..., description="Name of the recommended activity")
  description: str = Field(..., description="Brief description of the activity")
  location: str = Field(..., description="Location of the activity")
  price: str = Field(..., description="Price of the activity")
  length_minutes: int = Field(..., description="Length of the event in minutes")
  date: str = Field(..., description="Suggested date for the activity in ISO format")
  start_time: str = Field(..., description="Suggested start time in hours and minutes (HH:MM)")
  end_time: str = Field(..., description="Suggested end time in hours and minutes (HH:MM)")

async def run_agent(start_date: str, end_date: str, location: str, busy_periods: list[dict]):

  print('running agent...')
    
  agent = Agent(
    name="Travel Research Agent",
    tools=[
      WebSearchTool()
    ],
    instructions="""
      You are a tourist research expert. Your task is to help identify the best activities for a user to do during their trip based on their calendar availability. You will be provided with the user's calendar events which indicates when they are busy. Use this information to suggest activities during their free time.

      You should search the internet for popular activities, restaurants and other things to do in the destination city. 
      Consider the user's calendar events and the location of their calendar events to avoid suggesting activities that conflict with their schedule.

      You should return a list of recommendations which include the name of the activity, a brief description, location, price, and why it is recommended based on the user's calendar availability.

      Do not return multiple activities for the same time slot. Try to fill all of the available time slots with unique activities. Make sure that the activities you suggest do not overlap with any of the busy periods provided.

      Do not return suggestions that are not happening between the start_date and end_date provided.

      If the user's existing calendar events are in locations far from the trip location, take into account that travel time will be needed to get to/from the activity between calendar events.

      If the price of an activity is unknown, provide an estimated price range.

      Also provide an estimated duration for each activity to help the user plan their schedule.

      """,
    model=os.environ.get("OPENAI_MODEL", "gpt-4o-mini"),
    output_type=list[AgentRecommendation]
  )

  chat = [
    {
      "role": "user",
      "content": f"""
      <start_date>{start_date}</start_date>
      <end_date>{end_date}</end_date>
      <location>{location}</location>
      <busy_periods>{json.dumps(busy_periods, indent=2)}</busy_periods>
      """
    }
  ]

  print('executing agent...')

  response = await Runner.run(agent, chat)

  print('agent finished.')

  return response.final_output