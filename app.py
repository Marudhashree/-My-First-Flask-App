from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    name = ""
    number = 50  # Default value

    if request.method == "POST":
        name = request.form.get("name", "")
        number = int(request.form.get("number", 50))

    response = f"""
    <html>
    <head>
        <title>🚀 My First Flask App</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; padding: 20px; }}
            .container {{ max-width: 500px; margin: auto; }}
            input, button, select {{ padding: 10px; margin: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 My First Flask App</h1>
            <h2>Welcome to Flask!</h2>
            <p>This is a simple web app built with Flask in VS Code.</p>

            <form method="POST">
                <label>Enter your name:</label>
                <input type="text" name="name" value="{name}" required>
                <button type="submit">Say Hello</button>
            </form>
    """

    if name:
        response += f"<h3>Hello, {name}! 👋</h3>"

    response += f"""
            <form method="POST">
                <label>Select a number:</label>
                <input type="range" name="number" min="1" max="100" value="{number}">
                <button type="submit">Submit</button>
            </form>
            <p>You selected: {number}</p>
        </div>
    </body>
    </html>
    """

    return response

if __name__ == "__main__":
    app.run(debug=True)
