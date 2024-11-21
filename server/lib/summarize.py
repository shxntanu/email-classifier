import ollama

def summarize_email(email_content: str, model: str = "qwen:1.8b") -> str:    
    system_prompt = """You are a Language expert specializing in concise and meaningful summaries on the content of the email provided to you. 
    Generate a crisp summary of the email content provided to you which the user can glance at to quickly know the gist of the email without having to
    go through the email."""
    
    message = ""
    stream = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": email_content}
        ],
        stream=True
    )
    
    for chunk in stream:
        content = chunk["message"]["content"]
        message += content
    
    return message.strip()