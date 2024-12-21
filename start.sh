#!/bin/sh
cd backend
# gunicorn -w 4 -b 0.0.0.0:5000 app:app &
python -u app.py &
cd ../frontend
node server.js 
