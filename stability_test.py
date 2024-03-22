import anthropic
from dotenv import load_dotenv 
import json
import os
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from library import PromptLibrary
from stability_prompts import generate_stability_user_prompt, stability_system_prompt
from datetime import datetime

load_dotenv()
client = anthropic.Client()

@dataclass
class StabilityScore:
  title: str
  stability: int
  reasoning: str  
  original_output: str
  new_output: str

def get_new_output(prompt):
  message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1000,
    temperature=0.0,
    system=prompt.system,
    messages=[
        {"role": "user", "content": prompt.user}
    ]
  )

  return message.content[0].text

def get_stability(prompt):
  new_output = get_new_output(prompt)

  message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1000,
    temperature=0.0,
    system=stability_system_prompt,
    messages=[
        {"role": "user", "content": generate_stability_user_prompt(prompt.output, new_output)}
    ]
  )

  message_data = json.loads(message.content[0].text)
  stability_score = StabilityScore(prompt.title, message_data["stability"], message_data["reasoning"], prompt.output, new_output)
  return stability_score

def perform_scoring_run(prompts):
  """Concurrently get stability scores for a list of prompts."""

  scores = []
  # got rate limited let's set a max_workers :)
  with ThreadPoolExecutor(max_workers=2) as executor:
    futures = [executor.submit(get_stability, prompt) for prompt in prompts]
    while(futures):
      done, _ = wait(futures, return_when=FIRST_COMPLETED)
      for future in done:
        score = future.result()
        futures.remove(future)
        scores.append(score)

  return scores

def build_summary_table(scores):
  """Build a summary table of stability scores."""
  table = []
  table.append("Title\tStability\tReasoning")
  for score in scores:
    table.append("\t".join([score.title, str(score.stability), score.reasoning]))
  return "\n".join([row for row in table])

def save_scores(scores, dir='./scores'):
  """Save stability scores to a json file."""
  current_time = datetime.now().strftime("%Y-%m-%d-%H-%M")
  file_name = f"raw-output-{current_time}.jsonl"
  os.makedirs(dir, exist_ok=True)
  file_path = os.path.join(dir, file_name)
  with open(file_path, "w") as f:
    for score in scores:
      f.write(json.dumps(asdict(score)))
      f.write("\n")

def save_summary_table(scores, dir='./scores'):
  """Save a summary table of stability scores."""
  current_time = datetime.now().strftime("%Y-%m-%d-%H-%M")
  file_name = f"summary-{current_time}.tsv"
  os.makedirs(dir, exist_ok=True)
  file_path = os.path.join(dir, file_name)
  with open(file_path, "w") as f:
    f.write(build_summary_table(scores))
  
if __name__ == "__main__":
  library = PromptLibrary() 
  library.load()
  prompts = library.get_prompts() 
  scores = perform_scoring_run(prompts)
  table = build_summary_table(scores)
  print(table)
  save_scores(scores)
  save_summary_table(scores)