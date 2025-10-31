# DSPy Building AI Agents

Tutorial at https://dspy.ai/tutorials/customer_service_agent/

To Run, you first need to add your OPENAPI key to a `.env` file.

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

As an aside, if you go to the directory where MLflow is running, you
should be able to see the HTTP calls and the sqlite database.

