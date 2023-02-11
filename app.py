from flask import Flask, request, render_template
import openai

app = Flask(__name__)

openai.api_key = "API_KEY"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST", "GET"])
def upload():
    return render_template("form.html")


@app.route("/essay", methods=["POST", "GET"])
def essay():
    name = request.form["name"]
    age = request.form["age"]
    college = request.form["college"]
    course = request.form["course"]
    nationality = request.form["nationality"]
    hobbies = request.form["hobbies"]
    achievements = request.form["achievements"]
    essay_text = request.form["essay_text"]

    # Generate suggestions
    suggestion = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Write suggestions for the essay. The essay texy is {essay_test}. The name of the person is {name}. The age of the person is {age}. The person is interested in {course} course in {college} college. Give a few better suggestions to improve the essay",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        n=1,
        stop = None,

    )

    score = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Write a score for the essay. The essay texy is {essay_test}. The name of the person is {name}. The age of the person is {age}. The person is interested in {course} course in {college} college. Give a score for the essay out of 5",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        n=1,
        stop = None,

    )

    sample_essay = openai.Completion.create(
        engine="text-davinci-002",
        prompt="Write a sample essay. The essay texy is {essay_test}. The name of the person is {name}. The age of the person is {age}. The person is interested in {course} course in {college} college. Give a sample essay",
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        n=1,
        stop = None,

    )

    suggestion = suggestion["choices"][0]["text"]
    score = score["choices"][0]["text"]
    sample_essay = sample_essay["choices"][0]["text"]

    return render_template("essay.html",essay=essay_text, suggestion=suggestion, score=score, sample=sample_essay)

@app.route("/prompt", methods=["POST", "GET"])
def prompt():
    return render_template("prompt.html")

@app.route("/prompt_essay", methods=["POST", "GET"])
def prompt_essay():
    prompt = request.form["prompt"]
    essay = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        n=1,
        stop = None,

    )

    essay = essay["choices"][0]["text"]

    return render_template("prompt_essay.html", essay=essay)




if __name__ == "__main__":
    app.run(debug=True)
