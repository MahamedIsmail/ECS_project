FROM  python:3.16.0a1-slim-trixie

WORKDIR /app

COPY requirements.txt ./ 

RUN pip install -r requirements.txt

COPY . .
HEALTHCHECK --timeout=30s --interval=30s --retries= --start-period= --start-interval=5s \
CMD curl  localhost:3000/Health 
# Make sure the application runs in unbuffered mode, so that logs are output immediately.
ENV PYTHONUNBUFFERED=1   


CMD ["flask","--app", "./app/main.py", "run","--host=0.0.0.0","--debug"] 


# remove --debug in production, and run wiht gunicorn or waitress for production deployment.
