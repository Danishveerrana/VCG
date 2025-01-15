from my_flask_lib import Flask, request, json
from turtle import Screen, Turtle
import speech_recognition as sr
import pyttsx3
import threading

app = Flask(__name__)

# Initialize variables
screen = None
turtle = None
engine = None

def initialize_tts_engine():
    """Initialize the TTS engine."""
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    for voice in voices:
        if "female" in voice.name.lower():
            engine.setProperty("voice", voice.id)
            break
    engine.setProperty("rate", 150)
    return engine

def draw_grid(turtle, grid_size, canvas_width, canvas_height):
    """Draw a grid on the canvas."""
    turtle.speed(0)
    turtle.penup()
    turtle.color("lightgray")

    # Draw vertical lines
    for x in range(-canvas_width // 2, canvas_width // 2 + grid_size, grid_size):
        turtle.goto(x, canvas_height // 2)
        turtle.setheading(270)
        turtle.pendown()
        turtle.forward(canvas_height)
        turtle.penup()

    # Draw horizontal lines
    for y in range(-canvas_height // 2, canvas_height // 2 + grid_size, grid_size):
        turtle.goto(-canvas_width // 2, y)
        turtle.setheading(0)
        turtle.pendown()
        turtle.forward(canvas_width)
        turtle.penup()

    turtle.color("black")
    turtle.goto(0, 0)
    turtle.pendown()

def initialize_canvas():
    """Initialize the Turtle canvas."""
    global screen, turtle
    screen = Screen()
    screen.setup(width=800, height=600)
    screen.bgcolor("white")
    turtle = Turtle()

    # Draw the grid
    grid_size = 50
    canvas_width = 800
    canvas_height = 600
    draw_grid(turtle, grid_size, canvas_width, canvas_height)

@app.route("/")
def home():
    """Default endpoint."""
    return "Welcome to the Turtle Drawing API!"

@app.route("/command", methods=["POST"])
def process_command():
    """Process a command from the client."""
    global turtle, engine
    data = request.json
    command = data.get("command", "").lower()

    if "move" in command:
        try:
            distance = int(''.join(filter(str.isdigit, command)))
            turtle.forward(distance)
            speak(f"Moved {distance} units.", engine)
            return jsonify({"status": "success", "message": f"Moved {distance} units."})
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid distance input."})
    
    elif "rotate" in command or "turn" in command:
        try:
            angle = int(''.join(filter(str.isdigit, command)))
            turtle.left(angle)
            speak(f"Turned {angle} degrees.", engine)
            return jsonify({"status": "success", "message": f"Turned {angle} degrees."})
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid angle input."})
    
    elif "circle" in command:
        try:
            radius = int(''.join(filter(str.isdigit, command)))
            turtle.circle(radius)
            speak(f"Drew a circle with radius {radius}.", engine)
            return jsonify({"status": "success", "message": f"Drew a circle with radius {radius}."})
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid radius input."})

    elif "clear" in command:
        turtle.clear()
        draw_grid(turtle, 50, 800, 600)
        speak("Cleared the screen.", engine)
        return jsonify({"status": "success", "message": "Screen cleared."})

    elif "exit" in command:
        speak("Exiting the program.", engine)
        return jsonify({"status": "success", "message": "Program exiting."})

    return jsonify({"status": "error", "message": "Command not recognized."})

def speak(text, engine):
    """Speak the given text using the TTS engine."""
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    # Initialize Turtle and TTS in a separate thread
    threading.Thread(target=initialize_canvas).start()
    engine = initialize_tts_engine()
    app.run(host="0.0.0.0", port=5000)
