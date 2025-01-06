from turtle import Screen, Turtle
import speech_recognition as sr
import pyttsx3

def initialize_tts_engine():
    """Initialize the TTS engine and set it to a female voice if available."""
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")

    for voice in voices:
        if "female" in voice.name.lower() or "zira" in voice.name.lower():
            engine.setProperty("voice", voice.id)
            break

    engine.setProperty("rate", 150)  # Set a comfortable speaking speed
    return engine


def speak(text, engine):
    """Speak the given text using the TTS engine."""
    engine.say(text)
    engine.runAndWait()


def listen_for_command():
    """Use the microphone to capture and recognize user commands."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        try:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"Recognized: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand the command.")
        except sr.WaitTimeoutError:
            print("Listening timed out.")
        return ""


def draw_grid(turtle, grid_size, canvas_width, canvas_height):
    """Draw a grid on the canvas."""
    turtle.speed(0)
    turtle.penup()
    turtle.color("lightgray")

    # Draw vertical lines
    for x in range(-canvas_width // 2, canvas_width // 2 + grid_size, grid_size):
        turtle.goto(x, canvas_height // 2)
        turtle.setheading(270)  # Point downwards
        turtle.pendown()
        turtle.forward(canvas_height)
        turtle.penup()

    # Draw horizontal lines
    for y in range(-canvas_height // 2, canvas_height // 2 + grid_size, grid_size):
        turtle.goto(-canvas_width // 2, y)
        turtle.setheading(0)  # Point to the right
        turtle.pendown()
        turtle.forward(canvas_width)
        turtle.penup()

    # Reset turtle for drawing
    turtle.color("black")
    turtle.goto(0, 0)
    turtle.pendown()  # Ensure the pen is down for future drawing


def handle_move(turtle, engine):
    """Handle the move command and prompt for the distance."""
    speak("How far should I move?", engine)
    distance_input = listen_for_command()

    # Extract numeric value from the input
    try:
        # Split the input and check for numbers
        distance = int(''.join(filter(str.isdigit, distance_input)))
        turtle.forward(distance)
        speak(f"Moved {distance} units.", engine)
    except ValueError:
        speak("I couldn't understand the distance. Please say a valid number.", engine)


def handle_turn(turtle, engine):
    """Handle the turn command and prompt for the angle."""
    speak("How many degrees should I turn?", engine)
    angle_input = listen_for_command()

    # Extract numeric value from the input
    try:
        angle = int(''.join(filter(str.isdigit, angle_input)))
        turtle.left(angle)
        speak(f"Turned {angle} degrees.", engine)
    except ValueError:
        speak("I couldn't understand the angle. Please say a valid number.", engine)


def handle_circle(turtle, engine):
    """Handle the circle command and prompt for the radius."""
    speak("What radius should the circle have?", engine)
    radius_input = listen_for_command()

    # Extract numeric value from the input
    try:
        radius = int(''.join(filter(str.isdigit, radius_input)))
        turtle.circle(radius)
        speak(f"Drew a circle with radius {radius}.", engine)
    except ValueError:
        speak("I couldn't understand the radius. Please say a valid number.", engine)


def main():
    # Set up the drawing canvas
    screen = Screen()
    screen.setup(width=800, height=600)
    screen.bgcolor("white")  # Set the background color to white
    turtle = Turtle()

    # Initialize the TTS engine
    engine = initialize_tts_engine()
    speak("Welcome to Eduvox. Say a command.", engine)

    # Draw the grid on the canvas
    grid_size = 10  # Size of each grid square (e.g., 50 pixels)
    canvas_width = 800  # Canvas width (same as screen width)
    canvas_height = 600  # Canvas height (same as screen height)
    draw_grid(turtle, grid_size, canvas_width, canvas_height)

    while True:
        command = listen_for_command()

        if "exit" in command:
            speak("Exiting the program. Goodbye!", engine)
            break

        elif "move" in command:
            handle_move(turtle, engine)

        elif "rotate" in command:
            handle_turn(turtle, engine)

        elif "circle" in command:
            handle_circle(turtle, engine)

        elif "clear" in command:
            turtle.clear()
            draw_grid(turtle, grid_size, canvas_width, canvas_height)  # Redraw the grid after clearing
            speak("Cleared the screen.", engine)

        else:
            speak("I didn't understand that. Please try again.", engine)


if __name__ == "__main__":
    main()
