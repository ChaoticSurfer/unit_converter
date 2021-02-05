from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

conversions = {
    "მილიმეტრი": {"მილიმეტრი": 1, "სანტიმეტრი": 0.1, "მეტრი": 0.001, "კილომეტრი": 1 / 1000000},
    "სანტიმეტრი": {"მილიმეტრი": 10, "სანტიმეტრი": 1, "მეტრი": 0.001, "კილომეტრი": 1 / 1000000},
    "მეტრი": {"მილიმეტრი": 1000, "სანტიმეტრი": 100, "მეტრი": 1, "კილომეტრი": 0.001},
    "კილომეტრი": {"მილიმეტრი": 100000, "სანტიმეტრი": 10000, "მეტრი": 1000, "კილომეტრი": 1},
}


def convert(unit, measure=0):
    results = []
    for key, value in conversions[unit].items():
        if key == unit: continue
        results.append(f'{key} : {value * measure}')
    return results


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


def read_file():
    with open("static/logs.txt", "r") as f:
        lines = f.readlines()
    return lines


def write_to_file(txt):
    with open("static/logs.txt", "a") as f:
        f.write(str(txt) + "\n")


@app.route("/logs", methods=["GET"])
def show_table():
    lines = read_file()
    lines = tuple(map(lambda x: x.split(), lines))
    return render_template("table.html", lines=lines)


@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        measure = request.form["measure"]
        unit = request.form['unit']
        if measure == "":
            measure = 0

        data = convert(unit, int(measure))

        ip_address =  request.headers['X-Real-IP'] 
        #request.remote_addr 

        write_to_file(f"{ip_address} {data}")

        return render_template('result.html', data=data)


if __name__ == '__main__':
    app.debug = True
    app.run()
