from flask import Flask, Markup, request, render_template
import matplotlib.pyplot as plt
import io
import base64
import mysql.connector
from collections import Counter

app = Flask(__name__)


def datapakken(keuzescreen):
    keuze = keuzescreen
    mydb = mysql.connector.connect(
        host="192.168.172.74",
        user="corne",
        password="Welkom01",
        database="iot"
    )
    if keuze == "iotcorne":
        darray = []
        mycursor = mydb.cursor()
        mycursor.execute("SELECT Temperatuur FROM iotcorne ORDER BY Recorded DESC LIMIT 1")
        darray.append(mycursor.fetchone())
        mycursor.execute("SELECT C02 FROM iotcorne ORDER BY Recorded DESC LIMIT 1")
        darray.append(mycursor.fetchone())
        mycursor.execute("SELECT HUMIDITY FROM iotcorne ORDER BY Recorded DESC LIMIT 1")
        darray.append(mycursor.fetchone())
        mycursor.execute("SELECT Recorded FROM iotcorne ORDER BY Recorded DESC LIMIT 1")
        time = mycursor.fetchone()
        return darray, time
    elif keuze == "iotsam":
        mycursor = mydb.cursor()
        mycursor.execute("SELECT Waarde, Recorded FROM iotsam ORDER BY Recorded DESC LIMIT 1")
        data = mycursor.fetchone()
        return data
    elif keuze == "iotjesse":
        mycursor = mydb.cursor()
        mycursor.execute("SELECT Recorded FROM iotjesse ORDER BY Recorded DESC LIMIT 2")
        gegevens = mycursor.fetchall()
        print(gegevens)
        return gegevens
    elif keuze == "iotmauro":
        mycursor = mydb.cursor()
        mycursor.execute("SELECT Waarde, TagID FROM iotmauro")
        data = mycursor.fetchall()
        lijstg = []
        lijstf = []
        gefaald = 0
        gelukt = 0
        for i in data:
            waarde = i[0]
            id = i[1]
            if waarde == "ID klopt niet":
                gefaald = gefaald + 1
                lijstf.append(id)
            if waarde == "ID klopt":
                gelukt = gelukt + 1
                lijstg.append(id)
        lijstg = Counter(lijstg)
        lijstf = Counter(lijstf)
        return gelukt, gefaald
    elif keuze == "graph":
        mycursor = mydb.cursor()
        mycursor.execute("SELECT Waarde, TagID FROM iotmauro")
        data = mycursor.fetchall()
        lijstg = []
        lijstf = []
        for i in data:
            waarde = i[0]
            id = i[1]
            if waarde == "ID klopt niet":
                lijstf.append(id)
            if waarde == "ID klopt":
                lijstg.append(id)
        lijstg = Counter(lijstg)
        lijstf = Counter(lijstf)
        return lijstg, lijstf
    elif keuze == "databases":
        mycursor = mydb.cursor()
        mycursor.execute("SHOW TABLES")
        myresult = mycursor.fetchall()
        return myresult


def plotmaker(data, time, keuzescreen):
    if keuzescreen == "iotcorne":
        img = io.BytesIO()
        time = time[0].strftime("%Y-%m-%d %H:%M:%S")
        names = ['Temperatuur', 'C02', 'Humidity']
        values = [data[0][0], data[1][0], data[2][0]]
        plt.subplots()
        plt.bar(names, values)
        plt.title(time)
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        return plot_url
    elif keuzescreen == "iotmauro":
        img1 = io.BytesIO()
        namen = ['Gelukt', 'Gefaald']
        waarden = [data, time]
        gelukt, gefaald = datapakken("graph")
        names = []
        values = []
        for key, value in gelukt.items():
            names.append(str(key))
            values.append(value)
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
        fig.suptitle('Aantal ID Checks')
        ax1.bar(namen, waarden)
        ax1.set_title('Aantal x totaal')
        ax2.bar(names, values)
        ax2.set_title('Individueel gelukt')
        names = []
        values = []
        for key, value in gefaald.items():
            names.append(str(key))
            values.append(value)
        ax3.bar(names, values)
        ax3.set_title('Individueel gefaald')
        fig.savefig(img1, format='png')
        img1.seek(0)
        plot_url1 = base64.b64encode(img1.getvalue()).decode()
        return plot_url1


@app.route('/', methods=['GET', 'POST'])
def index():
    databases = datapakken("databases")
    if request.method == 'POST':
        selectedValue = request.form['database']
        gekozen = str(selectedValue)
        for i in databases:
            i = str(i)
            if i == gekozen:
                data1 = i[2:-3]
                if data1 == "iotjesse":
                    data = datapakken(data1)
                    data = str("Voor het laatst beweging gedetecteerd op " + data[0][0].strftime(
                        "%Y-%m-%d %H:%M:%S") + " daarvoor " + data[1][0].strftime("%Y-%m-%d %H:%M:%S"))
                    return render_template('index.html', data=data, databases=databases)
                elif data1 == "iotsam":
                    data = datapakken(data1)
                    print(data[1], data[0])
                    data = str(
                        "Waterstandniveau is op dit moment " + data[0] + " en de tijd waarop het gemeeten " + data[
                            1].strftime("%Y-%m-%d %H:%M:%S"))
                    return render_template('index.html', data=data, databases=databases)
                elif data1 == "iotmauro":
                    datag, dataf = datapakken(data1)
                    img1 = plotmaker(datag, dataf, data1)
                    return render_template('index.html', content=img1, databases=databases)
                elif data1 == "iotcorne":
                    data, time = datapakken(data1)
                    img = plotmaker(data, time, data1)
                    return render_template('index.html', content=img, databases=databases)
    return render_template('index.html', databases=databases)
    # content='<img src="data:image/png;base64,{}">'.format(img))
    # '<img src="data:image/png;base64,{}">'.format(img)


"""
def plotmaker(data):
    #time = time[0].strftime("%Y-%m-%d %H:%M:%S")
    print(data[0], data[1])
    img = io.BytesIO()
    y = [1, 2, 3, 4, 5]
    x = [0, 2, 1, 3, 4]
    plt.plot(x, y)
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    #
    return plot_url

def datav():
    mydb = mysql.connector.connect(
        host="172.16.1.11",
        user="corne",
        password="Student",
        database="lade"
    )
    data = ['a', 'b']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT Message, recorded FROM status ORDER BY recorded DESC LIMIT 1")
    myresult = mycursor.fetchall()
    print(myresult)
    for x in myresult:
        tijd = str(x[1])
        data1 = str(x[0])
        data[0] = data1
        data[1] = tijd
    return data
@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        data = datav()
        return render_template('index.html', content=data)
    return render_template('index.html', content=data)
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
