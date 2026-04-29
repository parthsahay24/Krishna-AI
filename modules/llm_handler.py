import re
from groq import Groq
from . import config
from . import memory_manager
from . import prompts


client = Groq(api_key=config.GROQ_API_KEY)

def get_krishna_response(user_text):
    # 1. Ask Memory: "Who am I talking to?"
    user_data = memory_manager.get_user_data()
    user_name = user_data.get("name")

    # 2. Logic: If we have no name, Krishna must be in "Discovery Mode"
    if not user_name:
        system_instructions = prompts.KRISHNA_SYSTEM_PROMPT + prompts.NAME_EXTRACTION_INSTRUCTION
    else:
        name_instruction = f"\nCRITICAL: The user's name is {user_name}. ALWAYS address them as {user_name}."
        system_instructions = prompts.KRISHNA_SYSTEM_PROMPT.format(user_name=user_name) + name_instruction


    # 3. Call the Brain - Groq
    response = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_text}
        ]
    )
    
    # Ensure krishna_text is a string, even if the AI returns nothing
    krishna_text = response.choices[0].message.content or ""


    # 4. The "Learning" Phase
    if not user_name and "[SAVE_NAME:" in krishna_text:
        match = re.search(r"\[SAVE_NAME:\s*(.*?)\]", krishna_text)
        if match:
            extracted_name = re.sub(r"[^\w\s]", "", match.group(1))
            extracted_name = re.sub(r"\s+", " ", extracted_name).strip()
            if extracted_name:
                memory_manager.save_user_name(extracted_name)
    
    # 5. UNIVERSAL CLEANUP (Move these outside all 'if' blocks)
    # This ensures the user NEVER sees a robot tag
    krishna_text = re.sub(r"\[SAVE_NAME:.*?\]", "", krishna_text)
    krishna_text = re.sub(r"\[waiting for name\]", "", krishna_text)
    
    return krishna_text.strip()
