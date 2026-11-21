# DSPy Building AI Agents

Tutorial at https://dspy.ai/tutorials/customer_service_agent/

## Requirements

This project uses Python 3.15, DSPy 3.5, and MLflow 3.18. Install the locked dependencies:

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

On subsequent runs, you can call the runner:

```bash
uv run src/runner.py --name Bob # defaults to version=1
uv run src/optimizer.py # version is now 2
uv run src/runner.py --name David --version 2
uv run src/runner.py --name Sally
uv run src/optimizer.py # version is now 3
uv run src/runner.py --name Adam --version 3
```

Notice that the code is just loading the model and running it!

## DSPy 3.5 migration notes

DSPy 3.5 replaces the old ReAct implementation with the structured-history version.
The `dspy.ReAct` constructor is unchanged, but these details are different:

- Results contain `history` and `termination_reason`, not `trajectory`.
- The agent uses a typed `submit` tool instead of a separate output extractor.
- `max_iters` counts model turns, not individual tool calls.
- XML is the default adapter. OpenAI models use the Responses API by default.

You must run `src/optimizer.py` again to create a new model version. Do not use a
registered model version created with DSPy 3.4 or earlier. Pass the new version
number to `src/runner.py` with `--version`.

MLflow 3.18 logs new models with DSPy's built-in model save format.

## Development checks

Run the linter, formatter check, and type checker:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check
```

Format the code with `uv run ruff format .`.

As an aside, if you go to the directory where MLflow is running, you
should be able to see the HTTP calls and the sqlite database.

