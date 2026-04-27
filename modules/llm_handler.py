from groq import Groq
from . import config
from . import prompts
from . import memory_manager


client = Groq(api_key=config.GROQ_API_KEY)

def get_krishna_response(user_text):
    # 1. Ask Memory: "Who am I talking to?"
    user_data = memory_manager.get_user_data()
    user_name = user_data.get("name")

    # 2. Logic: If we have no name, Krishna must be in "Discovery Mode"
    if not user_name:
        system_instructions = (
            prompts.KRISHNA_SYSTEM_PROMPT + 
            "\nCRITICAL: You do not know the user's name yet. "
            "Politely ask for their name in your first response."
        )
    else:
        system_instructions = prompts.KRISHNA_SYSTEM_PROMPT.format(user_name=user_name)

    # 3. Call Groq
    response = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_text}
        ]
    )
    
    krishna_text = response.choices[0].message.content

    # 4. Professional "Learning" Trick: 
    # If Krishna just learned a name, we extract it and save it.
    # (For now, we'll assume the first thing the user says is their name)
    if not user_name and len(user_text.split()) <= 2:
        memory_manager.save_user_name(user_text)

    return krishna_text
