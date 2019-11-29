from flask import Flask, render_template,url_for
from flask import request, redirect, session
from pymongo import MongoClient
import re

try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")
db=conn.database
eng_elec_base=db.eng_electronics_and_communications
eng_comp_base=db.eng_computer_science
ans=eng_elec_base.find()
ans_computer=eng_comp_base.find()
eng_electro_base=db.electrical_and_electronics
ans_electrical=eng_electro_base.find()
eng_mechanicals=db.eng_mechanical
ans_mechanical=eng_mechanicals.find()

eng_info=db.eng_information_technology
ans_information_technology=eng_info.find()

eng_chemicals=db.eng_chemical
ans_chemical=eng_chemicals.find()

eng_civils=db.eng_civil
ans_civil=eng_civils.find()

eng_aeros=db.eng_aero
ans_aero=eng_aeros.find()

eng_agris=db.eng_agri
ans_agri=eng_agris.find()


def get_jaccard_sim(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


app = Flask(__name__,static_url_path='/static')
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')
@app.route('/colleges/')
def college():
    return render_template('college.html')

@app.route('/courses/')
def courses():
    return render_template('single-college-page.html')
@app.route('/electronics_colleges/')
def search_electronics_and_communication():
    return render_template('electronics_and_communication.html',author='sony', tables=ans)
@app.route('/electrical_colleges/')
def search_electrical_and_electronics():
    return render_template('electrical_and_electronics.html',author='sony', tables=ans_electrical)

@app.route('/computer_colleges/')
def search_computer_science():
    return render_template('computer_science.html',author='sony', tables=ans_computer)

@app.route('/mechanical/')
def search_mechanical():
    return render_template('mechanical.html',author='sony', tables=ans_mechanical)

@app.route('/information_technology/')
def search_information():
    return render_template('information_technology.html',author='sony', tables=ans_information_technology)


@app.route('/chemical/')
def search_chemical():
    return render_template('chemical.html',author='sony', tables=ans_chemical)

@app.route('/civil/')
def search_civil():
    return render_template('civil.html',author='sony', tables=ans_civil)

@app.route('/aero/')
def search_aero():
    return render_template('aero.html',author='sony', tables=ans_aero)

@app.route('/agri/')
def search_agri():
    return render_template('agri.html',author='sony', tables=ans_agri)

@app.route('/quiz/')
def quiz():
    return render_template('quiz.html')



@app.route('/signup/')
def signup():
    return render_template('signup.html')

@app.route('/login/')
def login():
    return render_template('login.html')

@app.route('/search_result/', methods=['post', 'get'])
def search_result():
    username = request.form.get('res')
    print(username)
    return render_template('search_result.html')

''''@app.route('/search_result/', methods=['post', 'get'])
def search_result():
    message = ''
    if request.method == 'POST':
        username = request.form.get('res')  # access the data inside
    db = conn.database
    user_data = db.eng_computer_science
    regx = re.compile(username, re.IGNORECASE)
    s = r2d2_base.find({regx})
    return render_template('search_result.html',author='sony', tables=s)'''


@app.route('/signup/', methods=['post', 'get'])
def signup_next():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')  # access the data inside
        password = request.form.get('pass')
    print(username,'\n',password)
    db = conn.database
    user_data = db.login
    pos1 = {'Name': username,
            'Password':password}
    user_data.insert_one(pos1)
    return render_template('signup.html')

@app.route('/login/', methods=['post', 'get'])
def login_next():
    message = ''
    if request.method == 'POST':
        username = request.form.get('names')  # access the data inside
        password = request.form.get('pwd')
        email=request.form.get('email')
    print(email,'\n',username,'\n',password)
    db = conn.database
    user_data = db.user_data
    pos1 = {'Name': username,
            'Email': email,
            'Password':password}
    user_data.insert_one(pos1)
    return render_template('login.html')
username=""
email=""
dob=""
branch=""
f2=""
@app.route('/quiz/', methods=['post', 'get'])
def quiz_next():
    message = ''
    if request.method == 'POST':
        username = request.form.get('names')  # access the data inside
        email=request.form.get('email')
        dob = request.form.get('dob')
        branch = request.form.get('branch')
        f2 = request.form.get('pwdc')
    print(email,'\n',username,'\n',dob,'\n',branch)
    db = conn.database
    user_data = db.career
    pos1 = {'Name': username,
            'Email': email,
            'dob':dob,
            'branch':branch,
            'feild':f2}
    user_data.insert_one(pos1)
    values=[]

    career = db.careers
    ans=career.find()
    for i in ans:
        s=""
        x=i['keywords']
        names = []
        for j in x:
            s=s+str(j)+' '
        #print(s)
        curr_ans=get_jaccard_sim(f2,s)
        #print(curr_ans)
        names.append(i['degree'])
        names.append(curr_ans)
        values.append(names)
    values.sort(key = lambda x: x[1],reverse=True)
    for i in values[:3]:
        print(i[0])
    return render_template('quiz_result.html',tables=values[:5])




if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True)