from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        reminder_text = request.form['reminder_text']
        reminder_date = request.form['reminder_date']
        reminder_time = request.form['reminder_time']
        remind_when = request.form.getlist('remind_when')
        channel_notify = 'channel_notify' in request.form

        commands = generate_slack_commands(reminder_text, reminder_date, reminder_time, remind_when, channel_notify)
        return render_template('index.html', commands=commands, current_date=datetime.now().strftime('%Y-%m-%d'), current_time=datetime.now().strftime('%H:%M'))

    return render_template('index.html', commands=[], current_date=datetime.now().strftime('%Y-%m-%d'), current_time=datetime.now().strftime('%H:%M'))

def generate_slack_commands(text, date, time, when_list, channel_notify):
    command_template = '/remind "{text}" {date} at {time}'
    if channel_notify:
        text = f"@channel {text}"
    commands = []
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    for when in when_list:
        calculated_date = date_obj
        if when == '1_day':
            calculated_date -= timedelta(days=1)
        elif when == '2_days':
            calculated_date -= timedelta(days=2)
        elif when == '3_days':
            calculated_date -= timedelta(days=3)
        elif when == '1_week':
            calculated_date -= timedelta(weeks=1)
        elif when == '2_weeks':
            calculated_date -= timedelta(weeks=2)
        elif when == '3_weeks':
            calculated_date -= timedelta(weeks=3)
        elif when == '1_month':
            calculated_date -= timedelta(days=30)
        
        calculated_date_str = calculated_date.strftime('%Y-%m-%d')
        commands.append(command_template.format(text=text, date=calculated_date_str, time=time))
    return commands


if __name__ == "__main__":
    app.run(port=5001)
