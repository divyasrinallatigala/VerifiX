# --- Stage 1: Build the React frontend ---
FROM node:20-slim AS build-stage
WORKDIR /app/verifyx
COPY verifyx/package*.json ./
RUN npm install
COPY verifyx/ ./
RUN npm run build

# --- Stage 2: Serve the application with Python/Flask ---
FROM python:3.11-slim
ENV PYTHONUNBUFFERED True
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Copy built frontend assets from stage 1 to the 'static' folder
# Flask is configured to serve from 'static' folder in Vision/app.py
COPY --from=build-stage /app/verifyx/dist ./static

# Run the web service on container startup.
CMD exec python Vision/app.py
