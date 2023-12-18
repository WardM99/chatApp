# Backend

## While developing

if want to run the backend without Docker for developing reasons

```console
# Navigate to the backend directory
cd backend

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Poetry
pip3 install poetry

# Install all dependencies and dev dependencies
poetry install

# Run uvicorn
uvicorn src.app.app:app --reload
```
