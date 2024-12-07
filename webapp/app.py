from flask import Flask, render_template, request
from pymysql import connections
import os
import requests

app = Flask(__name__)

# Database Configuration
DBHOST = os.environ.get("DBHOST", "localhost")
DBUSER = os.environ.get("DBUSER", "root")
DBPWD = os.environ.get("DBPWD", "password")
DATABASE = os.environ.get("DATABASE", "employees")
COLOR_FROM_ENV = os.environ.get('APP_COLOR', "lime")
IMAGE_URL = os.environ.get("BACKGROUND_IMAGE", "")
GROUP_NAME = os.environ.get("GROUP_NAME", "Default Group")

DBPORT = int(os.environ.get("DBPORT", 3306))

# Create a connection to the MySQL database
db_conn = connections.Connection(
    host=DBHOST,
    port=DBPORT,
    user=DBUSER,
    password=DBPWD,
    db=DATABASE
)

# Define the path for static downloads
DOWNLOADS_PATH = "static/downloads"
if not os.path.exists(DOWNLOADS_PATH):
    os.makedirs(DOWNLOADS_PATH)

# Download the background image from the S3 URL
IMAGE_PATH = os.path.join(DOWNLOADS_PATH, "background.jpg")
try:
    if IMAGE_URL:
        response = requests.get(IMAGE_URL, timeout=10)  # Set a timeout for the request
        if response.status_code == 200:
            with open(IMAGE_PATH, "wb") as f:
                f.write(response.content)
            print("Background image downloaded successfully.")
        else:
            print(f"Failed to download background image. HTTP Status: {response.status_code}")
except Exception as e:
    print(f"Error downloading background image: {e}")

# Set the path for Flask to use
BACKGROUND_IMAGE_PATH = "/" + IMAGE_PATH

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('addemp.html', background_image=BACKGROUND_IMAGE_PATH, GROUP_NAME=GROUP_NAME)

@app.route("/about", methods=['GET', 'POST'])
def about():
    return render_template('about.html', background_image=BACKGROUND_IMAGE_PATH, GROUP_NAME=GROUP_NAME)

@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    primary_skill = request.form['primary_skill']
    location = request.form['location']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    try:
        cursor.execute(insert_sql, (emp_id, first_name, last_name, primary_skill, location))
        db_conn.commit()
        emp_name = f"{first_name} {last_name}"
    finally:
        cursor.close()

    return render_template('addempoutput.html', name=emp_name, background_image=BACKGROUND_IMAGE_PATH, GROUP_NAME=GROUP_NAME)

@app.route("/getemp", methods=['GET', 'POST'])
def GetEmp():
    return render_template("getemp.html", background_image=BACKGROUND_IMAGE_PATH, GROUP_NAME=GROUP_NAME)

@app.route("/fetchdata", methods=['GET', 'POST'])
def FetchData():
    emp_id = request.form['emp_id']

    output = {}
    select_sql = "SELECT emp_id, first_name, last_name, primary_skill, location FROM employee WHERE emp_id=%s"
    cursor = db_conn.cursor()

    try:
        cursor.execute(select_sql, (emp_id,))
        result = cursor.fetchone()
        if result:
            output["emp_id"] = result[0]
            output["first_name"] = result[1]
            output["last_name"] = result[2]
            output["primary_skills"] = result[3]
            output["location"] = result[4]
        else:
            return "No employee found with the given ID", 404
    except Exception as e:
        print(e)
        return "An error occurred while fetching data", 500
    finally:
        cursor.close()

    return render_template(
        "getempoutput.html",
        id=output["emp_id"],
        fname=output["first_name"],
        lname=output["last_name"],
        interest=output["primary_skills"],
        location=output["location"],
        background_image=BACKGROUND_IMAGE_PATH,
        GROUP_NAME=GROUP_NAME
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81, debug=True)
