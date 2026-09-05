from flask import Flask, render_template, request, redirect, url_for, session, flash

from database.database import (
    init_db,
    create_user,
    verify_user,
    save_analysis,
    get_user_analyses
)

from models.persona_model import predict_persona

from utils.leakage_detector import (
    detect_sensitive_data,
    calculate_risk,
    generate_recommendations
)


app = Flask(__name__)

app.secret_key = "development-secret-key"

init_db()


@app.route("/")
def index():

    if "user_id" in session:
        return redirect(url_for("dashboard"))

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and password are required.")
            return redirect(url_for("register"))

        if len(password) < 6:
            flash("Password must contain at least 6 characters.")
            return redirect(url_for("register"))

        success = create_user(username, password)

        if success:
            flash("Registration successful. Please login.")
            return redirect(url_for("login"))

        flash("Username already exists.")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = verify_user(username, password)

        if user:

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(url_for("dashboard"))

        flash("Invalid username or password.")

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("index"))


@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    analyses = get_user_analyses(session["user_id"])

    return render_template(
        "dashboard.html",
        analyses=analyses
    )


@app.route("/analysis", methods=["GET", "POST"])
def analysis():

    if "user_id" not in session:
        return redirect(url_for("login"))

    result = None

    if request.method == "POST":

        input_text = request.form.get("data", "").strip()

        if not input_text:
            flash("Please enter some data for analysis.")
            return redirect(url_for("analysis"))

        persona = predict_persona(input_text)

        detected_data = detect_sensitive_data(input_text)

        leakage_risk = calculate_risk(detected_data)

        privacy_risk = leakage_risk

        recommendations = generate_recommendations(
            detected_data
        )

        detected_text = ", ".join(
            item["type"]
            for item in detected_data
        )

        recommendation_text = " | ".join(
            recommendations
        )

        save_analysis(
            session["user_id"],
            input_text,
            persona,
            privacy_risk,
            leakage_risk,
            detected_text,
            recommendation_text
        )

        result = {
            "persona": persona,
            "privacy_risk": privacy_risk,
            "leakage_risk": leakage_risk,
            "detected_data": detected_data,
            "recommendations": recommendations
        }

    return render_template(
        "analysis.html",
        result=result
    )


@app.route("/report/<int:analysis_id>")
def report(analysis_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    analyses = get_user_analyses(session["user_id"])

    selected = None

    for item in analyses:

        if item["id"] == analysis_id:
            selected = item
            break

    if selected is None:
        flash("Report not found.")
        return redirect(url_for("dashboard"))

    return render_template(
        "report.html",
        analysis=selected
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
