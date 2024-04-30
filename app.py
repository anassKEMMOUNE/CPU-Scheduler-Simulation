from flask import Flask, render_template, request, redirect, url_for, jsonify,session

from scheduler import BatchScheduler, InteractiveScheduler
from system import System

app = Flask(__name__)
app.secret_key = 'secret_key'


def reset_page():
    f = open("static/csv/execution.csv", 'w')
    f.truncate(0)
    f.close()
    f = open("static/csv/process_table.csv", "w")
    f.truncate(0)
    f.close()
    f = open("static/csv/result.csv", "w")
    f.truncate(0)
    f.close()
    f = open("static/csv/SpecialFile.csv", "w")
    f.truncate(0)
    f.close()
    f = open("static/csv/system.txt", "w")
    f.truncate(0)
    f.close()



syst = None
algo = None


@app.route('/', methods=['GET', 'POST'])
def index():
    global syst, algo
    if request.method == 'POST':
        action = request.form['action']
        if action == "randomProcesses":

            number_processes = int(request.form['numberProcesses'])
            max_burst = int(request.form['maxBurst'])
            min_burst = int(request.form['minBurst'])
            max_arrival_time = int(request.form['maxArrivalTime'])
            quantum = 0
            contextSwitching = 0
            algo = request.form["dropdown"]
            print("algoooooo    ", algo)
            processes = System.generate_processes("static/csv/process_table.csv", number_processes, max_burst,
                                                  min_burst, max_arrival_time)
            if (algo == "FCFS" or algo == "SJF" or algo == "Priority Scheduling"):
                schedu = BatchScheduler()
            else:
                schedu = InteractiveScheduler()
                quantum = int(request.form["quantum"])
                contextSwitching = int(request.form["contextSwitching"])

            syst = System(schedu, processes, contextSwitching, quantum)
            result = syst.schedule(algo)
            syst.save_processes_csv("static/csv/result.csv", result[0])
            syst.system_to_csv("static/csv/system.txt")
            file = open("static/csv/system.txt", 'a')
            file.write("," + algo)
            file.close()
            print("Inside the post request")
            session["total"] = result[1]

            return render_template('index.html',total = session["total"])
    return render_template('index.html')


@app.route('/save_csv', methods=['POST'])
def save_csv():
    try:
        print("am here 1")
        data = request.get_json()
        csvData = data['csvData']
        print("am here 2")
        # Write the entire modified CSV data to the file
        with open('static/csv/process_table.csv', 'w') as file:
            file.write(csvData)
        file.close()

        print("am here 3")

        processes = System.load_from_csv('static/csv/process_table.csv')
        print("am here 4")
        syst = System.load_system_txt("static/csv/system.txt", processes)
        print("system   ", syst)
        file = open("static/csv/system.txt", "r")
        algo = file.readlines()[0].split(",")[-1].strip(" ")
        print("I am algo ", algo)
        file.close()
        result = syst.schedule(algo)
        print("system created !!!!!")
        syst.save_processes_csv("static/csv/result.csv", result[0])
        session["total"] = result[1]
        return redirect(url_for("index"))

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reset', methods=['GET'])
def reset():
    reset_page()
    print("Function executed!")
    # Optionally, you can return a response to the client
    return render_template("reset.html")


if __name__ == '__main__':
    app.run(debug=True)
