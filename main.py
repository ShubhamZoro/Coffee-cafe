from flask import Flask, render_template, redirect,url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,FloatField,BooleanField,URLField
from wtforms.validators import DataRequired

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)

    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)
    open = db.Column(db.String(250),nullable=False)
    close = db.Column(db.String(250),nullable=False)
    cafe_rating=db.Column(db.String(250),nullable=False)



class CafeForm(FlaskForm):
    cafe_name = StringField('Cafe name', validators=[DataRequired()])
    map_url=URLField("Cafe_location_url",validators=[DataRequired()])
    img_url=URLField("Cafe_Image",validators=[DataRequired()])
    seats=BooleanField("has_seats",validators=[DataRequired()])
    Location=StringField('Location',validators=[DataRequired()])
    open=StringField('Open',validators=[DataRequired()])
    close=StringField('Close',validators=[DataRequired()])
    cafe_rating= StringField("Cafe Rating",
                                validators=[DataRequired()])
    wifi= BooleanField("Wifi Strength Rating",
                              validators=[DataRequired()])

    has_toilet=BooleanField("Toilet",validators=[DataRequired()])
    coffee_price=FloatField("Price",validators=[DataRequired()])
    can_take_calls=BooleanField("can_talk_calls",validators=[DataRequired()])
    submit = SubmitField('Submit')

class UpdateForm(FlaskForm):
    cafe_name = StringField('Cafe name', validators=[DataRequired()])
    map_url = URLField("Cafe_location_url", validators=[DataRequired()])
    img_url = URLField("Cafe_Image", validators=[DataRequired()])
    coffee_price = FloatField("Price", validators=[DataRequired()])
    Location = StringField('Location', validators=[DataRequired()])
    open = StringField('Open', validators=[DataRequired()])
    close = StringField('Close', validators=[DataRequired()])
    submit = SubmitField('Submit')
db.create_all()
# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST","GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        add_cafe = Cafe(
            name=form.cafe_name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.Location.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.wifi.data,
            can_take_calls=form.can_take_calls.data,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
            open=form.open.data,
            close=form.close.data,
            cafe_rating=form.cafe_rating.data

        )
        db.session.add(add_cafe)
        db.session.commit()
        return redirect(url_for('cafes'))

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    cafes = db.session.query(Cafe).all()
    print(len(cafes))
    print(type(cafes))
    return render_template('cafes.html', cafes=cafes)





@app.route("/delete/<int:cafe_id>")
def delete_post(cafe_id):
    post_to_delete = Cafe.query.filter_by(id=cafe_id).first()
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('cafes'))

if __name__ == '__main__':
    app.run(debug=True)
