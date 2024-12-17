from langchain_google_genai import ChatGoogleGenerativeAI
print("Début du script")

# Remplacez "votre_clé_API" par votre clé API Google Generative AI
api_key = "AIzaSyA0BJ-l4g5TYK-Gd0fvK6lJMUIroDsr1rI"  # Remplacez par votre clé API valide
try:
    # Ajoutez le champ `model` requis
    chat_model = ChatGoogleGenerativeAI(api_key=api_key, model="chat-bison-001")
    print("Le modèle a été créé avec succès.")
    
    # Testez une requête simple
    response = chat_model.generate(messages=["Hello, how are you?"])
    print("Réponse générée :", response)
except Exception as e:
    print("Une erreur s'est produite :", e)

print("Fin du script")
