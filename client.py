from groq import Groq


api_key = os.getenv("GROQ_API_KEY")
    client = Groq(api_key=api_key)

def aiProcess(command):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile", # The "Smart" model
        messages=[
            {
                "role": "system",
                "content": "You are Jarvis, a helpful and witty virtual assistant."
            },
            {
                "role": "user",
                "content": command
            }
        ]
    )
    return completion.choices[0].message.content