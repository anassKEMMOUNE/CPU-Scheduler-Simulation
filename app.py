from flask import Flask, render_template, request, redirect, url_for, session,Response,jsonify
import os
from process import Process
from system import System
from scheduler import BatchScheduler,InteractiveScheduler

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form['action']
        if action == "randomProcesses" :

            number_processes = int(request.form['numberProcesses'])
            max_burst = int(request.form['maxBurst'])
            min_burst = int(request.form['minBurst'])
            max_arrival_time = int(request.form['maxArrivalTime'])
            quantum =  0
            contextSwitching = 0
            algo =  request.form["dropdown"]
            print("algo  ",algo)
            processes =  System.generate_processes("static/csv/process_table.csv",number_processes,max_burst,min_burst,max_arrival_time)
            if (algo == "FCFS" or algo == "SJF" or algo == "Priority Scheduling") : 
                schedu =  BatchScheduler()
            else :
                schedu = InteractiveScheduler()
                quantum = int(request.form["quantum"])
                contextSwitching = int(request.form["contextSwitching"])

            syst = System(schedu,processes,contextSwitching,quantum)
            syst.schedule(algo)

            
        return render_template('index.html')
    return render_template('index.html')




@app.route('/save_csv', methods=['POST'])
def save_csv():
    try:
        data = request.get_json()
        csvData = data['csvData']

        # Write the entire modified CSV data to the file
        with open('static/csv/process_table.csv', 'w') as file:
            file.write(csvData)

        return jsonify({'message': 'CSV data saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500






if __name__ == '__main__':
    app.run(debug=True)
