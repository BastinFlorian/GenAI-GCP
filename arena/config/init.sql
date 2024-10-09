"""Create the arena database schema."""

CREATE TABLE records (
    model_1_name VARCHAR(255),
    model_2_name VARCHAR(255),
    preference VARCHAR(6),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    question TEXT,
    answer_model_1 TEXT,
    answer_model_2 TEXT
);

CREATE TABLE arena (
    name VARCHAR(255),
    host VARCHAR(255),
    elo INT DEFAULT 1000,
    elo_llm INT DEFAULT 1000,
    elo_question INT DEFAULT 1000
);

CREATE TABLE question (
    question TEXT,
    answer TEXT,
    count INT DEFAULT 1
);