from flask import Flask, request, redirect, url_for, render_template_string
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # Redirects unauthenticated users to login page

# User class
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# In-memory users
users = {
    "admin": {"password": "admin123", "id": 1},
    "user": {"password": "user123", "id": 2},
}

# Load user function
@login_manager.user_loader
def load_user(user_id):
    for username, user_data in users.items():
        if user_data["id"] == int(user_id):
            return User(id=user_data["id"], username=username)
    return None

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if username in users and users[username]["password"] == password:
            user = User(id=users[username]["id"], username=username)
            login_user(user)
            return redirect(url_for("home"))
        else:
            return "Invalid username or password. Please try again."
    
    return render_template_string("""
    <html>
    <body>
        <h2>Login</h2>
        <form method="POST">
            <label for="username">Username:</label>
            <input type="text" name="username" required><br><br>
            <label for="password">Password:</label>
            <input type="password" name="password" required><br><br>
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    """)

# Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# Home route with authentication
@app.route("/", methods=["GET", "POST"])
@login_required
def home():
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
            <h2>Welcome, {current_user.username}!</h2>
            <p>This is a simple web app built with Flask.</p>

            <form method="POST">
                <label>Enter your name:</label>
                <input type="text" name="name" value="{name}" required>
                
                <label>Select a number:</label>
                <input type="range" name="number" min="1" max="100" value="{number}">
                
                <button type="submit">Submit</button>
            </form>
    """

    if name:
        response += f"<h3>Hello, {name}! 👋</h3>"

    response += f"""
            <p>You selected: {number}</p>
            <a href="/logout">Logout</a>
        </div>
    </body>
    </html>
    """
    
    return response

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Uses PORT from Render or defaults to 5000
    app.run(host="0.0.0.0", port=port, debug=True)
