from flask import Flask, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Liczba zapytan do aplikacji"
)
HTTP_RESPONSES = Counter(
    "app_http_responses_total",
    "Liczba odpowiedzi HTTP wedlug statusu",
    ["status"]
)

@app.before_request
def count_requests():
    REQUEST_COUNT.inc()
@app.after_request
def count_http_responses(response):
    HTTP_RESPONSES.labels(
        status=str(response.status_code)
    ).inc()

    return response

@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>DevOps Diploma Project</title>
        </head>
        <body>
            <h1>Moja pierwsza aplikacja DevOps!</h1>
            <p>Aplikacja dziala poprawnie.</p>
            <p>Projekt wykorzystuje Docker, CI/CD i monitoring.</p>
        </body>
    </html>
    """


@app.route("/health")
def health():
    return {"status": "healthy"}, 200


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)