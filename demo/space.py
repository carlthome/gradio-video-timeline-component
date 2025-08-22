import gradio as gr
from app import demo as app
import os

_docs = {
    "TimelineComponent": {
        "description": "A component to display an audio/video timeline.",
        "members": {
            "__init__": {
                "value": {
                    "type": "dict | Callable | None",
                    "default": "None",
                    "description": "A dictionary representing the timeline data.",
                },
                "label": {
                    "type": "str | I18nData | None",
                    "default": "None",
                    "description": "The label for this component.",
                },
                "every": {
                    "type": "Timer | float | None",
                    "default": "None",
                    "description": "Continuously calls `value` to recalculate it if `value` is a",
                },
                "inputs": {
                    "type": "Component | Sequence[Component] | set[Component] | None",
                    "default": "None",
                    "description": "Components that are used as inputs to calculate `value` if",
                },
                "show_label": {
                    "type": "bool | None",
                    "default": "None",
                    "description": "If True, will display label.",
                },
                "scale": {
                    "type": "int | None",
                    "default": "None",
                    "description": "Relative size compared to adjacent Components.",
                },
                "min_width": {
                    "type": "int",
                    "default": "160",
                    "description": "Minimum pixel width.",
                },
                "interactive": {
                    "type": "bool | None",
                    "default": "None",
                    "description": "If True, the timeline will be interactive.",
                },
                "visible": {
                    "type": "bool",
                    "default": "True",
                    "description": "If False, component will be hidden.",
                },
                "elem_id": {
                    "type": "str | None",
                    "default": "None",
                    "description": "An optional string that is assigned as the id of this",
                },
                "elem_classes": {
                    "type": "list[str] | str | None",
                    "default": "None",
                    "description": "An optional list of strings that are assigned as the",
                },
                "render": {
                    "type": "bool",
                    "default": "True",
                    "description": "If False, component will not be rendered in the Blocks",
                },
                "key": {
                    "type": "int | str | tuple[int | str, ...] | None",
                    "default": "None",
                    "description": "A key to identify the component across re-renders.",
                },
                "preserved_by_key": {
                    "type": "list[str] | str | None",
                    "default": '"value"',
                    "description": "A list of parameters to preserve across",
                },
            },
            "postprocess": {
                "value": {
                    "type": "dict | None",
                    "description": "The timeline data from the backend.",
                }
            },
            "preprocess": {
                "return": {
                    "type": "dict | None",
                    "description": "The timeline data as a dictionary.",
                },
                "value": None,
            },
        },
        "events": {
            "change": {
                "type": None,
                "default": None,
                "description": "Triggered when the value of the TimelineComponent changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.",
            }
        },
    },
    "__meta__": {
        "additional_interfaces": {},
        "user_fn_refs": {"TimelineComponent": []},
    },
}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
        """
# `gradio_timelinecomponent`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">
</div>

Audio/video timeline
""",
        elem_classes=["md-custom"],
        header_links=True,
    )
    app.render()
    gr.Markdown(
        """
## Installation

```bash
pip install gradio_timelinecomponent
```

## Usage

```python
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

```
""",
        elem_classes=["md-custom"],
        header_links=True,
    )

    gr.Markdown(
        """
## `TimelineComponent`

### Initialization
""",
        elem_classes=["md-custom"],
        header_links=True,
    )

    gr.ParamViewer(value=_docs["TimelineComponent"]["members"]["__init__"], linkify=[])

    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["TimelineComponent"]["events"], linkify=["Event"])

    gr.Markdown(
        """

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, the timeline data as a dictionary.
- **As output:** Should return, the timeline data from the backend.

 ```python
def predict(
    value: dict | None
) -> dict | None:
    return value
```
""",
        elem_classes=["md-custom", "TimelineComponent-user-fn"],
        header_links=True,
    )

    demo.load(
        None,
        js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          TimelineComponent: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""",
    )

demo.launch()
