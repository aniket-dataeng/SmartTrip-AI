# Stage 1: Build Frontend
FROM node:20 AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Stage 2: Backend & final image
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY execution/ ./execution/
COPY directives/ ./directives/

# Copy built frontend to the expected location
# api_server.py expects ../frontend/dist/
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Expose port (Cloud Run defaults to 8080)
EXPOSE 8080

# Run the server
CMD ["uvicorn", "execution.api_server:app", "--host", "0.0.0.0", "--port", "8080"]
