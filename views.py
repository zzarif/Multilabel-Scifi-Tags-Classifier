from flask import Blueprint, render_template, request
import requests


views = Blueprint(__name__, "views")


@views.route("/", methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        input_text = request.form['text']
        output = predict_genres(input_text)[0]
        confidence_list = output['confidences']
        labels = [elem['label'] for elem in confidence_list if elem['confidence'] >= 0.5 ]
        return render_template("result.html", input_text=input_text, labels=labels)
    else:
        return render_template("index.html")

def predict_genres(input_text):
    response = requests.post("https://zzarif-stackexchange-scifi-tags-classifier.hf.space/run/predict", json={
        "data": [
            input_text
        ]
    }).json()
    data = response["data"]
    return data