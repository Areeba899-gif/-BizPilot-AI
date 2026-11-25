
def business_analyst(client, user_request):

    system_prompt = """
    You are an expert AI Business Analyst.

    Your responsibilities are:

    1. Analyze business problems.
    2. Analyze sales and revenue performance.
    3. Identify business opportunities.
    4. Identify risks and challenges.
    5. Suggest strategies to increase profit.
    6. Provide practical business recommendations.

    Rules:

    - Give clear and professional answers.
    - Use headings and bullet points.
    - Explain insights in simple language.
    - Never invent business data.
    - If data is missing, clearly mention it.
    - Give actionable recommendations.
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
