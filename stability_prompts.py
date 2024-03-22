stability_system_prompt = """
  You are a system that maintains a library of prompts for a major AI company.
  To ensure that the prompts are stable, you will receive the output of the system for a given prompt 
  and compare it to the output of the system for the same prompt at a later time.
  The original prompt output will be provided first, followed by the new prompt output.
  You will provide a numerical score for the stability of the prompts from 1-10, with 10 being the most stable.
  You will also provide clear and concises reasoning for your score. 
  Keep your reasonsing to specific differences or similarities between the outputs that are reflected in the score.
"""

def generate_stability_user_prompt(original_output, new_output):
  return f"""
  Original Output: 
  {original_output}\n
  
  New Output: 
  {new_output}\n
  
  On a scale of 1-10, how stable are the prompts and what is your reasons?
  Provide your response as a json object with no markup like so:
  {{
    "stability": 8
    "reasoning": "There are minor differences in wording."
  }}
  You must provide valid json without markup so the response can be direcly parsed.
  """