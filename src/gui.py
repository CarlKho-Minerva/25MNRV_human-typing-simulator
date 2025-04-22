import tkinter as tk
from tkinter import ttk
import threading
import time
import json
import os
from .typing_engine import TypingSimulator
from .config import DEFAULT_CONFIG, SPEED_PRESETS  # Added SPEED_PRESETS import


class ToggleButton(ttk.Checkbutton):
    """Custom toggle button with modern look"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, style="Switch.TCheckbutton", **kwargs)


class TypingSimulatorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Typing Simulator")

        # Initialize variables before creating widgets
        self.font_size = 10
        self.speed_preset = tk.StringVar(value="Medium")
        self.error_var = tk.BooleanVar(value=True)
        self.keep_errors_var = tk.BooleanVar(value=False)
        self.error_rate_var = tk.DoubleVar(value=0.02)

        # Calculate viewport sizes (80% of screen)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)

        # Center window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.config = DEFAULT_CONFIG.copy()
        self.simulator = TypingSimulator(self.config)
        self.typing_thread = None
        self.is_typing = False
        self.countdown_label = None
        self.countdown_value = 5
        self.instructions_shown = False

        self.load_preferences()
        self._setup_styles()
        self._apply_theme()
        self._create_widgets()

    def _apply_theme(self):
        """Apply dark theme colors with better contrast"""
        self.root.configure(bg="#1a1a1a")  # Darker background
        style = ttk.Style()
        style.configure(
            ".",
            background="#1a1a1a",
            foreground="#ffffff",  # Brighter text
            fieldbackground="#2d2d2d",  # Lighter input areas
            borderwidth=0,
        )
        style.configure("TLabelframe", background="#1a1a1a", foreground="#ffffff")
        style.configure("TLabelframe.Label", background="#1a1a1a", foreground="#ffffff")
        style.configure(
            "Switch.TCheckbutton",
            background="#1a1a1a",
            foreground="#ffffff",
            padding=2
        )
        style.configure(
            "Preset.TRadiobutton",
            background="#2d2d2d",
            foreground="#ffffff",
            padding=10
        )
        style.configure(
            "TButton",
            background="#3d3d3d",
            foreground="#ffffff",
            padding=6
        )

    def _setup_styles(self):
        """Setup custom styles for widgets"""
        style = ttk.Style()
        style.configure("Switch.TCheckbutton", padding=2, width=4, background="#ffffff")

    def _create_widgets(self):
        # Create main container that fills the window
        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True)

        # Create left and right panes
        left_pane = ttk.Frame(container)
        right_pane = ttk.Frame(container)
        left_pane.pack(side="left", fill="both", expand=True, padx=10)
        right_pane.pack(side="right", fill="y", padx=10)

        # Instructions and countdown in left pane
        self.instructions_label = ttk.Label(
            left_pane,
            text="Welcome! Paste your text below and adjust settings.",
            font=('Segoe UI', 12),
            background="#1a1a1a",
            foreground="#ffffff",
            wraplength=600,
            justify="center"
        )
        self.instructions_label.pack(pady=5)

        self.countdown_label = ttk.Label(
            left_pane,
            text="",
            font=('Segoe UI', 48, 'bold'),
            background="#1a1a1a",
            foreground="#8ab4f8"
        )
        self.countdown_label.pack(pady=5)

        # Text area and its controls in left pane
        text_frame = ttk.Frame(left_pane)
        text_frame.pack(fill="both", expand=True)

        # Font size control
        font_controls = ttk.Frame(text_frame)
        font_controls.pack(fill="x", pady=5)
        ttk.Label(font_controls, text="Font Size:").pack(side="left")
        font_scale = ttk.Scale(
            font_controls,
            from_=8,
            to=24,
            value=self.font_size,
            command=lambda s: self.text_area.configure(font=("Segoe UI", int(float(s)))),
            orient="horizontal"
        )
        font_scale.pack(side="left", fill="x", expand=True, padx=5)

        # Text area with dark theme
        self.text_area = tk.Text(
            text_frame,
            bg="#2d2d2d",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat",
            padx=20,
            pady=10,
            font=("Segoe UI", self.font_size),
            undo=True  # Enable undo/redo
        )
        self.text_area.pack(fill="both", expand=True, pady=5)

        # Word count label below text area
        self.word_count_label = ttk.Label(
            text_frame,
            text="Words: 0",
            font=("Segoe UI", 10),
            background="#1a1a1a",
            foreground="#8ab4f8"
        )
        self.word_count_label.pack(anchor="w", padx=5, pady=(0, 5))
        self.text_area.bind("<KeyRelease>", self._update_word_count)
        self.text_area.bind("<FocusIn>", self._update_word_count)
        self.text_area.bind("<ButtonRelease>", self._update_word_count)
        # Bind Ctrl+Z for undo
        self.text_area.bind('<Control-z>', lambda e: self.text_area.edit_undo())
        self.text_area.bind('<Control-y>', lambda e: self.text_area.edit_redo())

        # Controls in right pane (always visible)
        controls_container = ttk.Frame(right_pane)
        controls_container.pack(fill="y", expand=True)

        # Speed controls
        speed_frame = ttk.LabelFrame(controls_container, text="Typing Speed", padding=10)
        speed_frame.pack(fill="x", pady=5)

        # Radio buttons in grid layout
        for i, (preset, data) in enumerate(SPEED_PRESETS.items()):
            btn = ttk.Radiobutton(
                speed_frame,
                text=preset,
                value=preset,
                variable=self.speed_preset,
                command=self._update_speed_preset,
                style="Preset.TRadiobutton",
                width=20  # Add fixed width
            )
            btn.pack(fill="x", pady=2)
            self._create_tooltip(btn, data["desc"])

        # Custom speed slider
        custom_frame = ttk.Frame(speed_frame)
        custom_frame.pack(fill="x", pady=5)
        ttk.Label(
            custom_frame,
            text="Words per minute:",
            wraplength=150
        ).pack(side="top", anchor="w")

        self.custom_speed_var = tk.IntVar(value=80)
        custom_slider = ttk.Scale(
            custom_frame,
            from_=1,
            to=1000,
            variable=self.custom_speed_var,
            orient="horizontal",
            command=lambda v: self._update_custom_speed(float(v))  # Fix the lambda
        )
        custom_slider.pack(fill="x", expand=True, pady=(5,0))
        self.custom_speed_label = ttk.Label(custom_frame, width=12)
        self.custom_speed_label.pack(pady=2)

        # Trigger initial update
        self._update_custom_speed(80.0)  # Initialize with default value

        # Error controls
        error_frame = ttk.LabelFrame(controls_container, text="Error Simulation", padding=10)
        error_frame.pack(fill="x", pady=5)

        # Error toggles with wider buttons
        for text, var in [
            ("Simulate Errors", self.error_var),
            ("Keep Errors", self.keep_errors_var)
        ]:
            toggle = ToggleButton(
                error_frame,
                text=text,
                variable=var,
                command=self._update_preferences,
                width=25
            )
            toggle.pack(fill="x", pady=2, padx=5)

        # Error rate slider
        error_rate_frame = ttk.Frame(error_frame)
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
            variable=self.error_rate_var,
            command=self._update_error_rate,
            orient="horizontal"
        )
        error_slider.pack(fill="x", expand=True, pady=(5,0))
        self.error_rate_label = ttk.Label(error_rate_frame, width=8)
        self.error_rate_label.pack(pady=2)

        # Initialize slider values
        self._update_custom_speed(self.custom_speed_var.get())
        self._update_error_rate(self.error_rate_var.get())

        # Action buttons at bottom of right pane
        button_frame = ttk.Frame(controls_container)
        button_frame.pack(side="bottom", fill="x", pady=10)

        self.start_button = ttk.Button(
            button_frame,
            text="Start (Ctrl+S)",
            style="Accent.TButton",
            command=self.start_typing
        )
        self.start_button.pack(fill="x", pady=2)

        self.stop_button = ttk.Button(
            button_frame,
            text="Stop (Esc)",
            command=self.stop_typing
        )
        self.stop_button.pack(fill="x", pady=2)

        # Keyboard shortcuts
        self.text_area.bind("<Control-b>", lambda e: self._format_selection("bold"))
        self.text_area.bind("<Control-i>", lambda e: self._format_selection("italic"))
        self.root.bind("<Control-s>", lambda e: self.start_typing())
        self.root.bind("<Escape>", lambda e: self.stop_typing())

    def _create_speed_controls(self, parent):
        """Create speed control section with presets"""
        speed_frame = ttk.LabelFrame(
            parent,
            text="Typing Speed",
            padding=10,
            style="Card.TLabelframe"
        )
        speed_frame.pack(fill=tk.X, pady=5)

        # Speed presets
        preset_frame = ttk.Frame(speed_frame)
        preset_frame.pack(fill=tk.X, pady=5)

        self.speed_preset = tk.StringVar(value=self.config.get("SPEED_PRESET", "Medium"))

        for preset, data in SPEED_PRESETS.items():
            btn = ttk.Radiobutton(
                preset_frame,
                text=preset,
                value=preset,
                variable=self.speed_preset,
                command=self._update_speed_preset,
                style="Preset.TRadiobutton"
            )
            btn.pack(side=tk.LEFT, padx=5)

            # Add tooltip
            self._create_tooltip(btn, data["desc"])

        # Replace custom entry with slider
        custom_frame = ttk.Frame(speed_frame)
        custom_frame.pack(fill=tk.X, pady=5)

        self.custom_speed_var = tk.IntVar(value=80)
        custom_slider = ttk.Scale(
            custom_frame,
            from_=1,
            to=1000,
            variable=self.custom_speed_var,
            orient="horizontal",
            command=lambda v: self._update_custom_speed(float(v))
        )
        custom_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.custom_speed_label = ttk.Label(custom_frame, text="80 WPM")
        self.custom_speed_label.pack(side=tk.LEFT)

        # Variation controls
        var_frame = ttk.Frame(speed_frame)
        var_frame.pack(fill=tk.X, pady=5)

        ttk.Label(var_frame, text="Speed variation:").pack(side=tk.LEFT)
        self.std_var = tk.IntVar(value=self.config["WPM_STD"])
        std_scale = ttk.Scale(
            var_frame,
            from_=0,
            to=100,
            variable=self.std_var,
            orient="horizontal",
            command=self._update_variation
        )
        std_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.std_label = ttk.Label(var_frame, width=8)
        self.std_label.pack(side=tk.LEFT, padx=5)
        self._update_variation(self.std_var.get())

    def _create_tooltip(self, widget, text):
        """Create tooltip for widget"""
        tooltip = tk.Label(
            self.root,
            text=text,
            background="#4d4d4d",
            foreground="#ffffff",
            relief="solid",
            borderwidth=1,
            font=("Segoe UI", 9)
        )

        def enter(event):
            tooltip.lift()
            tooltip.place_forget()
            x = widget.winfo_rootx() + widget.winfo_width()
            y = widget.winfo_rooty()
            tooltip.place(x=x, y=y)

        def leave(event):
            tooltip.place_forget()

        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def _update_speed_preset(self):
        """Update speed based on selected preset"""
        preset = self.speed_preset.get()
        if (preset != "Custom"):
            wpm = SPEED_PRESETS[preset]["wpm"]
            # Update the custom speed var and label to match preset
            self.custom_speed_var.set(wpm)
            self.custom_speed_label.configure(text=f"{wpm:,} WPM")
        else:
            try:
                wpm = int(self.custom_speed_var.get())
            except ValueError:
                wpm = 80  # Default if invalid input
                self.custom_speed_var.set("80")

        self.config["WPM_MEAN"] = wpm
        self.simulator.cpm_mean = wpm * 5
        self.config["SPEED_PRESET"] = preset

    def start_typing(self):
        if self.typing_thread and self.typing_thread.is_alive():
            return

        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            return

        self.is_typing = True
        self.start_button.state(['disabled'])
        self.countdown_value = 5
        self.instructions_shown = False
        self._countdown()

    def _show_instructions(self):
        """Show typing preparation instructions"""
        self.instructions_label.configure(
            text="Prepare to type!\n"
            "1. Place your cursor where you want to type\n"
            "2. Timer will start in 5 seconds\n"
            "3. Press ESC at any time to stop"
        )

    def _countdown(self):
        """Display countdown timer with status"""
        if not self.instructions_shown:
            self._show_instructions()
            self.instructions_shown = True
            self.root.after(1000, self._countdown)
            return

        if self.countdown_value > 0:
            self.countdown_label.configure(
                text=f"{self.countdown_value}",
                foreground="#8ab4f8" if self.countdown_value > 3 else "#ff7043"
            )
            self.countdown_value -= 1
            self.root.after(1000, self._countdown)
        else:
            self.countdown_label.configure(text="GO!", foreground="#81c995")  # Google Green
            self.instructions_label.configure(text="")
            self.root.after(500, lambda: self.countdown_label.configure(text=""))
            self._start_typing_thread()

    def _start_typing_thread(self):
        """Start the actual typing thread after countdown"""
        text = self.text_area.get("1.0", tk.END).strip()
        self.typing_thread = threading.Thread(target=self._typing_task, args=(text,))
        self.typing_thread.start()

    def stop_typing(self):
        """Stop the typing simulation"""
        self.is_typing = False
        self.simulator.stop_typing = True  # Add this flag to stop typing
        self.start_button.state(["!disabled"])

    def _typing_task(self, text):
        time.sleep(self.config["START_DELAY"])
        self.simulator.type_text(list(text))
        self.start_button.state(["!disabled"])

    def _format_text(self, marker):
        """Apply formatting to selected text"""
        try:
            selected = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
            self.text_area.insert(tk.INSERT, f"{marker}{selected}{marker}")
        except tk.TclError:  # No selection
            self.text_area.insert(tk.INSERT, marker)

    def _format_selection(self, style):
        """Handle keyboard shortcut formatting"""
        try:
            selected = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)

            if style == "bold":
                self.text_area.insert(tk.INSERT, f"<b>{selected}</b>")
            elif style == "italic":
                self.text_area.insert(tk.INSERT, f"<i>{selected}</i>")

        except tk.TclError:  # No selection
            pass

    def _add_bullet(self):
        """Add bullet point at current line"""
        line_start = self.text_area.index("insert linestart")
        self.text_area.insert(line_start, "• ")

    def load_preferences(self):
        """Load user preferences"""
        self.preferences_file = os.path.join(
            os.path.expanduser("~"), ".typing_simulator_prefs"
        )
        try:
            with open(self.preferences_file, "r") as f:
                self.preferences = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.preferences = {"simulate_errors": True}

    def _update_preferences(self):
        """Save user preferences"""
        self.preferences.update({
            'simulate_errors': self.error_var.get(),
            'keep_errors': self.keep_errors_var.get()
        })
        self.config.update({
            "ENABLE_ERRORS": self.error_var.get(),
            "KEEP_ERRORS": self.keep_errors_var.get()
        })
        try:
            with open(self.preferences_file, 'w') as f:
                json.dump(self.preferences, f)
        except Exception as e:
            print(f"Failed to save preferences: {e}")

    def _update_speed(self, value):
        """Update WPM setting with formatted display"""
        rounded_value = round(float(value))
        self.wpm_var.set(rounded_value)
        self.config["WPM_MEAN"] = rounded_value
        self.simulator.cpm_mean = rounded_value * 5
        self.wpm_label.configure(text=f"{rounded_value:,}" + (" WPM" if rounded_value < 1000 else ""))

    def _update_variation(self, value):
        """Update WPM variation with formatted display"""
        rounded_value = round(float(value))
        self.std_var.set(rounded_value)
        self.config["WPM_STD"] = rounded_value
        self.simulator.cpm_std = rounded_value * 5
        self.std_label.configure(text=f"±{rounded_value:,}")

    def _update_custom_speed(self, value):
        """Update custom speed display and config"""
        try:
            wpm = round(float(value))  # Convert to float first, then round to nearest integer
            self.custom_speed_label.configure(text=f"{wpm:,} WPM")
            if self.speed_preset.get() == "Custom":
                self.config["WPM_MEAN"] = wpm
                self.simulator.cpm_mean = wpm * 5
        except ValueError as e:
            print(f"Error updating speed: {e}")

    def _update_error_rate(self, value):
        """Update error rate with percentage display"""
        rate = round(float(value))/100
        self.error_rate_var.set(rate * 100)
        self.config["ERROR_RATE"] = rate
        self.simulator.base_error_rate = rate
        self.error_rate_label.configure(text=f"{rate*100:.1f}%")

    def _update_word_count(self, event=None):
        text = self.text_area.get("1.0", tk.END)
        words = len([w for w in text.split() if w.strip()])
        self.word_count_label.config(text=f"Words: {words}")

    def run(self):
        self.root.mainloop()
