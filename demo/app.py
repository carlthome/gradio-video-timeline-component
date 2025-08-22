import os
import sys

import gradio as gr
from gradio_timelinecomponent import TimelineComponent

custom_example = {
    "video": [
        {
            "id": "v1",
            "src": "https://www.w3schools.com/html/mov_bbb.mp4",
            "start": 1,
            "duration": 4,
        },
        {
            "id": "v2",
            "src": "https://www.w3schools.com/html/mov_bbb.mp4",
            "start": 7,
            "duration": 5,
        },
    ],
    "audio": [
        {
            "id": "a1",
            "src": "https://www.w3schools.com/html/horse.mp3",
            "start": 0,
            "duration": 5,
            "lane": 0,
        },
        {
            "id": "a2",
            "src": "https://www.w3schools.com/html/horse.mp3",
            "start": 5.5,
            "duration": 3,
            "lane": 1,
        },
        {
            "id": "a3",
            "src": "https://www.w3schools.com/html/horse.mp3",
            "start": 9,
            "duration": 2,
            "lane": 0,
        },
    ],
}


with gr.Blocks() as demo:
    gr.Markdown(
        "Drag and resize the audio or video clips to change their start times "
        "and durations."
    )
    TimelineComponent(
        value=custom_example, label="Interactive Timeline", interactive=True
    )


if __name__ == "__main__":
    demo.launch()
