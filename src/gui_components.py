"""GUI subcomponents for the Typing Simulator (modularized for clarity)."""

import tkinter as tk
from tkinter import ttk
from .config import SPEED_PRESETS

class ToggleButton(ttk.Checkbutton):
    """Custom toggle button with modern look."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, style="Switch.TCheckbutton", **kwargs)

class SpeedControls(ttk.LabelFrame):
    """Encapsulates speed preset and custom speed controls."""
    def __init__(self, parent, speed_preset_var, custom_speed_var, update_speed_preset, update_custom_speed):
        super().__init__(parent, text="Typing Speed", padding=10)
        for preset, data in SPEED_PRESETS.items():
            btn = ttk.Radiobutton(
                self,
                text=preset,
                value=preset,
                variable=speed_preset_var,
                command=update_speed_preset,
                style="Preset.TRadiobutton",
                width=20
            )
            btn.pack(fill="x", pady=2)
        custom_frame = ttk.Frame(self)
        custom_frame.pack(fill="x", pady=5)
        ttk.Label(custom_frame, text="Words per minute:", wraplength=150).pack(side="top", anchor="w")
        custom_slider = ttk.Scale(
            custom_frame,
            from_=1,
            to=1000,
            variable=custom_speed_var,
            orient="horizontal",
            command=lambda v: update_custom_speed(float(v))
        )
        custom_slider.pack(fill="x", expand=True, pady=(5,0))
        self.custom_speed_label = ttk.Label(custom_frame, width=12)
        self.custom_speed_label.pack(pady=2)

class ErrorControls(ttk.LabelFrame):
    """Encapsulates error simulation controls."""
    def __init__(self, parent, error_var, keep_errors_var, error_rate_var, update_preferences, update_error_rate):
        super().__init__(parent, text="Error Simulation", padding=10)
        for text, var in [
            ("Simulate Errors", error_var),
            ("Keep Errors", keep_errors_var)
        ]:
            toggle = ToggleButton(
                self,
                text=text,
                variable=var,
                command=update_preferences,
                width=25
            )
            toggle.pack(fill="x", pady=2, padx=5)
        error_rate_frame = ttk.Frame(self)
        error_rate_frame.pack(fill="x", pady=5)
        ttk.Label(
            error_rate_frame,
            text="Error Rate (%):",
            wraplength=150
        ).pack(side="top", anchor="w")
        error_slider = ttk.Scale(
            error_rate_frame,
            from_=0,
            to=50,
            variable=error_rate_var,
            command=update_error_rate,
            orient="horizontal"
        )
        error_slider.pack(fill="x", expand=True, pady=(5,0))
        self.error_rate_label = ttk.Label(error_rate_frame, width=8)
        self.error_rate_label.pack(pady=2)
