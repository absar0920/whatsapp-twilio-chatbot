from langchain_openai import ChatOpenAI


def get_openai_model(model="gpt-3.5-turbo"):
    """
    Get the OpenAI model based on the provided model name.
    """
    if model is None:
        model = "gpt-3.5-turbo"

    return ChatOpenAI(
        model=model, temperature=0.0, max_tokens=1000, max_retries=3, request_timeout=60
    )
