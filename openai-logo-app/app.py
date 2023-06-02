import os, openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=("GET", "POST"))
def openai_app():
    if request.method == "POST":
        text = request.form["text"]
        color = request.form["color"]
        number = request.form["number"]
        response = openai.Image.create(
            prompt=generate_prompt(text, color),
            n=int(number),
            size="256x256"
        )

        urls = ','.join(map(lambda x: x['url'], response['data']))
        return redirect(url_for("openai_app", result=urls))

    result = request.args.get("result")
    if result:
        urls = result.split(',')
        return render_template("index.html", len = len(urls), urls = urls, result=result)
    return render_template("index.html", result=result)

def generate_prompt(text, color):
    return """Lettermark logo design for \"{}\", {} color.""".format(text, color)


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5050)