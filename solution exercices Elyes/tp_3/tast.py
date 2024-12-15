from google.ai.generativelanguage_v1beta3 import ModelServiceClient

def list_models():
    # Spécifiez la clé API
    api_key = "AIzaSyA0BJ-l4g5TYK-Gd0fvK6lJMUIroDsr1rI"
    
    # Créer un client avec la clé API
    client = ModelServiceClient(
        client_options={"api_key": api_key}
    )
    
    # Appeler l'API pour lister les modèles
    response = client.list_models()
    for model in response.models:
        print(f"Model ID: {model.name}, Display Name: {model.display_name}")

list_models()
