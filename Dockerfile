# Set the base image to use
FROM python:3.10.6

# Set an environment variable
ENV PYTHONUNBUFFERED 1

# Install Poetry package manager
RUN pip install poetry

# Copy the current directory contents into the container at /code/
COPY . /code/

# Set the working directory to /code/
WORKDIR /code

# Install project dependencies using Poetry
RUN poetry install --no-root --no-interaction --no-ansi

# Expose port 8000
EXPOSE 8000

# Set the default command to run when the container starts
CMD poetry run python manage.py runserver 0.0.0.0:8000
