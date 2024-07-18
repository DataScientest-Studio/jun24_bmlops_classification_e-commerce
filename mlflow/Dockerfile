# MLflow Dockerfile
FROM python:3.9-slim

# Install MLflow
RUN pip install mlflow

# Expose the port
EXPOSE 5000

# Command to run MLflow
CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000"]
