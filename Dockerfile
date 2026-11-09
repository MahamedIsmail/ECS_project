FROM  python:3.15.2-trixie

WORKDIR /app

COPY requirements.txt ./ 

RUN pip install -r requirements.txt

COPY . .
HEALTHCHECK --timeout=30s --interval=15s --retries=3 \
CMD curl  localhost:80/Health 
# Make sure the application runs in unbuffered mode, so that logs are output immediately.
ENV PYTHONUNBUFFERED=1   


CMD ["flask","--app", "./app/main.py", "run","--host=0.0.0.0"] 


# remove --debug in production, and run wiht gunicorn or waitress for production deployment.
