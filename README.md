# DSPy Building AI Agents

Tutorial at https://dspy.ai/tutorials/customer_service_agent/

## Requirements

This project uses Python 3.15, DSPy 3.5, MLflow 3.18, and FastAPI 0.165.
Gradio 6.32 is available as a development-only test client. Install the locked
dependencies:

```bash
uv sync --group dev
```

Add your OpenAI API key to a `.env` file. You can copy `.env.example` to start.

Next, start MLflow (in some other directory):

```bash
mlflow server --backend-store-uri sqlite:///data.db --port 5000
```

to start mlflow pointing to an absolute path on the file system:

```bash
mlflow server --backend-store-uri sqlite:////home/ambantis/dev/sandbox/mlflow/data.db --port 5000
```

Next, run the "optimizer":

```bash
uv run src/optimizer.py
```

This will run the application and upload the model to MLflow.

## Run the HTTP server

Set `MODEL_VERSION` to the registered model version and start the server:

```bash
MODEL_VERSION=1 uv run src/server.py
```

The server listens on `127.0.0.1:8000` by default. You can change `HOST` and
`PORT` in the environment.

Available interfaces:

- FastAPI documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

Send a request to the HTTP API:

```bash
curl --request POST http://127.0.0.1:8000/v1/travel-requests \
  --header 'Content-Type: application/json' \
  --data '{
    "traveler_name": "Bob",
    "user_request": "Please help me book a flight from SFO to JFK on 09/01/2025."
  }'
```

The response contains `process_result`, `termination_reason`, and
`model_version`.

### Development Gradio client

Gradio is not part of the FastAPI application. To start its standalone test UI,
keep the FastAPI server running and use another terminal:

```bash
uv run dev/agent_client.py
```

Open http://127.0.0.1:7860. The Gradio client sends every request to the FastAPI
`POST /v1/travel-requests` endpoint, so Pydantic performs all input validation.
Set `API_BASE_URL` if FastAPI uses another address. `GRADIO_HOST` and
`GRADIO_PORT` control the development UI listener.

The standalone Gradio app also exposes the named `submit_request` endpoint for
programmatic development tests:

```python
from gradio_client import Client

client = Client("http://127.0.0.1:7860")
result = client.predict(
    traveler_name="Bob",
    user_request="Please help me book a flight from SFO to JFK on 09/01/2025.",
    api_name="/submit_request",
)
print(result)
```

## DSPy 3.5 migration notes

DSPy 3.5 replaces the old ReAct implementation with the structured-history version.
The `dspy.ReAct` constructor is unchanged, but these details are different:

- Results contain `history` and `termination_reason`, not `trajectory`.
- The agent uses a typed `submit` tool instead of a separate output extractor.
- `max_iters` counts model turns, not individual tool calls.
- XML is the default adapter. OpenAI models use the Responses API by default.

You must run `src/optimizer.py` again to create a new model version. Do not use a
registered model version created with DSPy 3.4 or earlier. Set `MODEL_VERSION`
to the new version number before you start `src/server.py`.

MLflow 3.18 logs new models with DSPy's built-in model save format.

## Development checks

Run the linter, formatter check, and type checker:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
uv run pytest
```

Format the code with `uv run ruff format .`.

As an aside, if you go to the directory where MLflow is running, you
should be able to see the HTTP calls and the sqlite database.

