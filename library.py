from dataclasses import dataclass, asdict
import re
import os
import json

def to_snake_case(string):
  return re.sub(r'\s+', '_', string.lower())

@dataclass
class Prompt:
  title: str
  user: str
  system: str
  output: str

class PromptLibrary:
  def __init__(self, dir='./prompts/'):
    self.prompts = []
    self.dir = dir 
  
  def add_prompt(self, prompt):
    self.prompts.append(prompt)

  def save(self):
    """Save each prompt as its own json file"""
    for prompt in self.prompts:
      filename = to_snake_case(prompt.title)
      # create directory if it doesn't exist
      os.makedirs(self.dir, exist_ok=True)
      with open(f"{self.dir}{filename}.json", "w") as f:
        f.write(json.dumps(asdict(prompt)))

  def load(self):
    """Load all prompts from the directory"""
    for file in os.listdir(self.dir):
      with open(f"{self.dir}{file}", "r") as f:
        data = json.loads(f.read())
        self.prompts.append(Prompt(**data)) 

  def get_prompts(self):
    return self.prompts