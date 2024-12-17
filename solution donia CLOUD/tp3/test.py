# Importation des bibliothèques nécessaires pour LangChain et Google Generative AI
from langchain.chat_models import ChatGoogleGenerativeAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage

# Testez chaque importation pour vérifier qu'elle fonctionne
def test_imports():
    print("Début du test des importations...\n")

    try:
        print("Importation réussie pour : ChatGoogleGenerativeAI")
        chat_model = ChatGoogleGenerativeAI(api_key="your_api_key_here")
    except ImportError as e:
        print(f"Erreur d'importation : ChatGoogleGenerativeAI : {e}")

    try:
        print("Importation réussie pour : ChatPromptTemplate et sous-classes")
        system_prompt = SystemMessagePromptTemplate.from_template(
            "You are a helpful assistant."
        )
        human_prompt = HumanMessagePromptTemplate.from_template("{input}")
        prompt_template = ChatPromptTemplate.from_messages([system_prompt, human_prompt])
    except ImportError as e:
        print(f"Erreur d'importation : ChatPromptTemplate et sous-classes : {e}")

    try:
        print("Importation réussie pour : AIMessage, HumanMessage, SystemMessage")
        ai_message = AIMessage(content="This is a message from the AI.")
        human_message = HumanMessage(content="This is a message from a human.")
        system_message = SystemMessage(content="This is a system message.")
    except ImportError as e:
        print(f"Erreur d'importation : AIMessage, HumanMessage, SystemMessage : {e}")

    print("\nTest des importations terminé.")


if __name__ == "__main__":
    test_imports()

