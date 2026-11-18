FROM  python:3.13-slim-trixie as Build_stage

WORKDIR /app

COPY requirements.txt ./ 

RUN pip install --no-cache-dir -r requirements.txt 

COPY /app .

 



From gcr.io/distroless/python3-debian13:nonroot

WORKDIR /app

COPY --from=Build_stage /usr/local/lib/python3.13/site-packages /python_packages

EXPOSE 80

COPY --from=Build_stage  /app   .

# Tells my python application where to find the packages installed in the build stage. So i dont have figure out the path to site-packages in the distroless image.
ENV PYTHONPATH=/python_packages

HEALTHCHECK --timeout=30s --interval=15s --retries=3 \
CMD [ "python","Healthchecker.py" ]

# Enterypoint is python3 , cmd is argument to python3, so we can run python3 -m gunicorn --access-logfile= etc .. 
# gunicorn enterypoint did not work with distroless image beacse i could find the gunicorn path in the distroless image. So we run gunicorn as a module with python3 -m gunicorn.

CMD ["-m", "gunicorn", "--access-logfile=-","-b"," 0.0.0.0:80","main:app"] 


# remove --debug in production, and run wiht gunicorn or waitress for production deployment.
# change to distroless python image for production deployment.
