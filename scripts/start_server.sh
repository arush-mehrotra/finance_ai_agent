#!/bin/bash
# Start the Finance AI Agent API server

# Set the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="$PROJECT_ROOT"

# Activate virtual environment if it exists
if [ -d "$PROJECT_ROOT/.venv" ]; then
    source "$PROJECT_ROOT/.venv/bin/activate"
fi

# Check if .env file exists
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "   Please create .env file from .env.example"
    echo "   and add your API keys"
    exit 1
fi

# Start the server
echo "Starting Finance AI Agent API..."
echo "API Documentation will be available at:"
echo "  - Swagger UI: http://localhost:8000/docs"
echo "  - ReDoc: http://localhost:8000/redoc"
echo ""

python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
