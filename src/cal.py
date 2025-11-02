from streamlit_calendar import calendar
from pydantic import BaseModel
import streamlit as st
from uuid import uuid4
from typing import Any, List
import datetime
from src.lib import _to_rfc3339

class Event(BaseModel):
    title: str
    from_my_calendar: bool = False
    start: str  # ISO format date-time string
    end: str    # ISO format date-time string

def show_calendar(events: List[Any], start_date: str, end_date: str, height=600):
    # Normalize start/end to RFC3339 and extract date portion (YYYY-MM-DD)
    if start_date:
        start_rfc = _to_rfc3339(start_date, datetime.datetime.now())
    else:
        start_rfc = _to_rfc3339(None, datetime.datetime.now())
    
    if end_date:
        end_rfc = _to_rfc3339(end_date, datetime.datetime.now() + datetime.timedelta(days=10))
    else:
        end_rfc = _to_rfc3339(None, datetime.datetime.now() + datetime.timedelta(days=10))

    start_iso = start_rfc[:10]  # YYYY-MM-DD
    end_iso = end_rfc[:10]      # YYYY-MM-DD

    try:
        end_exclusive = (datetime.date.fromisoformat(end_iso) + datetime.timedelta(days=1)).isoformat()
    except Exception:
        end_exclusive = end_iso

    calendar_options = {
        "editable": False,
        "selectable": False,
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "resourceTimelineWeek",
        },
        "slotMinTime": "00:00:00",
        "slotMaxTime": "24:00:00",
        "initialView": "resourceTimelineWeek",
        "initialDate": start_iso,
        "validRange": {
            "start": start_iso,
            "end": end_exclusive
        },
        "contentHeight": height,
        "aspectRatio": 1.5,
            "initialView": "resourceTimelineDay",
        "resources": [
            {"id": "a", "title": "My Schedule"},
        ],
    }

    calendar_events = []

    for idx, item in enumerate(events):
        # support (event, i) tuple shape
        if isinstance(item, (list, tuple)) and len(item) == 2 and isinstance(item[1], int):
            event_obj = item[0]
            idx = item[1]
        else:
            event_obj = item

        # normalize event to dict
        if hasattr(event_obj, "model_dump"):  # pydantic v2
            event_dict = event_obj.model_dump()
        elif hasattr(event_obj, "dict"):      # pydantic v1 or similar
            try:
                event_dict = event_obj.dict()
            except Exception:
                event_dict = {}
        elif isinstance(event_obj, dict):
            event_dict = event_obj
        else:
            # fallback to attribute access
            event_dict = {
                "title": getattr(event_obj, "title", str(event_obj)),
                "start": getattr(event_obj, "start", None),
                "end": getattr(event_obj, "end", None)
            }

        # ensure required fields
        title = event_dict.get("title") or event_dict.get("summary") or f"Event {idx}"
        start = event_dict.get("start")
        end = event_dict.get("end")

        if not start:
            # skip events without start
            continue

        calendar_events.append({
            "id": str(event_dict.get("id", idx)),
            "title": title,
            "start": start,
            **({"end": end} if end else {}),
            "resourceId": "a"
        })
    
    for calendar_event in calendar_events:
        print("Calendar Event: ", calendar_event)

        # Render using streamlit_calendar component with custom CSS
        with st.container():
            st.markdown("""
            <style>
            .fc-view-harness {
                    overflow-x: auto !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            c = calendar(
                    events=calendar_events,
                    options=calendar_options,
                    key='calendar',
            )
            st.write(c)
