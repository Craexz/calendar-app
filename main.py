from json.decoder import JSONDecodeError
from flask import Flask, request, render_template, redirect
import random, base64
 
import logging
log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__)

def encode(text):
    text_bytes = text.encode('ascii')
    base64_bytes = base64.b64encode(text_bytes)
    encoded = base64_bytes.decode('ascii')
    return encoded

def decode(text):
    text_bytes = text.encode('ascii')
    decoded_bytes = base64.b64decode(text_bytes)
    decoded = decoded_bytes.decode('ascii')
    return decoded

def triggerDeleteSubmitted(user):
    file = open('users/'+user+"/deleteTriggered.txt", 'w')
    file.write("TRUE")

def triggerDeleteNotSubmitted(user):
    file = open('users/'+user+"/deleteTriggered.txt", 'w')
    file.write("FALSE")

def checkDeletedTriggered(user):
    file = open('users/'+user+"/deleteTriggered.txt", 'r')
    data = file.read()
    if data == "TRUE":
        return True
    else:
        return False



def triggerCreateSubmitted(user):
    file = open('users/'+user+"/createTriggered.txt", 'w')
    file.write("TRUE")

def triggerCreateNotSubmitted(user):
    file = open('users/'+user+"/createTriggered.txt", 'w')
    file.write("FALSE")

def checkCreateTriggered(user):
    file = open('users/'+user+"/createTriggered.txt", 'r')
    data = file.read()
    if data == "TRUE":
        return True
    else:
        return False

      


@app.route('/')   
def start():
    print("User connected")
    return render_template('index.html')


@app.route("/login")
def load_login():
    print("User loaded login screen")
    return render_template("login.html")

@app.route('/homepage', methods=['POST'])
def homepage():
    global username_
    username_ = request.form['username']
    password_ = request.form['password']

    usernamefile = open("src/usernames.txt", 'r')
    passwordfile = open('src/passwords.txt', 'r')
    passlist = passwordfile.read().splitlines()
    userlist = usernamefile.read().splitlines()
    usernames = []
    passwords = []

    for username in userlist:
        username = decode(username)
        usernames.append(username)

    for password in passlist:
        password = decode(password)
        passwords.append(password)

    try:  
        global usernameindex
        usernameindex = usernames.index(username_)
        usernameindex = int(usernameindex)
    except ValueError:
        print("User entered incorrect login info")
        return render_template("incorrectlogin.html")

    try:  
        global passwordindex
        passwordindex = passwords.index(password_)
        passwordindex = int(passwordindex)
    except ValueError:
        print("User entered incorrect login info")
        return render_template("incorrectlogin.html")

    if username_ in usernames and password_ in passwords:
        if usernameindex == passwordindex:
                path = 'users/'+username_+"/data.txt"
                file = open(path, 'r')
                data = []
                for line in file.read().splitlines():
                    data.append(line)
                triggerDeleteNotSubmitted(username)
                triggerCreateNotSubmitted(username)
                print("User successfully logged in")
                return render_template('homepage.html', username = username_, data = data)
        else:
            print("User entered incorrect login info")
            return render_template("incorrectlogin.html")
    else:
        print("User entered incorrect login info")
        return render_template("incorrectlogin.html")

@app.route('/signup')
def signup():
    print("User loaded signup page")
    return render_template("signup.html")

@app.route('/post_signup', methods=['POST'])
def post_signup():
    username = request.form['username']
    password = request.form['password']
    if username == '' or password == '':
        return render_template("message.html",
                               message='Credentials not allowed, try again')
    passwordfile = open("src/passwords.txt", 'r')
    usernamefile = open('src/usernames.txt', 'r')

    password = encode(password)

    username = encode(username)

    passlist = passwordfile.read().splitlines()
    userlist = usernamefile.read().splitlines()

    if password in passlist and username in userlist:
        print("User tried to make an account that is already taken")
        return render_template("accounttaken.html")
    else:
        try:
            import os 
            parent_dir = "users/"
            directory = decode(username)
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)

            open(str(path)+'/data.txt', 'x')
            open(str(path)+'/deleteTriggered.txt', 'x')
            open(str(path)+'/createTriggered.txt', 'x')

            passwordfile = open("src/passwords.txt", 'a')
            usernamefile = open('src/usernames.txt', 'a') 
            usernamefile.write(username)
            usernamefile.write('\n')
            passwordfile.write(password)
            passwordfile.write('\n')
            print("User created a new account")
            return render_template("login.html")
        except FileExistsError:
            print("User tried to make an account that is already taken.")
            return render_template("accounttaken.html")

