# Using a Protagon with Custom GPTs

## Steps

1. Download a `.protagon.json` from [protagons.com/library](https://protagons.com/library)
2. Open the file and copy the `synthesized_prompt.content` field
3. Go to [chat.openai.com](https://chat.openai.com) > Explore GPTs > Create
4. Paste the prompt into the **Instructions** field
5. Set the GPT name to the Protagon's `name` field
6. Optionally set the description to the Protagon's `tagline`

## Programmatic extraction

```python
from protagons import load

protagon = load("character.protagon.json")
instructions = protagon.synthesized_prompt

# Copy to clipboard (macOS)
import subprocess
subprocess.run(["pbcopy"], input=instructions.encode(), check=True)
print("Copied to clipboard!")
```

## Notes

- Custom GPTs have a ~8,000 character instruction limit
- Most Protagon synthesized prompts are 1,500-3,000 characters
- For dark/adversarial content tiers, add a fiction wrapper
