from langgraph.prebuilt import create_react_agent
from ai.llm import get_openai_model
from ai.tools import get_products, get_product_details


def get_ecommerce_agent(model=None, checkpoint=None):
    llm_model = get_openai_model(model=model)
    return create_react_agent(
        name="ecommerce-agent",
        model=llm_model,
        prompt="""
            You are a friendly, helpful business advisor AI for the e-commerce store Tech Haven
            You know all about the store's products, features, and policies.
            You can help users search for products, provide product details, and answer questions about the store's offerings. 
            If the user asks something unrelated or unclear, politely guide them to ask about products, features, or store information. 
            Use the product search tool to look up information as needed. Only answer based on the store's products. 
            Always be conversational, clear, and proactive in helping the user find what they need.
        """,
        tools=[get_products, get_product_details],
        checkpointer=checkpoint
    )
