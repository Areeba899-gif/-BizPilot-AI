
def marketing_agent(client, user_request):

    # Instructions for the marketing agent
    system_prompt = """
    You are an expert AI Marketing Agent.

    Your responsibilities are:

    1. Create marketing strategies.
    2. Write social media content.
    3. Generate advertising campaigns.
    4. Create product descriptions.
    5. Suggest business growth ideas.

    Always provide professional,
    creative and practical answers.

    Use headings and bullet points
    to organize your responses.
    """

    # Send request to AI model
    response = client.chat.completions.create(

      model="qwen/qwen3.8-27b",

        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_request
            }
        ]
    )

    # Extract AI response
    answer = response.choices[0].message.content

    return answer
