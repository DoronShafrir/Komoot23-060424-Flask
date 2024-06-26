# This version committed on December 23
from flask import Flask, redirect, url_for, render_template, request, flash
from  Komoot_Ana3 import K_Analize
from FetchTours import API
from datetime import datetime as dt
from pathlib import Path
from Comments import Comments as cm

'''-----Initialization---------'''
app = Flask(__name__)
app.secret_key = "Doron"
komoot_email = ""
komoot_password = ""
stat_data = []

@app.route("/", methods=["POST", "GET"])
@app.route("/home", methods=["POST", "GET"])
def home():
    global komoot_email
    global komoot_password
    global stat_data
    print(f"the request method is {request.method}")
    display_status = "none"

    if request.method == "POST":

        komoot_email = request.form["email"]
        komoot_password = request.form["password"]
        print(f"email: {komoot_email}, password: {komoot_password}")
        get_list = API()

        approved = get_list.login(komoot_email, komoot_password)


        print(f"approved: {approved}")

        if not approved:
            flash ("Wrong email or password", "info")
            display_status="none"
        else:
            get_list.get_user_tours_list() #save the outcome from the site API to "main.csv"
            display_status = "block"     #change the link to the second page to block(to be shown)

    updated_time = date_of_main()
    return render_template("home.html", display_status=display_status, updated_time=updated_time)


@app.route("/mainstat", methods=["POST", "GET"])
def mainstat():
    global stat_data
    if request.method == "POST":
        week_days_options = request.form.getlist('week_days_options')[0]
        from_when = request.form.getlist('from_when')[0]
        start_date = request.form.getlist('date')[0]
        print(f"status of radio buttons  week days: {week_days_options}")
        print(f"status of radio buttons  from when: {from_when}")
        print(f"status of start date: {start_date}")
        conf = confirm_create([start_date] ,week_days_options, from_when)
        daily = 1 if week_days_options == "daily" else 0
        stat_data = K_Analize(conf)
        updated_time = date_of_main()
        return render_template("main-stat.html", stat_data=stat_data.data, summary=stat_data.summary,
                               updated_time=updated_time, daily=daily)
    else:
        today_gen = dt.now()
        today_str = [f"{today_gen.year}-{today_gen.month}-{today_gen.day}"]
        conf = confirm_create(today_str)
        stat_data = K_Analize(conf)
        daily = 0

    updated_time = date_of_main()
    return render_template("main-stat.html", stat_data=stat_data.data, summary=stat_data.summary,
                           updated_time=updated_time, daily=daily)
# End of main_stat

@app.route("/show_comments", methods=["POST", "GET"])
def show_comments():
    global stat_data
    if request.method == "POST":
        week_days_options = 'daily'
        from_when = request.form.getlist('from_when')[0]
        start_date = request.form.getlist('date')[0]
        print(f"status of radio buttons  week days: {week_days_options}")
        print(f"status of radio buttons  from when: {from_when}")
        print(f"status of start date: {start_date}")
        conf = confirm_create([start_date], week_days_options, from_when, 'with_comments')
        daily = 1 if week_days_options == "daily" else 0
        stat_data = K_Analize(conf)
        updated_time = date_of_main()
        return render_template("show_comments.html", stat_data=stat_data.data, summary=stat_data.summary,
                               updated_time=updated_time, daily=daily)
    else:
        today_gen = dt.now()
        today_str = [f"{today_gen.year}-{today_gen.month}-{today_gen.day}"]
        conf = confirm_create(today_str)
        stat_data = K_Analize(conf)
        daily = 0

    updated_time = date_of_main()
    return render_template("show_comments.html", stat_data=stat_data.data, summary=stat_data.summary,
                           updated_time=updated_time, daily=daily)




@app.route("/change_comments", methods=["POST", "GET"])
def change_comments():
    date_to_change = cm.get_list_of_dates_to_change()
    if request.method == "POST":

        preferred_date = request.form.getlist('date_to_change')
        comment_to_change = request.form.getlist('comment')
        duration_to_change = request.form.getlist('duration')
        distance_to_change = request.form.getlist('distance')
        print(f"date_to_change  = {preferred_date}, comment = {comment_to_change},\n  duration = {duration_to_change}, distance ={distance_to_change}")

        cm.add_comment_to_csv(preferred_date, comment_to_change, duration_to_change, distance_to_change)

    return render_template("change_comments.html", date_to_change=date_to_change)




#--------------this rpocedure convert the radio swiches to a configuration list------------------#
def confirm_create(start_date , week_days_options ='weekly', from_when='from_date', with_comments='without_comments'):
    if start_date == [""]:
        start_date = ['2023-12-10'] # pseudo date just to fill
    else:
        start_date = start_date
    conf_begin = {'weekly' : [1,0], 'daily' : [0,1]}
    conf_end = {'day_one' : [1,0,0], 'year_start' : [0,1,0] , 'from_date' : [0,0,1]}
    conf_comments = {'without_comments': [0], 'with_comments': [1]}
    conf = start_date + conf_begin[week_days_options] + conf_end[from_when] + conf_comments[with_comments]
    print(conf)
    return conf

#--------------this pocedure get from the OS the last time main.csv was updated------------------#
def date_of_main():
    try:
        file_name = Path("main.csv")
        time = file_name.stat().st_mtime
        t = dt.fromtimestamp(time) #time stamp
        minutes = f"0{t.minute}" if t.minute <10 else t.minute
        return f"{t.day}/{t.month}/{t.year}  {t.hour}:{minutes}"
    except Exception:
        return "main.csv does not exist"


if __name__ == "__main__":
    app.run()
