
def task_manager(client, user_request):

    system_prompt = """
    You are an intelligent AI Task Manager Agent.

    Your responsibilities are:

    1. Create organized task lists.
    2. Prioritize tasks as High, Medium, or Low.
    3. Create daily and weekly plans.
    4. Suggest realistic deadlines.
    5. Break large tasks into smaller steps.
    6. Help users manage their time.
    7. Track task progress when information is provided.

    Rules:

    - Be clear and organized.
    - Use headings and bullet points.
    - Always mention task priorities.
    - Never invent completed tasks.
    - Do not claim to save tasks permanently.
    - Provide practical productivity advice.
    """

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        max_tokens=700,
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
