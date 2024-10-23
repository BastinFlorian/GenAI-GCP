from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from config.cloud_sql import POOL
from config.config import ARENA_TABLE, RECORDS_TABLE, QUESTION_TABLE

app = FastAPI()

class EloUpdateRequest(BaseModel):
    model1_name: str
    model2_name: str
    result: str  # 'win', 'draw', or 'lose' for model1
    elo_type: str # 'elo', 'elo_llm', or 'elo_question'


class RecordRequest(BaseModel):
    model_1_name: str
    model_2_name: str
    preference: str  # 'win', 'lose', or 'draw'
    question: str
    answer_model_1: str
    answer_model_2: str


def compute_elo(current_elo, opponent_elo, result, k=32) -> int:
    expected_score = 1 / (1 + 10 ** ((opponent_elo - current_elo) / 400))
    if result == 'win':
        score = 1
    elif result == 'draw':
        score = 0.5
    elif result == 'lose':
        score = 0
    else:
        raise ValueError("Invalid result value")
    new_elo = current_elo + k * (score - expected_score)
    return int(new_elo)

@app.post("/compute_new_elo")
def compute_new_elo(request: EloUpdateRequest):
    with POOL.connect() as db_conn:
        # Fetch current Elo ratings
        query = text(
            f"SELECT name, {request.elo_type} FROM {ARENA_TABLE} WHERE name IN (:model1_name, :model2_name)")
        result = db_conn.execute(
            query, {"model1_name": request.model1_name, "model2_name": request.model2_name}).fetchall()
        if len(result) != 2:
            raise HTTPException(status_code=404, detail="One or both models not found")

        model1_elo = None
        model2_elo = None
        for row in result:
            if row[0] == request.model1_name:
                model1_elo = row[1]
            elif row[0] == request.model2_name:
                model2_elo = row[1]

        if model1_elo is None or model2_elo is None:
            raise HTTPException(status_code=404, detail="One or both models not found")

        # Compute new Elo ratings
        new_model1_elo = compute_elo(model1_elo, model2_elo, request.result)
        new_model2_elo = compute_elo(model2_elo, model1_elo, 'win' if request.result == 'lose' else 'lose' if request.result == 'win' else 'draw')

        # Update Elo ratings in the database
        update_query = text(
            f"UPDATE {ARENA_TABLE} SET {request.elo_type} = :elo WHERE name = :name")
        db_conn.execute(
            update_query, {"elo": new_model1_elo, "name": request.model1_name})
        db_conn.execute(
            update_query, {"elo": new_model2_elo, "name": request.model2_name})
        db_conn.commit()

        return {"message": "Elo ratings updated successfully", "model1_new_elo": new_model1_elo, "model2_new_elo": new_model2_elo}

@app.get("/select_two_random_models_with_host")
def select_two_random_models_with_host():
    with POOL.connect() as db_conn:
        query = text(
            f"SELECT name, host FROM {ARENA_TABLE} ORDER BY RANDOM() LIMIT 2")
        result = db_conn.execute(query).fetchall()
        if len(result) != 2:
            raise HTTPException(status_code=404, detail="Not enough models found")
        return [{"name": row[0], "host": row[1]} for row in result]


@app.get("/get_model_ranking")
def get_model_ranking():
    with POOL.connect() as db_conn:
        query = text(
            f"SELECT name, elo, elo_llm, elo_question FROM {ARENA_TABLE} ORDER BY elo DESC")
        result = db_conn.execute(query).fetchall()
        return [{"name": row[0], "elo": row[1], "elo_llm": row[2], "elo_question": row[3]} for row in result]

@app.post("/record_result")
def record_result(request: RecordRequest):
    with POOL.connect() as db_conn:
        insert_query = text(
            f"INSERT INTO {RECORDS_TABLE} (model_1_name, model_2_name, preference, question, answer_model_1, answer_model_2) "
            "VALUES (:model_1_name, :model_2_name, :preference, :question, :answer_model_1, :answer_model_2)"
        )
        db_conn.execute(insert_query, {
            "model_1_name": request.model_1_name,
            "model_2_name": request.model_2_name,
            "preference": request.preference,
            "question": request.question,
            "answer_model_1": request.answer_model_1,
            "answer_model_2": request.answer_model_2
        })
        db_conn.commit()
        return {"message": "Result recorded successfully"}

@app.get("/get_random_question")
def get_random_question():
    with POOL.connect() as db_conn:
        # Select a random question
        query = text(f"SELECT question, count FROM {QUESTION_TABLE} ORDER BY RANDOM() LIMIT 1")
        result = db_conn.execute(query).fetchone()
        if result is None:
            raise HTTPException(status_code=404, detail="No questions found")

        question, count = result

        # Update the count
        update_query = text(f"UPDATE {QUESTION_TABLE} SET count = :count WHERE question = :question")
        db_conn.execute(update_query, {"count": count + 1, "question": question})
        db_conn.commit()

        return {"question": question}