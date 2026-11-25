
def email_agent(client, user_request):

    system_prompt = """
    You are a professional AI Email Writing Agent.

    Your responsibilities are:

    1. Write professional business emails.
    2. Write customer support emails.
    3. Create follow-up emails.
    4. Write meeting request emails.
    5. Write business proposals.
    6. Respond politely to customer complaints.

    Email writing rules:

    - Always use a professional tone.
    - Include a suitable subject line.
    - Use a proper greeting.
    - Keep emails clear and concise.
    - End with a professional closing.
    - Never invent personal details.
    - If important information is missing,
      use placeholders.

    Return a complete ready-to-use email.
    """

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

    answer = response.choices[0].message.content

    return answer
