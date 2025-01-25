import tkinter as tk
from tkinter import ttk
import threading
import time
import json
import os
from .typing_engine import TypingSimulator
from .config import DEFAULT_CONFIG


class ToggleButton(ttk.Checkbutton):
    """Custom toggle button with modern look"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, style="Switch.TCheckbutton", **kwargs)


class TypingSimulatorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Typing Simulator")
        self.root.geometry("800x700")  # Taller window
        self.config = DEFAULT_CONFIG.copy()
        self.simulator = TypingSimulator(self.config)
        self.typing_thread = None
        self.is_typing = False
        self.countdown_label = None
        self.countdown_value = 5  # Increased countdown time
        self.instructions_shown = False

        self.load_preferences()
        self._setup_styles()
        self._apply_theme()
        self._create_widgets()

    def _apply_theme(self):
        """Apply dark theme colors"""
        self.root.configure(bg="#202124")
        style = ttk.Style()
        style.configure(
            ".",
            background="#202124",
            foreground="#e8eaed",
            fieldbackground="#303134",
            borderwidth=0,
        )
        style.configure("TLabelframe", background="#202124", foreground="#e8eaed")
        style.configure("TLabelframe.Label", background="#202124", foreground="#e8eaed")
        style.configure(
            "Switch.TCheckbutton", background="#202124", foreground="#e8eaed", padding=2
        )
        style.configure(
            "TButton", background="#303134", foreground="#e8eaed", padding=6
        )

        # Add styles for canvas
        style = ttk.Style()
        style.configure("Canvas.TFrame", background="#202124")

        # Make scrollbar less visible in dark theme
        style.configure("TScrollbar",
            background="#202124",
            troughcolor="#303134",
            borderwidth=0,
            arrowcolor="#e8eaed")

    def _setup_styles(self):
        """Setup custom styles for widgets"""
        style = ttk.Style()
        style.configure("Switch.TCheckbutton", padding=2, width=4, background="#ffffff")

    def _create_widgets(self):
        # Create main scrollable canvas
        canvas = tk.Canvas(self.root, bg="#202124")
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)

        # Main frame inside canvas
        main_frame = ttk.Frame(canvas)
        main_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Add main frame to canvas
        canvas.create_window((0, 0), window=main_frame, anchor="nw", width=780)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Instructions and countdown labels with reduced padding
        self.instructions_label = ttk.Label(
            main_frame,
            text="Welcome! Paste your text below and adjust settings.",
            font=('Segoe UI', 12),
            background="#202124",
            foreground="#e8eaed",
            wraplength=600,
            justify="center"
        )
        self.instructions_label.pack(pady=2)

        self.countdown_label = ttk.Label(
            main_frame,
            text="",
            font=('Segoe UI', 48, 'bold'),
            background="#202124",
            foreground="#8ab4f8"
        )
        self.countdown_label.pack(pady=2)

        # Text area with reduced padding
        self.text_area = tk.Text(
            main_frame,
            height=15,
            width=70,
            bg="#303134",
            fg="#e8eaed",
            insertbackground="#e8eaed",
            relief="flat",
            padx=10,
            pady=5,
            font=("Segoe UI", 10),
        )
        self.text_area.pack(pady=5)

        # Formatting toolbar with modern look
        format_frame = ttk.Frame(main_frame)
        format_frame.pack(fill=tk.X, pady=5)

        for btn, symbol in [("Bold", "B"), ("Italic", "I"), ("Bullet", "•")]:
            ttk.Button(
                format_frame,
                text=symbol,
                width=3,
                command=lambda m=btn: self._format_text(
                    "**" if m == "Bold" else "_" if m == "Italic" else "• "
                ),
            ).pack(side=tk.LEFT, padx=2)

        # Speed control frame
        speed_frame = ttk.LabelFrame(main_frame, text="Typing Speed", padding=5)
        speed_frame.pack(fill=tk.X, pady=5)

        # WPM Scale with higher range
        ttk.Label(speed_frame, text="Words per minute:").pack(side=tk.LEFT)
        self.wpm_var = tk.IntVar(value=self.config["WPM_MEAN"])
        wpm_scale = ttk.Scale(
            speed_frame,
            from_=10,
            to=5000000,  # Increased maximum
            variable=self.wpm_var,
            orient="horizontal",
            command=lambda x: self._update_speed(round(float(x)))
        )
        wpm_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.wpm_label = ttk.Label(speed_frame, width=10)
        self.wpm_label.pack(side=tk.LEFT, padx=5)
        self._update_speed(self.wpm_var.get())

        # Variation Scale
        var_frame = ttk.Frame(speed_frame)
        var_frame.pack(fill=tk.X, pady=5)
        ttk.Label(var_frame, text="Speed variation:").pack(side=tk.LEFT)
        self.std_var = tk.IntVar(value=self.config["WPM_STD"])
        std_scale = ttk.Scale(
            var_frame,
            from_=0,
            to=1000,  # Increased maximum
            variable=self.std_var,
            orient="horizontal",
            command=lambda x: self._update_variation(round(float(x)))
        )
        std_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.std_label = ttk.Label(var_frame, width=10)
        self.std_label.pack(side=tk.LEFT, padx=5)
        self._update_variation(self.std_var.get())

        # Error control frame (single frame now)
        error_frame = ttk.LabelFrame(main_frame, text="Error Simulation", padding=5)
        error_frame.pack(fill=tk.X, pady=5)

        # Error controls in single frame
        controls_grid = ttk.Frame(error_frame)
        controls_grid.pack(fill=tk.X, padx=5)

        # Error toggle and keep errors in one row
        toggle_frame = ttk.Frame(controls_grid)
        toggle_frame.pack(fill=tk.X, pady=2)

        self.error_var = tk.BooleanVar(value=self.preferences.get('simulate_errors', True))
        error_toggle = ToggleButton(
            toggle_frame,
            text="Simulate Human-Like Typing Errors",
            variable=self.error_var,
            command=self._update_preferences,
            width=30
        )
        error_toggle.pack(side=tk.LEFT, padx=5)

        self.keep_errors_var = tk.BooleanVar(value=self.preferences.get('keep_errors', False))
        keep_errors_toggle = ToggleButton(
            toggle_frame,
            text="Keep Errors in Final Output",
            variable=self.keep_errors_var,
            command=self._update_preferences,
            width=30
        )
        keep_errors_toggle.pack(side=tk.LEFT, padx=5)

        # Error rate slider in second row
        error_rate_frame = ttk.Frame(controls_grid)
        error_rate_frame.pack(fill=tk.X, pady=2)
        ttk.Label(error_rate_frame, text="Error Rate:").pack(side=tk.LEFT)
        self.error_rate_var = tk.DoubleVar(value=self.config["ERROR_RATE"] * 100)
        error_rate_scale = ttk.Scale(
            error_rate_frame,
            from_=0,
            to=50,
            variable=self.error_rate_var,
            orient="horizontal",
            command=self._update_error_rate
        )
        error_rate_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
        self.error_rate_label = ttk.Label(error_rate_frame, width=8)
        self.error_rate_label.pack(side=tk.LEFT, padx=5)
        self._update_error_rate(self.error_rate_var.get())

        # Control buttons with reduced padding
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(pady=5)

        self.start_button = ttk.Button(
            controls_frame,
            text="Start Typing (Ctrl+S)",
            style="Accent.TButton",
            command=self.start_typing,
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(
            controls_frame, text="Stop (Esc)", command=self.stop_typing
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Add padding at bottom for better scrolling
        ttk.Frame(main_frame, height=20).pack()

        # Bind mousewheel to scroll
        self.root.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        self.root.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        self.root.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

        # Keyboard shortcuts
        self.root.bind("<Control-s>", lambda e: self.start_typing())
        self.root.bind("<Escape>", lambda e: self.stop_typing())

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
        self.is_typing = False
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

    def _update_error_rate(self, value):
        """Update error rate with percentage display"""
        rate = round(float(value))/100
        self.error_rate_var.set(rate * 100)
        self.config["ERROR_RATE"] = rate
        self.simulator.base_error_rate = rate
        self.error_rate_label.configure(text=f"{rate*100:.1f}%")

    def run(self):
        self.root.mainloop()
