from flask import Flask, jsonify, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random
'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///D:\project\python\66-starting-files-cafe-api\instance\cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    # seats: Mapped[str] = mapped_column(String(250), nullable=False)
    # has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    # has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    # has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    # can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    # coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    
    def to_dict(self):
        dictionary= {}
        for coulmn in self.__table__.columns:
            dictionary[coulmn.name]=getattr(self,coulmn.name)
        return dictionary


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

# HTTP GET - Read Record
@app.route('/random',methods=["GET"])
def get_random_cafe():
    
    result= Cafe.query.order_by(Cafe.id).all()
    random_cafe = random.choice(result)
    return jsonify(cafe=random_cafe.to_dict())
# HTTP POST - Create Record
@app.route('/all',methods=['GET'])
def all_cafe():
    result= Cafe.query.order_by(Cafe.id).all()
    cafes=[cafe.to_dict() for cafe in result]
    print(cafes)
    return render_template('index.html',cafe=cafes)

@app.route("/search")
def get_cafe_at_location():
    query_location = request.args.get("loc")
    all_cafes = Cafe.query.filter(Cafe.location.ilike(f"%{query_location}%")).all()
    # Note, this may get more than one cafe per location

    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."}), 404

# HTTP DELETE - Delete Record
@app.route("/add",methods=["POST"])
def add():
    new_cafe =Cafe(
        name=request.form.get("name"),
        location=request.form.get("location"),
        map_url= request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        # has_sockets=bool(request.form.get("sockets")),
        # has_toilet=bool(request.form.get("toilet")),
        # has_wifi=bool(request.form.get("wifi")),
        # can_take_calls=bool(request.form.get("calls")),
        # seats=request.form.get("seats"),
        # coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"sucessfull":"cafe added successfully "})

if __name__ == '__main__':
    app.run(debug=True)
