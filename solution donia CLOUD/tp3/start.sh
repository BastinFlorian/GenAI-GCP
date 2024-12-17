#!/bin/sh
# Start Streamlit with the environment variable PORT
streamlit run app.py --server.port=${PORT} --server.address=0.0.0.0
