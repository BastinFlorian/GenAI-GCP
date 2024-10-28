import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI,HarmCategory,HarmBlockThreshold
from langchain_core.prompts import ChatPromptTemplate
#from langchain.prompts import PromptTemplate
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()

api_key = os.environ.get('GOOGLE_API_KEY')

class UserInput(BaseModel):
    question: str
    temperature: float  
    language: str



@app.post("/answer")
def answer(user_input: UserInput):
    '''
    This fuction ...


    Args

        '''

    gemini_model = ChatGoogleGenerativeAI(
        api_key=api_key, 
        model=" ",
        temperature = user_input.temperature,
        safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
)

    chat = ChatPromptTemplate.from_messages([
   ("system","You are a helpful AI Assistant with a sense of humor"),
   ("human","{input}")
])
    chat1= chat.format_messages(input=f"The user asked the question: {user_input.question} in {user_input.language}.")
    #chat1= chat.format_messages(input=user_input.question)



    try:
        print(f"Received request: {user_input}")

        response = gemini_model.invoke(chat1) 

        print(f"Response from model: {response}")

        return {"message": response.content}

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")
