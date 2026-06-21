web: streamlit run ui/app.py --server.port $PORT --server.address 0.0.0.0
api: gunicorn --bind 0.0.0.0:$PORT src.api:app --workers 2 --timeout 120
