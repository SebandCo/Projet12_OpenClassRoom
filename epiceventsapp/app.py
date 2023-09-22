from flask import Flask
import exchange_bdd as bdd


app = Flask(__name__)


@app.route('/')
def home():
    enterprises = bdd.browse_enterprise()
    return str(enterprises)


if __name__ == '__main__':
    app.run(debug=True)
