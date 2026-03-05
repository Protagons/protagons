# Using a Protagon with Poe

## Server Bot Setup

1. Go to [poe.com/create_bot](https://poe.com/create_bot)
2. Choose **Server Bot** for full control
3. In your server bot's message handler, use the Protagon as a system message:

```python
from protagons import load

protagon = load("character.protagon.json")

async def handle_message(request):
    messages = [
        {"role": "system", "content": protagon.synthesized_prompt},
        {"role": "user", "content": request.query[-1].content},
    ]
    # Forward to your LLM of choice
    ...
```

## Prompt Bot Setup (simpler)

1. Go to [poe.com/create_bot](https://poe.com/create_bot)
2. Choose **Prompt Bot**
3. Paste the `synthesized_prompt.content` into the **System Prompt** field
4. Set the bot name to the Protagon's name
