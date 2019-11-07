from app import app
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LocationForm, RegistrationForm, LoginForm, UploadForm
import os

from app import db
from app.models import Location, User, Titanic
from sqlalchemy.exc import IntegrityError
from werkzeug import secure_filename
import ast

def validate_login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

@app.route('/location', methods=['GET', 'POST'])
def location():
    form = LocationForm()    
    location_data = db.session.query(Location)
    location_data = [str(row).split('|') for row in location_data]

    if form.validate_on_submit():
        location = Location(location_name=form.location_name.data,\
                            city=form.city.data,\
                            lat_long=form.lat_long.data,\
                            address=form.address.data)

        try:
            obj = db.session.query(Location).filter(Location.location_name==form.location_name.data).first()
            if obj == None:
                db.session.add(location)
                db.session.commit()
                flash('Your location data has been saved successfully!')
            else:
                obj.update({"city" : form.city.data,\
                                     "lat_long" : form.lat_long.data,\
                                     "address" : form.address.data})
                db.session.commit()

            return redirect(url_for('location'))
        except IntegrityError as e:
            flash('Integrity error')

    return render_template('location.html', form=form, location_data=location_data,\
                            is_authenticated=current_user.is_authenticated)

@app.route('/location_delete/<location_name>', methods=['GET'])
def location_delete(location_name):
    location = db.session.query(Location).filter(Location.location_name==location_name).first()
    db.session.delete(location)
    db.session.commit()

    return redirect(url_for('location'))
        
@app.errorhandler(401)
def unauthorized(e):
    # note that we set the 404 status explicitly
    return "<h1>Unauthorized</h1>", 401






@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!')
            return redirect(url_for('login'))
        except IntegrityError as e:
            flash('Integrity error')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('location'))
        
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('location'))
            else:
                flash("User/password is not valid") 
        else:
            flash("User/password is not valid") 
            return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    from app.my_lib.titanic import Upload
    form = UploadForm()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        APP_ROOT = os.path.dirname(os.path.abspath(__file__))
        UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
        form.file.data.save(UPLOAD_FOLDER + "/" + filename)

        u = Upload()
        u.upload_to_db(UPLOAD_FOLDER + "/" + filename)

        flash('Your file has been uploaded successfully')
        return redirect(url_for('upload'))

    return render_template('upload.html', form=form,\
                            is_authenticated=current_user.is_authenticated)

@app.route('/titanic_chart')
@login_required
def titanic_chart():
    from app.my_lib.titanic import TitanicChart
    import json
    titanic_chart = TitanicChart()
    xtrace1, ytrace1, xtrace2, ytrace2, name1, name2, labels, count =\
         titanic_chart.titanic_chart()

    return render_template('titanic_chart.html',\
                            xtrace1=xtrace1,\
                                xtrace2=xtrace2,\
                                ytrace1=json.dumps(ytrace1),\
                                ytrace2=json.dumps(ytrace2),\
                                name1=json.dumps(name1),\
                                name2=json.dumps(name2),\
                                labels=json.dumps(labels),\
                                count=json.dumps(count),\
                                is_authenticated=current_user.is_authenticated)


@app.route('/location_map_1/<location_name>', methods=['GET'])
def location_map_1(location_name):
    obj = db.session.query(Location).filter(Location.location_name==location_name).first()
    if obj!=None:
        lat_long = list(ast.literal_eval(obj.lat_long.strip()))[:-2]
        lat_long.reverse()
        new_lat_long = list()
        long_idx = 1
        for idx, row in enumerate(lat_long[::2]):
            new_lat_long.append([row, lat_long[long_idx]])
            long_idx+=2

    return render_template('map_1.html', lat_long=new_lat_long)


@app.route('/location_map_2/<location_name>', methods=['GET'])
def location_map_2(location_name):
    import requests 
    URL = "http://pintar.ai:666/solr/user1/select?q=city%3AJakarta" +\
          "&wt=json&rows=0&fq=created_date:[2019-11-04T12:23:02.131Z%20TO%202019-11-04T13:50:46.209Z]" +\
          "&facet=true&facet.range=created_date&facet.range.start=2019-11-04T12:23:02.131Z&" +\
          "facet.range.end=2019-11-04T13:50:46.209Z&facet.range.gap=%2B1MINUTE"
    print(URL)
    
    r = requests.get(url = URL)
    data = r.json()
    obj = db.session.query(Location).filter(Location.location_name==location_name).first()
    if obj!=None:
        lat_long = list(ast.literal_eval(obj.lat_long.strip()))[:-2]
        lat_long.reverse()
        new_lat_long = list()
        long_idx = 1
        for idx, row in enumerate(lat_long[::2]):
            new_lat_long.append([row, lat_long[long_idx]])
            long_idx+=2
        intensity = data['response']['numFound'] * 100000
        radius = data['response']['numFound'] * 10
        latlong_intensity = list()
        latlong_intensity.append(new_lat_long[0][0])
        latlong_intensity.append(new_lat_long[0][1])
        latlong_intensity.append(intensity)
    return render_template('map_2.html', lat_long=new_lat_long[:2], latlong_intensity=latlong_intensity, radius=radius)