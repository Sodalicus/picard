#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Paweł Krzemiński 
#
# Distributed under terms of the MIT license.

"""

"""

from flask import Flask, g
from flask import render_template, request, redirect, url_for, flash
from flask import session
import os
import sqlite3
from picard_client import send
from picard_base import get_radios, save_radios, get_def_radio, get_recent_temp, get_now_playing
from picard_base import get_volume


app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY='12345',
    DATABASE=os.path.join(app.root_path, 'data.db'),
    SITE_NAME='Remote Control'
))

addr = ("127.0.0.1", 65432)

def get_db():
    """Create connection to database """
    if not g.get('db'):
        con = sqlite3.connect(app.config['DATABASE'])
        con.row_factory = sqlite3.Row
        g.db = con
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Close connection to db"""
    if g.get('db'):
        g.db.close()


def retrive_data():
    """Get most recent reading from database"""
    cur = get_db().cursor()
    sqlQuery = "SELECT * FROM reading ORDER BY time_added ASC;"
    return results


def read_devices_info():
    """Read device info (name, type, switchability, description)
       from table device"""
    cur = get_db().cursor()
    sqlQuery = "SELECT * FROM device;"
    cur.execute(sqlQuery)
    results = cur.fetchall()
    devices = []
    for row in results:
        devices.append(dict((cur.description[idx][0], value)
                for idx, value in enumerate(row)))
    return devices



@app.route('/', methods=['GET', 'POST'])
def index():
    """
    devices = read_devices_info()
    status = retrive_data()
    if status == None:
        status = [0]*11
    for device in devices:
        device['status'] = status[device['id']]
        if device['unit'] == "celsius":
            device['symbol'] = "&#8451;"
        elif device['unit'] == "percents":
            device['symbol'] = "%"
        elif device['unit'] == "minutes":
            device['symbol'] = "&prime;"
        else:
            device['symbol'] = None
    mostRecent = status[10]
    #flash('Status: {}'.format(status))
    nowPlaying = player.now_playing()
    nowPlaying = "crap"
    #volume = player.return_volume()
    volume = "10"
    return render_template('index.html',\
            devices = devices,\
            mostRecent = mostRecent,\
            nowPlaying = nowPlaying,\
            volume = volume)
    """
    defRadio = get_def_radio()
    tempDate = get_recent_temp()
    radios = get_radios().keys()
    nowPlaying = get_now_playing()
    volume = get_volume()
    if defRadio == None:
        defRadio = {'name' : 'No default radio selected', 'url' : '---'}
    return render_template('index.html',\
            defRadio = defRadio,\
            tempDate = tempDate,\
            radios = radios,\
            nowPlaying = nowPlaying,\
            volume = volume)

@app.route('/settings', methods=['GET'])
def settings():
    radios = get_radios()
    print('settings')
    print(radios)
    return render_template('settings.html',\
            radios = radios)

@app.route('/switch', methods=["POST"])
def switch():
    devNumber = int(request.form['dev_switch'])
    #talk_to_ard(devNumber-1)
    #flash('Clicked: {}'.format(devNumber))
    return redirect(url_for("index"))
    return render_template('index.html')


@app.route('/play_radio_def', methods=["POST"])
def play_radio_def():
    """Play default radio"""
    send("radio_def", addr)
    #player.play("radio")
    #display.msg("radio")
    return redirect(url_for("index"))

@app.route('/radio_stop', methods=["POST"])
def stop_radio():
    """Stop playing radio"""
    send("radio_stop", addr)
    #player.play("radio")
    #display.msg("radio")
    return redirect(url_for("index"))

@app.route('/noise', methods=["POST"])
def play_noise():
    #player.play("noise")
    #display.msg("noise")
    return redirect(url_for("index"))


@app.route('/beep', methods=['POST'])
def beep():
    #talk_to_ard(4)
    return redirect(url_for("index"))

@app.route('/volumeup', methods=['POST'])
def volume_up():
    send("volume_up", addr)
    return redirect(url_for("index"))

@app.route('/volumedown', methods=['POST'])
def volume_down():
    send("volume_down", addr)
    #player.volume_down()
    #vol = player.return_volume()
    #display.msg("Vol "+str(vol))
    return redirect(url_for("index"))

@app.route('/update_radios', methods=['POST'])
def update_radios():
    """Read the form from settings.html and update database accordingly."""
    if request.method == "POST":
        formData = request.form
        radioDef = int(request.form.get("radioDef"))
        radios = []
        for i in range(1, 11):
            radios.append( { 'id' :formData['radioId'+str(i)],\
                             'name' : formData['radioName'+str(i)],\
                             'url' : formData['radioUrl'+str(i)],\
                             'defRadio' : (True if radioDef == i else False)} )
        save_radios(radios)
        return redirect(url_for("settings"))

@app.route('/radio_play', methods=['POST'])
def radio_play():
    """get radio name from the drop-down input and play it."""
    if request.method == "POST":
        formData = request.form
        msg =  formData['dropdown']
        send(msg, addr)
    return redirect(url_for("index"))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
