import pandas as pd
import uuid

# Conversations data with memory labels (STM or LTM)
conversations = [
    [
        {"role": "user", "content": "Hi, I want help choosing colors that suit me. I usually look pale in bright red.", "memory": "LTM"},
        {"role": "assistant", "content": "Got it. Let’s find better options. Do you have any colors you already like?", "memory": "STM"},
        {"role": "user", "content": "Yes, I feel comfortable in pastel shades like lavender and peach.", "memory": "LTM"},
        {"role": "assistant", "content": "Perfect, pastels balance your complexion well. Do you want me to suggest outfits?", "memory": "STM"},
        {"role": "user", "content": "Yes, please suggest pastel options for office wear.", "memory": "STM"},
    ],
    [
        {"role": "user", "content": "Hey, I want outfit ideas for a dinner date this weekend.", "memory": "STM"},
        {"role": "assistant", "content": "Sure, what’s your usual style for evenings?", "memory": "STM"},
        {"role": "user", "content": "I prefer elegant looks, usually a black dress or something simple.", "memory": "LTM"},
        {"role": "assistant", "content": "Noted. Do you like to accessorize heavily or keep it minimal?", "memory": "STM"},
        {"role": "user", "content": "Minimal accessories, I feel more confident that way.", "memory": "LTM"},
    ],
    [
        {"role": "user", "content": "I need help picking beachwear for my holiday.", "memory": "STM"},
        {"role": "assistant", "content": "Nice! Do you like flowy outfits or more fitted styles?", "memory": "STM"},
        {"role": "user", "content": "Flowy, like maxi dresses. They’re comfortable for me.", "memory": "LTM"},
        {"role": "assistant", "content": "Great. Do you also wear shorts or prefer dresses only?", "memory": "STM"},
        {"role": "user", "content": "Mostly dresses, but I’ll take shorts too for variety.", "memory": "STM"},
    ],
    [
        {"role": "user", "content": "Can you help me avoid fabrics that irritate my skin?", "memory": "LTM"},
        {"role": "assistant", "content": "Of course. Do you know which fabrics trouble you?", "memory": "STM"},
        {"role": "user", "content": "Yes, wool sweaters make me very itchy.", "memory": "LTM"},
        {"role": "assistant", "content": "Noted. Do you want alternatives for winter wear?", "memory": "STM"},
        {"role": "user", "content": "Yes, something cozy but not wool.", "memory": "STM"},
    ],
    [
        {"role": "user", "content": "I’m attending a wedding soon. Can you suggest something?", "memory": "STM"},
        {"role": "assistant", "content": "Definitely. Do you like traditional or modern styles for weddings?", "memory": "STM"},
        {"role": "user", "content": "I prefer traditional outfits with embroidery.", "memory": "LTM"},
        {"role": "assistant", "content": "Beautiful. Any favorite colors for weddings?", "memory": "STM"},
        {"role": "user", "content": "Gold and maroon always work for me.", "memory": "LTM"},
    ],
    [
        {"role": "user", "content": "What’s a good casual style for weekends?", "memory": "STM"},
        {"role": "assistant", "content": "What do you normally wear on weekends?", "memory": "STM"},
        {"role": "user", "content": "Mostly jeans and sneakers. I like to keep it simple.", "memory": "LTM"},
        {"role": "assistant", "content": "Great. Want me to suggest casual layers for variety?", "memory": "STM"},
        {"role": "user", "content": "Yes, maybe some hoodie and jacket combos.", "memory": "STM"},
    ],
    [
        {"role": "user", "content": "I’m building a work wardrobe. Can you guide me?", "memory": "STM"},
        {"role": "assistant", "content": "Sure. Do you like more formal or business casual?", "memory": "STM"},
        {"role": "user", "content": "Business casual. I don’t like stiff suits.", "memory": "LTM"},
        {"role": "assistant", "content": "Understood. Any colors you prefer for work?", "memory": "STM"},
        {"role": "user", "content": "I like navy and beige for work outfits.", "memory": "LTM"},
    ],
    [
        {"role": "user", "content": "Do you think oversized clothes suit me?", "memory": "STM"},
        {"role": "assistant", "content": "Depends! Do you usually enjoy fitted or loose clothing?", "memory": "STM"},
        {"role": "user", "content": "I feel most comfortable in slightly loose fits.", "memory": "LTM"},
        {"role": "assistant", "content": "Got it. Want me to suggest balanced oversized styles?", "memory": "STM"},
        {"role": "user", "content": "Yes, maybe for streetwear looks.", "memory": "STM"},
    ],
    [
        {"role": "user", "content": "I want ideas for winter layering.", "memory": "STM"},
        {"role": "assistant", "content": "Sure. Do you already have a favorite winter style?", "memory": "STM"},
        {"role": "user", "content": "Yes, I love layering hoodies with long coats.", "memory": "LTM"},
        {"role": "assistant", "content": "Nice. Any fabrics or colors to avoid?", "memory": "STM"},
        {"role": "user", "content": "Avoid bright neon colors in winter wear.", "memory": "LTM"},
    ],
    [
        {"role": "user", "content": "What should I wear for an interview?", "memory": "STM"},
        {"role": "assistant", "content": "Good question. Do you lean more formal or semi-formal?", "memory": "STM"},
        {"role": "user", "content": "Semi-formal, I want to look sharp but approachable.", "memory": "LTM"},
        {"role": "assistant", "content": "Great. Any specific preferences in outfits?", "memory": "STM"},
        {"role": "user", "content": "Blazers with neutral shirts usually work for me.", "memory": "LTM"},
    ],
]

# Flatten into CSV rows with user_id, session_id, and memory column
rows = []
for conv_index, conv in enumerate(conversations, 1):
    user_id = f"user_{conv_index}"
    session_id = str(uuid.uuid4())
    for turn_index, msg in enumerate(conv, 1):
        rows.append({
            "user_id": user_id,
            "session_id": session_id,
            "turn": turn_index,
            "role": msg["role"],
            "content": msg["content"],
            "memory": msg["memory"]
        })

df = pd.DataFrame(rows)

# Save to CSV
file_path = "fashion_assistant_conversations_with_memory.csv"
df.to_csv(file_path, index=False)