@app.route("/createAssignment", methods = ["POST"])
def createAssignment():
        nameofuser = request.form['username_']
        nameofuser = nameofuser.replace(" ", "")
        name = request.form['Name']
        description = request.form['Description']
        duedate = request.form['DueDate']
  
        if checkCreateTriggered(nameofuser) == False:
          if nameofuser:
              file = open('users/'+nameofuser+"/data.txt")
              lines = []
              for line in file.read().splitlines():
                  lines.append(line)
              length_ = len(lines)
              
              id_ = length_+1
  
              data_ = {
                  'name': name,
                  'description': description,
                  'duedate': duedate,
                  'id': id_
              }
  
              path = 'users/'+nameofuser+"/data.txt"
  
              import json
              try:
  
                  with open(path, "r") as f:  
                      data = f.read()  
                  if data == "" or data == " ":
                      data = str(data_)
                  else:
                      data = str(data)+"\n"+str(data_)
              except JSONDecodeError:
                  data = data_
              with open(path, 'w') as f:
                  f.write(data)
  
              file = open(path, 'r')
              data = []
              for line in file.read().splitlines():
                  data.append(line)

              triggerCreateSubmitted(nameofuser)
              print("User created an assignment")
              return render_template('homepage.html', data = data, username = nameofuser)
          else:
              return render_template('homepage.html', username = nameofuser)
        else:
          print("User resubmitted createAssignment method, but was handled.")
          triggerCreateNotSubmitted(nameofuser)
          return redirect("/createResubmitted?username="+nameofuser)
@app.route('/deleteResubmitted')
def deleteResubmitted():
     nameofuser = request.args.get("username")
     path = 'users/'+nameofuser+"/data.txt"
     file = open(path, 'r')
     data = []
     for line in file.read().splitlines():
           data.append(line)

     return render_template('homepage.html', data = data, username = nameofuser)

@app.route('/createResubmitted')
def createResubmitted():
     nameofuser = request.args.get("username")
     path = 'users/'+nameofuser+"/data.txt"
     file = open(path, 'r')
     data = []
     for line in file.read().splitlines():
           data.append(line)

     return render_template('homepage.html', data = data, username = nameofuser)

@app.route('/deletebtn', methods = ["GET"])
def deletebtn():
                nameofuser = request.args.get("username")
                id_ = request.args.get("id_")
                if checkDeletedTriggered(nameofuser) == False:
                    path = 'users/'+nameofuser+"/data.txt"
                    file = open(path, 'r')
                    i = 1
                    for line in file.read().splitlines():
                        if i == int(id_):
                            linetodelete = line
                            break
                        else:
                            i = i+1

                    

                    file = open(path, "r")
                    lines = file.readlines()
                    file.close()

                    newfile = open(path, "w")
                    for line in lines:
                        try:
                            if line.strip("\n") != linetodelete:
                                newfile.write(line)
                        except UnboundLocalError as e:
                            print(e)
                            pass

                    newfile.close()

                    file = open(path, 'r')
                    data = []
                    for line in file.read().splitlines():
                        data.append(line)
                    triggerDeleteSubmitted(nameofuser)
                    print("User deleted a button")
                    return render_template('homepage.html', data = data, username = nameofuser)
                else: 
                    print("User resubmitted deleteBtn method, but was handled.")
                    triggerDeleteNotSubmitted(nameofuser)
                    return redirect("/deleteResubmitted?username="+nameofuser)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
