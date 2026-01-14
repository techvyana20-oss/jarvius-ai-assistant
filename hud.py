import tkinter as tk
import threading
from time import strftime
from weather import get_weather
from system_stats import get_cpu, get_ram
from voice import listen, speak

# ================== UI CONSTANTS ==================
WIDTH, HEIGHT = 800, 600
CENTER_X, CENTER_Y = 400, 300

angle1 = 0
angle2 = 0
status_text = "IDLE"
listening_active = True


# ================== MAIN HUD ==================
def start_hud():
    global angle1, angle2, status_text, listening_active

    root = tk.Tk()
    root.title("JARVIUS HUD")
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.configure(bg="#050b14")
    root.resizable(False, False)

    canvas = tk.Canvas(
        root,
        width=WIDTH,
        height=HEIGHT,
        bg="#050b14",
        highlightthickness=0
    )
    canvas.pack()

    # ============ DRAW RING FUNCTION ============
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

    # ============ HUD ANIMATION LOOP ============
    def animate():
        global angle1, angle2
        canvas.delete("all")

        # Rotating rings
        draw_ring(220, 3, 40, angle1, "#00f7ff")
        draw_ring(180, 4, 30, -angle2, "#00cfff")
        draw_ring(130, 2, 20, angle1 * 2, "#00ffaa")

        # Center text
        canvas.create_text(
            CENTER_X,
            CENTER_Y,
            text="J.A.R.V.I.U.S",
            fill="white",
            font=("Arial", 18, "bold")
        )

        # Status text
        canvas.create_text(
            CENTER_X,
            CENTER_Y + 40,
            text=status_text,
            fill="#00ffaa",
            font=("Arial", 11)
        )

        # Time
        canvas.create_text(
            CENTER_X,
            CENTER_Y + 120,
            text=strftime("%I:%M:%S %p"),
            fill="#00ffaa",
            font=("Arial", 12)
        )

        # Weather
        canvas.create_text(
            40,
            40,
            text=get_weather(),
            fill="#00ffaa",
            font=("Arial", 11),
            anchor="w"
        )

        # System stats
        canvas.create_text(
            40,
            70,
            text=get_cpu(),
            fill="#00f7ff",
            font=("Arial", 11),
            anchor="w"
        )
        canvas.create_text(
            40,
            90,
            text=get_ram(),
            fill="#00f7ff",
            font=("Arial", 11),
            anchor="w"
        )

        angle1 += 1
        angle2 += 2

        root.after(60, animate)

    # ============ VOICE THREAD ============
    def voice_loop():
        global status_text, listening_active

        speak("Jarvius online")

        activated = False

        while listening_active:
            status_text = "LISTENING..."

            command = listen()  # SAFE: returns "" on silence

            if command == "":
                continue

            # Wake word
            if "jarvius" in command:
                activated = True
                status_text = "ACTIVE"
                speak("Yes, how can I help you")
                continue

            if not activated:
                continue

            # Commands
            if "time" in command:
                speak("The current time is " + strftime("%I %M %p"))

            elif "status" in command:
                speak("All systems are running normally")

            elif "shutdown" in command or "exit" in command:
                speak("Shutting down Jarvius")
                listening_active = False
                root.quit()
                break

            activated = False

    # ============ START THREADS ============
    threading.Thread(target=voice_loop, daemon=True).start()
    animate()
    root.mainloop()
