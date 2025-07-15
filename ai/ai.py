from ai.agents import get_ecommerce_agent


class BusinessAdvisorAgent:
    def __init__(self):
        self.agent = get_ecommerce_agent()
        pass

    def handle_query(self, user_query: str) -> str:
        responses = self.agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_query,
                    }
                ]
            },
        )
        response = responses["messages"][-1].content
        if not response or response.strip().lower() in {
            "n/a",
            "none",
            "no answer",
            "not applicable",
        }:
            return (
                f"Hi! I'm your Tech Haven assistant. You can ask me about our products, prices, availability, or details about any item in our store. "
                f"For example, try asking 'What laptops do you have?' or 'Tell me about the Apple iPhone 14 Pro.'"
            )
        return response
