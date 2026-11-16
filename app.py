from flask import Flask, render_template, request

from student_manager import (
    calculate_average,
    get_mention,
    is_admitted,
    validate_grades,
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        raw = request.form.get("grades", "").strip()
        if not raw:
            error = "Erreur : veuillez saisir au moins une note."
        else:
            try:
                grades = [float(x.strip()) for x in raw.split(",")]
            except ValueError:
                grades = None
                error = "Erreur : les notes doivent être des nombres séparés par des virgules."
            if grades is not None:
                if not validate_grades(grades):
                    error = "Erreur : les notes doivent être comprises entre 0 et 20."
                else:
                    avg = calculate_average(grades)
                    result = {
                        "average": round(avg, 2),
                        "mention": get_mention(avg),
                        "admitted": "Admis" if is_admitted(avg) else "Non admis",
                    }
    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
