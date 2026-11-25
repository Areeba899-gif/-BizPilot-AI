
from agents.marketing_agent import marketing_agent
from agents.email_agent import email_agent
from agents.business_analyst import business_analyst
from agents.task_manager import task_manager


def run_coordinator(client, user_request):

    request = user_request.lower()

    if any(word in request for word in [
        "email", "reply", "follow-up", "follow up"
    ]):
        selected_agent = "Email Agent"
        answer = email_agent(client, user_request)

    elif any(word in request for word in [
        "marketing", "advertisement", "campaign",
        "instagram", "promotion"
    ]):
        selected_agent = "Marketing Agent"
        answer = marketing_agent(client, user_request)

    elif any(word in request for word in [
        "sales analysis", "analyze sales",
        "revenue", "profit", "sales report"
    ]):
        selected_agent = "Business Analyst Agent"
        answer = business_analyst(client, user_request)

    elif any(word in request for word in [
        "task", "schedule", "deadline",
        "to-do", "todo", "daily plan", "weekly plan"
    ]):
        selected_agent = "Task Manager Agent"
        answer = task_manager(client, user_request)

    else:
        selected_agent = "General Assistant"

        response = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            max_tokens=700,
            messages=[
                {
                    "role": "system",
                    "content": "You are BizPilot AI, a helpful professional business assistant. Keep answers clear and practical."
                },
                {
                    "role": "user",
                    "content": user_request
                }
            ]
        )

        answer = response.choices[0].message.content

    return selected_agent, answer


