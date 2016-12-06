from flask import Flask,request, render_template, g, redirect, Response,jsonify
import os,csv
from sqlalchemy import *
from sqlalchemy.pool import NullPool
import traceback

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
public_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, template_folder=tmpl_dir, static_folder=public_dir,static_url_path='')

#connect to database

host = "104.196.175.120" 
password ="rezq8"  
user =  "cl3469"
DATABASEURI = "postgresql://%s:%s@%s/postgres" % (user, password, host)

engine = create_engine(DATABASEURI)
# import logging

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request
  The variable g is globally accessible
  """
  try:
        g.conn = engine.connect()
  except:
        print "uh oh, problem connecting to database"
        traceback.print_exc()
        g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception:
    pass

@app.route('/insertM')
def insertM():

  # print to_id,from_id
  with open(public_dir+'/vc.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')

    cat ={}
    for row in spamreader:
      ct=0
      print row
      for e in row:
        if len(e)>0: ct+=1
      if ct == len(row):
        try:
           g.conn.execute("INSERT into movie values (%s,%s,%s,%s)",row[0],row[1],row[2],row[3])
        except Exception as e:
          print e
        try:
          try:
            cursor =  g.conn.execute("select tid from tags where TNAME=%s;",row[4])
            tid = cursor.fetchone()[0]
          except:
            cursor = g.conn.execute("INSERT into tags(TNAME) values (%s); select max(tid) from tags;",row[4])
            tid = cursor.fetchone()[0]

          g.conn.execute("INSERT into movie_tag(mid,tid) values(%s,%s);",row[0],tid)
        except Exception as e:
          print e
  # g.conn.execute("INSERT into msg values (%s,%s,%s,%s)",int(time.time()),from_id,to_id,text)

  return jsonify(data="ok")


@app.route('/getmid', methods=['GET'])
def getmid():
  uid = request.args.get('uid', 0, type=int)
  mid = request.args.get('mid', "", type=str)
  print uid, mid
  data={}
  try:
    cursor = g.conn.execute("select * from movie where MID=%s",mid)
    result = cursor.fetchone()
    if result != None:
      data["mid"]=result["mid"]
      data["name"]=result["name"]
      data["mlink"]=result["mlink"]
      data["mimg"]=result["mimg"]
  except Exception as e:
          print e


  try:
    ret =[]
    cursor = g.conn.execute("select movie.*,movie_tag.tid from movie_tag, movie where movie.mid=movie_tag.mid and movie.mid <> %s and movie_tag.tid in (select tid from movie_tag as t where t.mid=%s)",mid,mid)
    for result in cursor:
      in_data={}
      in_data["mid"]=result["mid"]
      in_data["name"]=result["name"]
      in_data["mlink"]=result["mlink"]
      in_data["mimg"]=result["mimg"]
      tid = result["tid"]
      ret.append(in_data)
  except Exception as e:
          print e
  
  try:
    cursor = g.conn.execute("select movie.* from movie_tag, movie where movie.mid=movie_tag.mid and movie_tag.tid <> %s order by random() limit 2",tid)
    for result in cursor:
      in_data={}
      in_data["mid"]=result["mid"]
      in_data["name"]=result["name"]
      in_data["mlink"]=result["mlink"]
      in_data["mimg"]=result["mimg"]
      ret.append(in_data)
  except Exception as e:
          print e
  
  data["rec_list"] = ret

  return jsonify(data=data)

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/signup')
def signup():
	return render_template('sign-up.html')

@app.route('/signin')
def signin():
	return render_template('sign-in.html')

@app.route('/home')
def home():
    return render_template('home.html')

##add a new user
@app.route('/adduser', methods=['POST'])
def adduser():
    try:
        PSW = str(request.form['PSW'])
        UName = str(request.form['UName'])
        EMAIL = str(request.form['EMAIL'])
        print PSW, UName,EMAIL
        profiles = g.conn.execute("Select UID from users where email=%s and psw=%s",EMAIL,PSW)
        if profiles:
            print profiles
            return render_template('sign-up.html', msg='User already existed!')
        else:
            g.conn.execute("INSERT INTO users(PSW, UName,EMAIL) VALUES (%s, %s, %s);",PSW, UName,EMAIL)
            profiles = g.conn.execute("Select UID from users where email=%s and psw=%s",EMAIL,PSW)
            for profile in profiles:
                UID=str(profile)[1]
            print UID
            redirect_to_index = render_template('/home.html',data="ok")
            response = app.make_response(redirect_to_index )
            response.set_cookie('uid',value=UID)
            response.set_cookie('name',value=UName)
            return response
    except:
        print traceback.print_exc()
        return 'Oops something goes wrong!'

##usersignin
@app.route('/login', methods=['POST'])
def login():
    try:
        PSW = str(request.form['PSW'])
        EMAIL = str(request.form['EMAIL'])
        print PSW, EMAIL
        profiles = g.conn.execute("Select UID from users where email=%s and psw=%s",EMAIL,PSW)
        UID=''
        for profile in profiles:
            UID=str(profile)[1]
        if UID:
            redirect_to_index = render_template('/home.html',data="ok")
            response = app.make_response(redirect_to_index )
            response.set_cookie('uid',value=UID)
            return response
        else:
            return render_template('sign-up.html', msg='User does not exist!')
    except:
        print traceback.print_exc()
        return 'Oops something goes wrong!'

if __name__ == '__main__':
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)
    def run(debug, threaded, host, port):
        """
        This function handles command line parameters.
        Run the server using

            python server.py

        Show the help text using

            python server.py --help

        """
        HOST, PORT = host, port
        print "running on %s:%d" % (HOST, PORT)
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


    run()
