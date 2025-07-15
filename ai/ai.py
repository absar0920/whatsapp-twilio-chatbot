from ai.agents import get_ecommerce_agent


class BusinessAdvisorAgent:
    def __init__(self):
        self.agent = get_ecommerce_agent()

    def handle_query(self, user_query: str, chat_history: list = None) -> tuple:
        if chat_history is None:
            chat_history = []
        chat_history = chat_history + [{"role": "user", "content": user_query}]
        responses = self.agent.invoke({"messages": chat_history})
        response = responses["messages"][-1].content
        chat_history.append({"role": "assistant", "content": response})
        if not response or response.strip().lower() in {
            "n/a",
            "none",
            "no answer",
            "not applicable",
        }:
            fallback = (
                f"Hi! I'm your NexSaas assistant. You can ask me about our products, prices, availability, or details about any item in our store. "
                f"For example, try asking 'What laptops do you have?' or 'Tell me about the Apple iPhone 14 Pro.'"
            )
            chat_history[-1]["content"] = fallback
            return fallback, chat_history
        return response, chat_history
