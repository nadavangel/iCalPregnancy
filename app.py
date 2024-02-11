# -*- coding: utf-8 -*-
import tempfile
import threading
import uuid
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, send_file, abort, Response
from json import dumps
from dotenv import load_dotenv

import time
import os

from calenderCalc.iCal import PregnancyICal

app = Flask('PregnancyCalendar')
load_dotenv()
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'THIS IS NOT A SECRET')

# Function to create a file
def create_file(selected_option: str, date_input: str, week_input: int , show_week_starts: bool, add_trimester_starts: bool):
    def getFileName():
        return f"PregnancyCalendar_{time.time()}_{uuid.uuid4().hex}"
    filename = getFileName()
    
    cal = PregnancyICal()
    if selected_option == 'last_month':
        cal.lastMonthlyPeriod = datetime.fromisoformat(date_input)
    elif selected_option == 'ovulation':
        cal.ovulationDate = datetime.fromisoformat(date_input)
    elif selected_option == 'week_number':
        cal.setByWeekNumber(week_input)
    else:
        error_message = dumps({'Message': 'Invalid option'})
        abort(Response(error_message, 400))
        
    cal.addTrimester = add_trimester_starts
    cal.allDays = not show_week_starts
    fullPath = cal.write(directory=Path(tempfile.gettempdir()), fileName = filename)
    return fullPath

# Function to delete a file after 2 minutes
def delete_file_after_delay(filename, delay_seconds=60):
    def delete_file():
        time.sleep(delay_seconds)
        os.remove(filename)

    # Start a new thread to delete the file after the delay
    threading.Thread(target=delete_file).start()

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_option = request.form.get('options')
        date_input = request.form.get('date_input')
        week_input = request.form.get('week_input')
        show_week_starts = 'show_week_starts' in request.form
        add_trimester_starts = 'add_trimester_starts' in request.form
        
        if week_input == '':
            week_input  = 2
        else:
            week_input = int(week_input)

        filename = create_file(selected_option, date_input, week_input, show_week_starts, add_trimester_starts)

        # Start a download session
        delete_file_after_delay(filename)
        return send_file(filename, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
