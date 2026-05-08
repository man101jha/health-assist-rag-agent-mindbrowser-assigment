# Stage 1: Build Angular
FROM node:20-alpine as build-stage
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
# Angular 17+ uses 'browser' subfolder in dist
RUN npm run build

# Stage 2: Setup Python & Serve
FROM python:3.12-slim
WORKDIR /app

# Memory optimization for 512MB RAM
ENV MALLOC_ARENA_MAX=2
ENV OMP_NUM_THREADS=1
ENV TORCH_NUM_THREADS=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Copy built frontend from stage 1
# Note: Adjust path if your project name is different
COPY --from=build-stage /app/frontend/dist/health-assistant-ui/browser ./static

# Ensure data directory exists for ingestion
RUN mkdir -p data
COPY backend/data/ ./data/

# Environment variables (Defaults)
ENV PORT=8001

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
