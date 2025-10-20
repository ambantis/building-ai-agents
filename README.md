# DSPy Building AI Agents

Tutorial at https://dspy.ai/tutorials/customer_service_agent/

To Run, you first need to add your OPENAPI key to a `.env` file.

Next, start MLflow:

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db --port 5000
```

Next, run the "optimizer":

```bash
uv run src/optimizer.py
```

This will run the application and upload the model to MLflow.

On subsequent runs, you can call the runner:

```bash
uv run src/runner.py --name David --version 1
```

Notice that the code is just loading the model and running it!

As an aside, if you go to the directory where MLflow is running, you
should be able to see the HTTP calls and the sqlite database.

Note that exporting the model to MLflow requires the presence of a `requirements.txt`.
If you need to update dependencies, be sure to update it as well:

```bash
uv pip compile pyproject.toml -o requirements.txt
```
