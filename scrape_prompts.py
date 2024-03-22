import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
from library import Prompt, PromptLibrary

def scrape_one(prompt_url):
  response = requests.get(prompt_url)
  soup = BeautifulSoup(response.text, "html.parser")

  title = soup.find("h1").text
  table = soup.find("div", class_='rdmd-table-inner')
  user_content = table.find('td', string='User').find_next_sibling('td').text
  system = table.find('td', string='System') 
  if system:
    system_content = system.find_next_sibling('td').text
  else:
    system_content = ""
  example_output_heading = soup.find(id='section-example-output')
  output = example_output_heading.find_next('blockquote').text

  prompt = Prompt(title, user_content, system_content, output)
  return prompt

def scrape_all(homepage, max=5):
  prompt_links = get_prompt_links(homepage)
  library  = PromptLibrary()
  for link in prompt_links[0:max]:
    library.add_prompt(scrape_one(link))
    time.sleep(0.1) #be kind :)
  return library


def get_prompt_links(homepage):
  response = requests.get(homepage)
  soup = BeautifulSoup(response.text, "html.parser")
  anchors = soup.find_all("a")
  links = []

  for a in anchors:
     href = a.get('href')
     if href and href.startswith('page/'):
        prompt_url = urljoin(homepage, href)
        links.append(prompt_url)
  return links


if __name__ == "__main__":
    homepage = "https://docs.anthropic.com/claude/prompt-library"
    library = scrape_all(homepage, 100)
    library.save()