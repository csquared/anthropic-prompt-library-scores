# anthropic-prompt-library

Project scoring the Anthropic prompt library
First metric is "stability" - do I get the same output for a given input?
Uses Claude to assess similarity.

### Requirements

```bash
> pip install -r requirements.txt
```

### Download prompts
Uses `beautifulsoup` to scrape the prompts from the website.
Save the prompts into a json file per prompt.

Single-threaded and sleeps to be kind :)

```bash
> python scrape_prompts.py
```

### Score prompts
Re-runs the prompt and then uses claude to determine similarity of output.
Saves the full run in `.jsonl` file.
Saves a summary table as `.tsv` file.
Multi-threaded.

Note: there are some red herrings where the expected output has a redacted 

```bash
> python score_prompts.py
```
