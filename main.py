from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from langchain_core.output_parsers import JsonOutputParser

# Define the FastAPI app
app = FastAPI()


# Define the request model
class PromptRequest(BaseModel):
    prompt: str


# Define the response model
class PromptResponse(BaseModel):
    response: str


def get_summary(prompt: str):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional document summarizer"},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Please summarize the following document briefly and clearly, highlighting the main points and main topics covered. Keep it as short as possible, focusing on the main idea, leaving out unnecessary information: {prompt}",
                    },
                ],
            },
        ],
    )

    message = response.choices[0].message.content
    total_token = response.usage.total_tokens
    parser = JsonOutputParser()
    print("total_token:", total_token)

    return message


@app.post("/summary", response_model=PromptResponse)
def run_prompt(request: PromptRequest):
    # Generate the summary for the given prompt
    response_text = get_summary(request.prompt)
    return {"response": response_text}
