---
tags: [gradio-custom-component, SimpleTextbox]
title: gradio_timelinecomponent
short_description: Audio/video timeline
colorFrom: blue
colorTo: yellow
sdk: gradio
pinned: false
app_file: space.py
---

# `gradio_timelinecomponent`
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">

Audio/video timeline

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

## `TimelineComponent`

### Initialization

<table>
<thead>
<tr>
<th align="left">name</th>
<th align="left" style="width: 25%;">type</th>
<th align="left">default</th>
<th align="left">description</th>
</tr>
</thead>
<tbody>
<tr>
<td align="left"><code>value</code></td>
<td align="left" style="width: 25%;">

```python
dict | Callable | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">A dictionary representing the timeline data.</td>
</tr>

<tr>
<td align="left"><code>label</code></td>
<td align="left" style="width: 25%;">

```python
str | I18nData | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">The label for this component.</td>
</tr>

<tr>
<td align="left"><code>every</code></td>
<td align="left" style="width: 25%;">

```python
Timer | float | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Continuously calls `value` to recalculate it if `value` is a</td>
</tr>

<tr>
<td align="left"><code>inputs</code></td>
<td align="left" style="width: 25%;">

```python
Component | Sequence[Component] | set[Component] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Components that are used as inputs to calculate `value` if</td>
</tr>

<tr>
<td align="left"><code>show_label</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">If True, will display label.</td>
</tr>

<tr>
<td align="left"><code>scale</code></td>
<td align="left" style="width: 25%;">

```python
int | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">Relative size compared to adjacent Components.</td>
</tr>

<tr>
<td align="left"><code>min_width</code></td>
<td align="left" style="width: 25%;">

```python
int
```

</td>
<td align="left"><code>160</code></td>
<td align="left">Minimum pixel width.</td>
</tr>

<tr>
<td align="left"><code>interactive</code></td>
<td align="left" style="width: 25%;">

```python
bool | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">If True, the timeline will be interactive.</td>
</tr>

<tr>
<td align="left"><code>visible</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will be hidden.</td>
</tr>

<tr>
<td align="left"><code>elem_id</code></td>
<td align="left" style="width: 25%;">

```python
str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional string that is assigned as the id of this</td>
</tr>

<tr>
<td align="left"><code>elem_classes</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">An optional list of strings that are assigned as the</td>
</tr>

<tr>
<td align="left"><code>render</code></td>
<td align="left" style="width: 25%;">

```python
bool
```

</td>
<td align="left"><code>True</code></td>
<td align="left">If False, component will not be rendered in the Blocks</td>
</tr>

<tr>
<td align="left"><code>key</code></td>
<td align="left" style="width: 25%;">

```python
int | str | tuple[int | str, ...] | None
```

</td>
<td align="left"><code>None</code></td>
<td align="left">A key to identify the component across re-renders.</td>
</tr>

<tr>
<td align="left"><code>preserved_by_key</code></td>
<td align="left" style="width: 25%;">

```python
list[str] | str | None
```

</td>
<td align="left"><code>"value"</code></td>
<td align="left">A list of parameters to preserve across</td>
</tr>
</tbody></table>


### Events

| name | description |
|:-----|:------------|
| `change` | Triggered when the value of the TimelineComponent changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input. |



### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As output:** Is passed, the timeline data as a dictionary.
- **As input:** Should return, the timeline data from the backend.

 ```python
 def predict(
     value: dict | None
 ) -> dict | None:
     return value
 ```
