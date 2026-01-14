# hud.py
import tkinter as tk
import math
from time import strftime
from weather import get_weather
from system_stats import get_cpu, get_ram

WIDTH, HEIGHT = 800, 600
CENTER_X, CENTER_Y = 400, 300

angle1 = 0
angle2 = 0

def start_hud():
    global angle1, angle2

    root = tk.Tk()
    root.title("JARVIUS HUD")
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.configure(bg="#050b14")
    root.resizable(False, False)

    canvas = tk.Canvas(
        root, width=WIDTH, height=HEIGHT,
        bg="#050b14", highlightthickness=0
    )
    canvas.pack()

    def draw_ring(radius, thickness, segments, offset, color):
        for i in range(segments):
            start = offset + (360 / segments) * i
            canvas.create_arc(
                CENTER_X - radius,
                CENTER_Y - radius,
                CENTER_X + radius,
                CENTER_Y + radius,
                start=start,
                extent=12,
                style="arc",
                outline=color,
                width=thickness
            )

    def animate():
        nonlocal canvas
        global angle1, angle2
        canvas.delete("all")

        # Rings
        draw_ring(220, 3, 40, angle1, "#00f7ff")
        draw_ring(180, 4, 30, -angle2, "#00cfff")
        draw_ring(130, 2, 20, angle1 * 2, "#00ffaa")

        # Center circle
        canvas.create_oval(
            CENTER_X - 90, CENTER_Y - 90,
            CENTER_X + 90, CENTER_Y + 90,
            outline="#00f7ff", width=3
        )

        # Center text
        canvas.create_text(
            CENTER_X, CENTER_Y,
            text="J.A.R.V.I.U.S",
            fill="white",
            font=("Orbitron", 18, "bold")
        )

        # Time
        canvas.create_text(
            CENTER_X, CENTER_Y + 120,
            text=strftime("%I:%M:%S %p"),
            fill="#00ffaa",
            font=("Arial", 12)
        )

        # Weather
        canvas.create_text(
            100, 50,
            text=get_weather(),
            fill="#00ffaa",
            font=("Arial", 11),
            anchor="w"
        )

        # System Stats
        canvas.create_text(
            100, 80,
            text=get_cpu(),
            fill="#00f7ff",
            font=("Arial", 11),
            anchor="w"
        )
        canvas.create_text(
            100, 100,
            text=get_ram(),
            fill="#00f7ff",
            font=("Arial", 11),
            anchor="w"
        )

        angle1 += 1
        angle2 += 2

        root.after(1000, animate)

    animate()
    root.mainloop()

