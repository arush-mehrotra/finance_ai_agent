#!/bin/bash
# Test runner script for Finance AI Agent

# Set the project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PYTHONPATH="$PROJECT_ROOT"

# Activate virtual environment if it exists
if [ -d "$PROJECT_ROOT/.venv" ]; then
    source "$PROJECT_ROOT/.venv/bin/activate"
fi

# Parse command line argument
TEST_TYPE="${1:-all}"

case "$TEST_TYPE" in
    stock)
        echo "Running stock service tests..."
        python backend/tests/test_stock_service.py
        ;;
    news)
        echo "Running news service tests..."
        python backend/tests/test_news_service.py
        ;;
    ai)
        echo "Running AI agent tests..."
        python backend/tests/test_ai_agent.py
        ;;
    all)
        echo "Running all tests..."
        echo ""
        python backend/tests/test_stock_service.py
        echo ""
        echo "================================"
        echo ""
        python backend/tests/test_news_service.py
        echo ""
        echo "================================"
        echo ""
        python backend/tests/test_ai_agent.py
        ;;
    *)
        echo "Usage: ./run_tests.sh [stock|news|ai|all]"
        echo "  stock - Run stock service tests only"
        echo "  news  - Run news service tests only"
        echo "  ai    - Run AI agent tests only"
        echo "  all   - Run all tests (default)"
        exit 1
        ;;
esac
