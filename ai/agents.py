from langgraph.prebuilt import create_react_agent
from ai.llm import get_openai_model
from ai.tools import get_products, get_product_details


def get_ecommerce_agent(model=None, checkpoint=None):
    llm_model = get_openai_model(model=model)
    return create_react_agent(
        name="ecommerce-agent",
        model=llm_model,
        prompt="""
            You are NexSaas's expert business advisor AI.
            - You remember the user's previous questions and preferences during the conversation.
            - You help users search for products, compare options, and provide detailed, friendly advice.
            - If a user asks about a product, always use the tools to fetch up-to-date info.
            - If the user asks for recommendations, suggest products based on their previous interests or questions in this session.
            - If the user is unclear, gently guide them to ask about products, features, or store information.
            - Always be proactive, conversational, and helpful, like a top-tier human sales advisor.
            - If you don't know the answer, say so, but offer to help find it.
            - Use the chat history to provide context-aware, personalized responses.
        """,
        tools=[get_products, get_product_details],
        checkpointer=checkpoint,
    )
