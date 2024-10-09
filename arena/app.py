"""
Module for interacting with ELO rating models and updating their ratings.
"""

import os
from re import sub
import pandas as pd
import requests
import gradio as gr
from api import EloUpdateRequest

HOST = "https://arena-api-1021317796643.europe-west1.run.app"
# HOST = "http://0.0.0.0:8181"

def get_elo_data():
    response = requests.get(os.path.join(HOST, 'get_model_ranking'))
    if response.status_code == 200:
        return response.json()
    else:
        st.error('Failed to fetch data from API')
        return None

def get_random_models():
    """
    Function to get ELO data from the API.
    """
    response = requests.get(os.path.join(HOST, 'select_two_random_models_with_host'), timeout=30)
    if response.status_code == 200:
        return response.json()
    return None


def get_random_question():
    """
    Function to get ELO data from the API.
    """
    response = requests.get(os.path.join(
        HOST, 'get_random_question'), timeout=30)
    if response.status_code == 200:
        return response.json()["question"], gr.update(visible=True)
    return None


def get_answer(host: str, question: str):
    """
    Function to get an answer from a model.
    """
    temperature = 0.1
    language = "English"
    return requests.post(
        os.path.join(host, "answer"),
        json={
            "question": question,
            "temperature": temperature,
            "language": language
        },
        timeout=30
    )


def update_elo(request: EloUpdateRequest):
    """
    Function to update ELO ratings.
    """
    response = requests.post(
        os.path.join(HOST, "compute_new_elo"),
        json=request.model_dump(),
        timeout=30
    )
    if response.status_code == 200:
        return "ELO ratings updated successfully"
    return f"Failed to update ELO ratings: {response.text}"


def record_results(model1_name: str, model2_name: str, result: str, question: str, answer_model_1: str, answer_model_2: str):
    """
    Function to record the results of a comparison between two models.
    """
    response = requests.post(
        os.path.join(HOST, "record_result"),
        json={
            "model_1_name": model1_name,
            "model_2_name": model2_name,
            "preference": result,
            "question": question,
            "answer_model_1": answer_model_1,
            "answer_model_2": answer_model_2
        },
        timeout=30
    )
    if response.status_code == 200:
        return "Results recorded successfully"
    return f"Failed to record results: {response.text}"


def ask_random_question(random_question):
    print(random_question)
    if random_question:
        answer1, answer2, random_models_data, pref_update, submit_update = ask_question(
            random_question)
        return gr.update(value=random_question), answer1, answer2, random_models_data, pref_update, submit_update
    return gr.update(value="Failed to fetch random question"), "", "", "", gr.update(visible=False), gr.update(visible=False)


def ask_question(question):
    """
    Function to ask a question to two random models and get their answers.
    """
    random_models = get_random_models()
    if not random_models:
        return "Failed to fetch data from API", "", "", "", ""

    response1 = get_answer(random_models[0]["host"], question)
    response2 = get_answer(random_models[1]["host"], question)

    if response1.status_code == 200:
        answer1 = response1.json()["message"]
    else:
        answer1 = f"Error: {response1.text}"

    if response2.status_code == 200:
        answer2 = response2.json()["message"]
    else:
        answer2 = f"Error: {response2.text}"

    return answer1, answer2, random_models, gr.update(visible=True), gr.update(visible=True)


def validate_preference(preference, random_models, question, answer1, answer2, elo_type):
    """
    Function to validate the user's preference and update ELO ratings accordingly.
    """
    if preference == "👈 Left":
        result = "win"
    elif preference == "Right 👉":
        result = "lose"
    elif preference == "Equal":
        result = "draw"

    # Update ELO ratings
    update_elo(EloUpdateRequest(
        model1_name=random_models[0]["name"],
        model2_name=random_models[1]["name"],
        result=result,
        elo_type=elo_type
    ))

    # Record the results
    record_results(
        model1_name=random_models[0]["name"],
        model2_name=random_models[1]["name"],
        result=result,
        question=question,
        answer_model_1=answer1,
        answer_model_2=answer2
    )

    # Clear the question input
    gr.Info("ELO ratings updated and results recorded successfully")
    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(value=""), gr.update(visible=False)


with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.TabItem("Rate Chatbots with you own questions"):
            elo_type = gr.Textbox(label="ELO type", value="elo", visible=False)
            question = gr.Textbox(label="What is your question?")
            submit_question = gr.Button("Ask question")

            with gr.Row():
                with gr.Column():
                    model1_answer = gr.Markdown(label="Model 1 Answer")
                with gr.Column():
                    model2_answer = gr.Markdown(label="Model 2 Answer")


            preference = gr.Radio(
                label="Which model do you prefer?",
                choices=["👈 Left", "Equal", "Right 👉"],
                visible=False
            )
            random_models = gr.State()

            submit_preference = gr.Button("Validate preference", visible=False)

            submit_question.click(
                ask_question,
                inputs=question,
                outputs=[model1_answer, model2_answer, random_models, preference, submit_preference]
            )

            submit_preference.click(
                validate_preference,
                inputs=[preference, random_models, question,
                        model1_answer, model2_answer, elo_type],
                outputs=[model1_answer, model2_answer,
                            preference, question, submit_preference]
            )

        with gr.TabItem("Rate Chatbots with random questions"):
            elo_type = gr.Textbox(
                label="ELO type", value="elo_question", visible=False)

            question = gr.Markdown(label="Random Question")
            get_question = gr.Button("Generate Question")
            button_ask_question = gr.Button("Get answers", visible=False)

            with gr.Row():
                with gr.Column():
                    model1_answer = gr.Markdown(label="Model 1 Answer")
                with gr.Column():
                    model2_answer = gr.Markdown(label="Model 2 Answer")

            preference = gr.Radio(
            label="Which model do you prefer?",
            choices=["👈 Left", "Equal", "Right 👉"],
            visible=False
            )
            random_models = gr.State()

            submit_preference = gr.Button("Validate preference", visible=False)
            get_question.click(get_random_question, outputs=[question, button_ask_question])

            button_ask_question.click(
                ask_random_question,
                inputs=[question],
                outputs=[question, model1_answer, model2_answer, random_models, preference, submit_preference]
            )

            submit_preference.click(
            validate_preference,
                inputs=[preference, random_models, question,
                        model1_answer, model2_answer, elo_type],
            outputs=[model1_answer, model2_answer, preference, question, submit_preference]
            )

        with gr.TabItem("Chatbot Ranking"):
            ranking = gr.Dataframe(headers=["Model Name", "Students questions ELO", "Template questions ELO", "LLM ELO"], datatype=["str", "number", "number", "number"])

            def display_ranking():
                elo_data = get_elo_data()
                if elo_data:
                    formatted_data = pd.DataFrame([{
                        "Model Name": model["name"],
                        "Students questions ELO": model["elo"],
                        "Template questions ELO": model["elo_question"],
                        "LLM ELO": model["elo_llm"]
                    } for model in elo_data])
                    return formatted_data
                return pd.DataFrame(columns=["Model Name", "Students questions ELO", "Template questions ELO", "LLM ELO"])

            gr.Button("Refresh Ranking").click(
                display_ranking,
                outputs=ranking
            )


# Launch the Gradio app
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8080)
