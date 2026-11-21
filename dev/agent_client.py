import os

import gradio as gr
import httpx
from dotenv import load_dotenv

load_dotenv()

DEFAULT_REQUEST = "Please help me book a flight from SFO to JFK on 09/01/2025."
REQUEST_TIMEOUT_SECONDS = 120.0


def create_gradio_app(api_base_url: str) -> gr.Blocks:
    """Create a Gradio client for the FastAPI agent endpoint."""

    def submit_request(traveler_name: str, user_request: str) -> str:
        response = httpx.post(
            f"{api_base_url}/v1/travel-requests",
            json={
                "traveler_name": traveler_name,
                "user_request": user_request,
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()["process_result"]

    with gr.Blocks(title="Airline Customer Service") as demo:
        gr.Markdown(
            "# Airline Customer Service\nAsk the agent to book or manage a flight."
        )
        traveler_name = gr.Textbox(
            label="Traveler name",
            value="Bob",
            max_lines=1,
        )
        user_request = gr.Textbox(
            label="Request",
            value=DEFAULT_REQUEST,
            lines=6,
            max_lines=12,
        )
        submit_button = gr.Button("Submit", variant="primary")
        process_result = gr.Textbox(
            label="Agent response",
            lines=8,
            interactive=False,
        )
        submit_button.click(
            fn=submit_request,
            inputs=[traveler_name, user_request],
            outputs=process_result,
            api_name="submit_request",
        )

    return demo


def main() -> None:
    """Start the standalone development client."""
    demo = create_gradio_app(os.getenv("API_BASE_URL", "http://127.0.0.1:8000"))
    demo.launch(
        server_name=os.getenv("GRADIO_HOST", "127.0.0.1"),
        server_port=int(os.getenv("GRADIO_PORT", "7860")),
        show_error=False,
    )


if __name__ == "__main__":
    main()
