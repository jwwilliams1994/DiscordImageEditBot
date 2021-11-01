import datetime, os
from PIL import Image
import mysql.connector
from mysql.connector import Error
import matplotlib
matplotlib.use('AGG')
from matplotlib import pyplot as plt
from influxdb import InfluxDBClient


# mydb = mysql.connector.connect(host="localhost", user="End", password="Wellington", database="atmolog")
def strTimetoDateTime(input):
    try:
        return datetime.datetime.strptime(input.replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S.%f')
    except:
        return datetime.datetime.strptime(input.replace("T", " ").replace("Z", ""), '%Y-%m-%d %H:%M:%S')


def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)


# def atmograph(mins, randId):
#     try:
#         mydb = mysql.connector.connect(host="localhost", user="End", password="Wellington", database="atmolog")
#         currentTime = datetime.datetime.now()
#         pastTime = currentTime - datetime.timedelta(minutes=mins)
#         sql_select_Query = "SELECT * FROM History WHERE (CAST(Date AS DATETIME) BETWEEN CAST('%s' AS DATETIME) AND CAST('%s' AS DATETIME));" % (
#         pastTime, currentTime)
#         cursor = mydb.cursor()
#         cursor.execute(sql_select_Query)
#         records = cursor.fetchall()
#         # print("Total number of rows is: ", cursor.rowcount)
#         Dates = []
#         Temps = []
#         Humids = []
#         Press = []
#         for row in records:
#             # print("Date = ", row[0], )
#             Dates.append(strTimetoDateTime(row[0]) - datetime.timedelta(hours=4))
#             # print("Temperature = ", row[1])
#             Temps.append(row[1])
#             # print("Humidity  = ", row[2])
#             Humids.append(row[2])
#             # print("Pressure  = ", row[3], "\n")
#             Press.append(row[3])
#         # print(Dates, "\n", Temps, "\n", Humids, "\n", Press)
#
#     except Error as e:
#         print("Error reading data from MySQL table", e)
#     finally:
#         if (mydb.is_connected()):
#             mydb.close()
#             cursor.close()
#             print("MySQL connection is closed")
#         dpi = 80
#         fig = plt.figure(figsize=(12, 3), dpi=dpi, facecolor=(0.196, 0.208, 0.231))
#         host = fig.add_subplot()
#         host.set_facecolor((0.196, 0.208, 0.231))
#         # fig, host = plt.subplots()
#         fig.subplots_adjust(right=0.75)
#
#         par1 = host.twinx()
#         par2 = host.twinx()
#
#         # Offset the right spine of par2.  The ticks and label have already been
#         # placed on the right by twinx above.
#         par2.spines["right"].set_position(("axes", 1.1))
#         # Having been created by twinx, par2 has its frame off, so the line of its
#         # detached spine is invisible.  First, activate the frame but make the patch
#         # and spines invisible.
#         make_patch_spines_invisible(par2)
#         # Second, show the right spine.
#         par2.spines["right"].set_visible(True)
#
#         p1, = host.plot(Dates, Temps, "b-", label="Temperature")
#         p2, = par1.plot(Dates, Humids, "r-", label="Humidity")
#         p3, = par2.plot(Dates, Press, "g-", label="Pressure")
#
#         host.set_xlim(pastTime - datetime.timedelta(hours=4), currentTime - datetime.timedelta(hours=4))
#         host.set_ylim(min(Temps) - 2, max(Temps) + 2)
#         par2.set_ylim(min(Press) - 0.001, max(Press) + 0.001)
#         par1.set_ylim(min(Humids) - 2, max(Humids) + 2)
#
#         host.set_xlabel("Date")
#         host.set_ylabel("Temperature")
#         par1.set_ylabel("Humidity")
#         par2.set_ylabel("Pressure")
#
#         host.yaxis.label.set_color(p1.get_color())
#         par1.yaxis.label.set_color(p2.get_color())
#         par2.yaxis.label.set_color(p3.get_color())
#
#         tkw = dict(size=4, width=1.5)
#         host.tick_params(axis='y', colors=p1.get_color(), **tkw)
#         par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
#         par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
#         host.tick_params(axis='x', rotation=45, **tkw)
#
#         lines = [p1, p2, p3]
#         plt.savefig(str(randId) + 'atmograph.png', transparent = False, bbox_inches = 'tight', pad_inches = 0.05)
#         return str(randId) + 'atmograph.png'
from random import randint
def atmograph2(mins):
    randId = str(randint(11111, 999999))
    try:
        client = InfluxDBClient(host='localhost', port=8086)
        client.switch_database('Atmolog')
        currentTime = datetime.datetime.now()
        pastTime = currentTime - datetime.timedelta(minutes=mins)
        # sql_select_Query = "SELECT * FROM History WHERE (CAST(Date AS DATETIME) BETWEEN CAST('%s' AS DATETIME) AND CAST('%s' AS DATETIME));" % (
        # pastTime, currentTime)
        # cursor = mydb.cursor()
        # cursor.execute(sql_select_Query)
        # records = cursor.fetchall()
        # print("Total number of rows is: ", cursor.rowcount)
        results = client.query('SELECT * FROM "Atmolog"."autogen"."Atmosphere" WHERE time> now() - ' + str(mins) + 'm')
        Dates = []
        Temps = []
        Humids = []
        Press = []
        points = results.get_points()
        for point in points:
            Dates.append(strTimetoDateTime(point['time']) - datetime.timedelta(hours=4))
            Temps.append(point['Temperature'])
            Humids.append(point['Humidity'])
            Press.append(point['Pressure'])
        # for row in records:
        #     # print("Date = ", row[0], )
        #     Dates.append(strTimetoDateTime(row[0]) - datetime.timedelta(hours=4))
        #     # print("Temperature = ", row[1])
        #     Temps.append(row[1])
        #     # print("Humidity  = ", row[2])
        #     Humids.append(row[2])
        #     # print("Pressure  = ", row[3], "\n")
        #     Press.append(row[3])
        # print(Dates, "\n", Temps, "\n", Humids, "\n", Press)

    except Exception as e:
        print(e)
    finally:
        dpi = 160
        blak = (39 / 255, 40 / 255, 34 / 255)
        print(blak)
        fig = plt.figure(figsize=(12, 3), dpi=dpi, facecolor=blak)
        host = fig.add_subplot()
        host.set_facecolor((0, 0, 0, 0))
        # fig, host = plt.subplots()
        fig.subplots_adjust(right=0.75)

        par1 = host.twinx()
        par2 = host.twinx()
        host.set_zorder(7)
        par1.set_zorder(6)
        par2.set_zorder(5)

        # Offset the right spine of par2.  The ticks and label have already been
        # placed on the right by twinx above.
        par2.spines["right"].set_position(("axes", 1.1))
        # Having been created by twinx, par2 has its frame off, so the line of its
        # detached spine is invisible.  First, activate the frame but make the patch
        # and spines invisible.
        make_patch_spines_invisible(par2)
        # Second, show the right spine.
        par2.spines["right"].set_visible(True)

        p1, = host.plot(Dates, Temps, zorder=88, color='#f92672', label="Temperature")

        p3, = par2.plot(Dates, Press, zorder=1, color='#a6e22e', label="Pressure")
        p2, = par1.plot(Dates, Humids, zorder=4, color='#66d9ef', label="Humidity")


        host.set_xlim(pastTime - datetime.timedelta(hours=4), currentTime - datetime.timedelta(hours=4))
        host.set_ylim(min(Temps) - 2, max(Temps) + 2)
        par2.set_ylim(min(Press) - 0.001, max(Press) + 0.001)
        par1.set_ylim(min(Humids) - 2, max(Humids) + 2)

        host.set_xlabel("Date")
        host.set_ylabel("Temperature")
        par1.set_ylabel("Humidity")
        par2.set_ylabel("Pressure")

        host.xaxis.label.set_color('#fd971f')
        host.yaxis.label.set_color(p1.get_color())
        par1.yaxis.label.set_color(p2.get_color())
        par2.yaxis.label.set_color(p3.get_color())

        tkw = dict(size=4, width=1.5)
        host.tick_params(axis='y', colors=p1.get_color(), **tkw)
        par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
        par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
        host.tick_params(axis='x', colors='#fd971f', rotation=45, **tkw)

        lines = [p3, p2, p1]
        plt.savefig(str(randId) + 'atmograph.png', transparent = False, bbox_inches = 'tight', pad_inches = 0.05)
        img = Image.open(str(randId) + 'atmograph.png').copy().convert('RGBA')
        os.remove(str(randId) + 'atmograph.png')
        return img

