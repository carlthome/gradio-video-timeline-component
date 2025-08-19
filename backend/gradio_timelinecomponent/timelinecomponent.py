from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any

from gradio.components.base import Component, FormComponent
from gradio.events import Events
from gradio.i18n import I18nData

if TYPE_CHECKING:
    from gradio.components import Timer


class TimelineComponent(FormComponent):
    """
    A component to display an audio/video timeline.
    """

    EVENTS = [
        Events.change,
    ]

    def __init__(
        self,
        value: dict | Callable | None = None,
        *,
        label: str | I18nData | None = None,
        every: Timer | float | None = None,
        inputs: Component | Sequence[Component] | set[Component] | None = None,
        show_label: bool | None = None,
        scale: int | None = None,
        min_width: int = 160,
        interactive: bool | None = None,
        visible: bool = True,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | tuple[int | str, ...] | None = None,
        preserved_by_key: list[str] | str | None = "value",
    ):
        """
        Parameters:
            value: A dictionary representing the timeline data.
            label: The label for this component.
            every: Continuously calls `value` to recalculate it if `value` is a
                function.
            inputs: Components that are used as inputs to calculate `value` if
                `value` is a function.
            show_label: If True, will display label.
            scale: Relative size compared to adjacent Components.
            min_width: Minimum pixel width.
            interactive: If True, the timeline will be interactive.
            visible: If False, component will be hidden.
            elem_id: An optional string that is assigned as the id of this
                component in the HTML DOM.
            elem_classes: An optional list of strings that are assigned as the
                classes of this component in the HTML DOM.
            render: If False, component will not be rendered in the Blocks
                context.
            key: A key to identify the component across re-renders.
            preserved_by_key: A list of parameters to preserve across
                re-renders.
        """
        super().__init__(
            label=label,
            every=every,
            inputs=inputs,
            show_label=show_label,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            value=value,
            render=render,
            key=key,
            preserved_by_key=preserved_by_key,
        )

    def preprocess(self, payload: dict | None) -> dict | None:
        """
        Parameters:
            payload: The timeline data from the frontend.
        Returns:
            The timeline data as a dictionary.
        """
        return payload

    def postprocess(self, value: dict | None) -> dict | None:
        """
        Parameters:
            value: The timeline data from the backend.
        Returns:
            The timeline data to be sent to the frontend.
        """
        return value

    def api_info(self) -> dict[str, Any]:
        return {"type": "object"}

    def example_payload(self) -> Any:
        return {
            "video": [
                {
                    "id": "v1",
                    "src": "https://www.w3schools.com/html/mov_bbb.mp4",
                    "start": 0,
                    "duration": 5,
                },
                {
                    "id": "v2",
                    "src": "https://www.w3schools.com/html/mov_bbb.mp4",
                    "start": 6,
                    "duration": 4,
                },
            ],
            "audio": [
                {
                    "id": "a1",
                    "src": "https://www.w3schools.com/html/horse.mp3",
                    "start": 1,
                    "duration": 8,  # clipped by audio file's actual duration
                    "lane": 0,
                },
                {
                    "id": "a2",
                    "src": "https://www.w3schools.com/html/horse.mp3",
                    "start": 3,
                    "duration": 2,
                    "lane": 1,
                },
                {
                    "id": "a3",
                    "src": "https://www.w3schools.com/html/horse.mp3",
                    "start": 7,
                    "duration": 3,
                    "lane": 0,
                },
            ],
        }

    def example_value(self) -> Any:
        return {
            "video": [
                {
                    "id": "v1",
                    "src": "https://www.w3schools.com/html/mov_bbb.mp4",
                    "start": 0,
                    "duration": 5,
                },
                {
                    "id": "v2",
                    "src": "https://www.w3schools.com/html/mov_bbb.mp4",
                    "start": 6,
                    "duration": 4,
                },
            ],
            "audio": [
                {
                    "id": "a1",
                    "src": "https://www.w3schools.com/html/horse.mp3",
                    "start": 1,
                    "duration": 8,  # clipped by audio file's actual duration
                    "lane": 0,
                },
                {
                    "id": "a2",
                    "src": "https://www.w3schools.com/html/horse.mp3",
                    "start": 3,
                    "duration": 2,
                    "lane": 1,
                },
                {
                    "id": "a3",
                    "src": "https://www.w3schools.com/html/horse.mp3",
                    "start": 7,
                    "duration": 3,
                    "lane": 0,
                },
            ],
        }
