from flask import Flask, render_template, request, redirect
import os
import logging

app = Flask(__name__)

# Basic application logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Temporary notes storage
# We will replace this with AWS RDS in the database step.
notes = []


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        note = request.form.get("note", "").strip()

        if note:
            notes.append(note)
            app.logger.info("New note created successfully")

        return redirect("/")

    return render_template("index.html", notes=notes)


@app.route("/delete/<int:index>")
def delete(index):
    if 0 <= index < len(notes):
        notes.pop(index)
        app.logger.info("Note deleted successfully")

    return redirect("/")


@app.route("/health")
def health():
    return {
        "status": "healthy",
        "service": "Cloud Notes App"
    }


if __name__ == "__main__":
    # 0.0.0.0 allows the application to be accessed
    # from the AWS EC2 server.
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )