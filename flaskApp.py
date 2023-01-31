from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

dbPath = "database/BeeHouse.db"

beehives = []

# list containing all the data of the selected beehive
bh_data_bat = [{'value': 'None'}]
bh_data_huml2 = [{'value': 'None'}]
bh_data_hum0 = [{'value': 'None'}]
bh_data_sound1 = [{'value': 'None'}]
bh_data_templ2 = [{'value': 'None'}]
bh_data_temp0 = [{'value': 'None'}]


def get_beehives():
    try:
        con = sqlite3.connect(dbPath)
        con.row_factory = sqlite3.Row
    except sqlite3.Error as e:
        print("error")
        print(e)
        return False

    cursor = con.cursor()
    cursor.execute("SELECT * FROM beehive")
    db_rec = cursor.fetchall()
    con.close()

    for i in db_rec:
        # print(i['adr'])
        beehives.append(i)

    return db_rec


def get_bh_data(str_query):
    print(str_query)
    local_bh_data_list = []
    try:
        con = sqlite3.connect(dbPath)
        con.row_factory = sqlite3.Row
    except sqlite3.Error as e:
        print("error")
        print(e)
        return False

    cursor = con.cursor()
    cursor.execute(str_query)
    db_rec = cursor.fetchall()
    con.close()

    for i in db_rec:
        local_bh_data_list.append(i)
        # print(i)

    return local_bh_data_list


get_beehives()


@app.route('/')
def index():
    # print(beehives)
    return render_template('homepage.html', beehives=beehives)


@app.route('/beehive/<string:hive_id>')
def beehive(hive_id):
    # print(hive_id)
    selected_hive = [hive for hive in beehives if hive['sName'] == hive_id]

    str_query_arg = str(selected_hive[0]['sName'][-1])

    bh_data_bat = [{'value': 'None'}] + get_bh_data("SELECT value FROM collect WHERE bhsn = '" + str_query_arg + "_1'")
    bh_data_huml2 = [{'value': 'None'}] + get_bh_data("SELECT value FROM collect WHERE bhsn = '" + str_query_arg + "_2'")
    bh_data_hum0 = [{'value': 'None'}] + get_bh_data("SELECT value FROM collect WHERE bhsn = '" + str_query_arg + "_3'")
    bh_data_sound1 = [{'value': 'None'}] + get_bh_data("SELECT value FROM collect WHERE bhsn = '" + str_query_arg + "_4'")
    bh_data_templ2 = [{'value': 'None'}] + get_bh_data("SELECT value FROM collect WHERE bhsn = '" + str_query_arg + "_5'")
    bh_data_temp0 = [{'value': 'None'}] + get_bh_data("SELECT value FROM collect WHERE bhsn = '" + str_query_arg + "_6'")

    print(bh_data_bat)
    print(bh_data_huml2)
    print(bh_data_hum0)
    print(bh_data_sound1)
    print(bh_data_templ2)
    print(bh_data_temp0)
    # print(selected_hive[0])
    # print(selected_hive[0]['adr'])
    return render_template('beehive.html',
                           beehives=beehives,
                           selected_hive=selected_hive,
                           bat=bh_data_bat,
                           huml2=bh_data_huml2,
                           hum0=bh_data_hum0,
                           sound1=bh_data_sound1,
                           templ2=bh_data_templ2,
                           temp0=bh_data_temp0
                           )


if __name__ == '__main__':
    app.run(debug=True)
