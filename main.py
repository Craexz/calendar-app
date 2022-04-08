from json.decoder import JSONDecodeError

from flask import Flask 
from flask import request
from flask import render_template
from flask import redirect

import random
import base64
import logging
import sys
import os
import time
import json
import threading

def installRequirements():
  os.system("pip install -q -r requirements.txt")
  os.system("pip install -q -–upgrade pip")
  
def divider(waitTime = 0):
  time.sleep(waitTime)
  print("\n\n" + "-"*60 + "\n\n")

banner = """
                ▄████▄   ▄▄▄        ██████ 
                ▒██▀ ▀█  ▒████▄    ▒██    ▒ 
                ▒▓█    ▄ ▒██  ▀█▄  ░ ▓██▄   
                ▒▓▓▄ ▄██▒░██▄▄▄▄██   ▒   ██▒
                ▒ ▓███▀ ░ ▓█   ▓██▒▒██████▒▒
                ░ ░▒ ▒  ░ ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░
                ░  ▒     ▒   ▒▒ ░░ ░▒  ░ ░
                ░          ░   ▒   ░  ░  ░  
                ░ ░            ░  ░      ░  
                ░                           

        Calendar App Server -- Developed by Ben Hershey 
"""

def slowprint(s):
  for c in s + '\n':
    sys.stdout.write(c)
    sys.stdout.flush()
    time.sleep(1./50)

def encode(text):
        text_bytes = text.encode("ascii")
        base64_bytes = base64.b64encode(text_bytes)
        return base64_bytes.decode("ascii")


def decode(text):
        text_bytes = text.encode("ascii")
        decoded_bytes = base64.b64decode(text_bytes)
        return decoded_bytes.decode("ascii")



def server(addr, port, logs):    
    log = logging.getLogger("werkzeug")
    
    log.disabled = not logs

    app = Flask(__name__,template_folder="html/",static_folder='assets/')


    def assignment_action_timeout_handler(user, deleteOrCreate, setOption = None):
        if setOption is None:
                return checkTrigger(user, f'{deleteOrCreate}Triggered.txt')

        if setOption == True:
                file = open(f"userData/{user}/{deleteOrCreate}Triggered.txt", "w")
                file.write("TRUE")     

        elif setOption == False:
                file = open(f"userData/{user}/{deleteOrCreate}Triggered.txt", "w")
                file.write("FALSE")



    def checkTrigger(user, fileName):
        user = user.replace(" ", "")
        file = open(f"userData/{user}/{fileName}", "r")
        data = file.read()
        return data == "TRUE"


    @app.route("/")
    def start():
        print("\n\n[INFO] User connected")

        username = request.cookies.get("username")
        token = request.cookies.get("token")

        if username is None:
            return render_template("index.html", checkedToken = "NO")
        try:

            path = f"userData/{username}/data.txt"

            file = open(path, "r")
            data = list(file.read().splitlines())

            tokenFile = open(f"userData/{username}/token.txt", "r")
            actualToken = tokenFile.read()

            if token == actualToken:
                return render_template(
                    "homepage.html", username=username, data=data, token=actualToken
                )

        except Exception:
            return render_template("index.html", checkedToken = "NO")


    @app.route("/login")
    def load_login():
        print("[SERVER] User loaded login screen")
        return render_template("login.html")

    @app.route("/loginwithtoken", methods = ['GET'])
    def loginwithtoken():
      try:
          token = request.args.get('token')
          username = request.args.get('username').replace(" ", "")
          path = f"userData/{username}/data.txt"
          file = open(path, "r")
          data = list(file.read().splitlines())
    
          assignment_action_timeout_handler(username, "delete", False)
          assignment_action_timeout_handler(username, "create", False)
    
    
          print("[SERVER] User successfully logged in")
    
          token_ = open(f"userData/{username}/token.txt", "r").read()
    
          if str(token).replace(" ", "") == token_:
            return render_template(
                    "homepage.html", username=username, data=data, token=token
                )
      except Exception:
        return render_template('index.html', checkedToken = "DONE")
    @app.route("/homepage", methods=["POST"])
    def homepage():
        global username_

        username_ = request.form["username"]
        password_ = request.form["password"]

        usernamefile = open("globalData/usernames.txt", "r")
        passwordfile = open("globalData/passwords.txt", "r")

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
            usernameindex = usernameindex

        except ValueError:
            print("[SERVER] User entered incorrect login info")
            return render_template("incorrectlogin.html")

        try:
            global passwordindex
            passwordindex = passwords.index(password_)
            passwordindex = passwordindex

        except ValueError:
            print("[SERVER] User entered incorrect login info")
            return render_template("incorrectlogin.html")

        if username_ in usernames and password_ in passwords and usernameindex == passwordindex:
            path = f"userData/{username_}/data.txt"

            file = open(path, "r")
            data = list(file.read().splitlines())

            assignment_action_timeout_handler(username, "delete", False)
            assignment_action_timeout_handler(username, "create", False)


            print("[SERVER] User successfully logged in")

            token = open(f"userData/{username_}/token.txt", "r").read()

            return render_template(
                "homepage.html", username=username_, data=data, token=token
            )

        else:
            print("[SERVER] User entered incorrect login info")
            return render_template("incorrectlogin.html")


    @app.route("/signup")
    def signup():
        print("[SERVER] User loaded signup page")
        return render_template("signup.html")


    @app.route("/post_signup", methods=["POST"])
    def post_signup():
        username = request.form["username"]
        password = request.form["password"]

        if username == "" or password == "":
            return render_template(
                "message.html", message="Credentials not allowed, try again"
            )

        usernamefile = open("globalData/usernames.txt", "r")

        username = encode(username)
        password = encode(password)

        userlist = usernamefile.read().splitlines()

        if username in userlist:
            print("[SERVER] User tried to make an account that is already taken")
            return render_template("accounttaken.html")
        else:
            try:
                import os

                directory = decode(username)
                parent_dir = "userData/"

                path = os.path.join(parent_dir, directory)
                
                os.mkdir(path)

                open(f'{str(path)}/data.txt', "x")
                open(f'{str(path)}/deleteTriggered.txt', "x")
                open(f'{str(path)}/createTriggered.txt', "x")
                open(f'{str(path)}/token.txt', "x")

                usedTokensFile = open("globalData/usedTokens.txt", "r")
                usedTokens = list(usedTokensFile.read().splitlines())
                tokenFound = False

                while not tokenFound:
                    tokenToTry = random.randint(100000000, 999999999)

                    if str(tokenToTry) in usedTokens:
                        tokenFound = False

                    else:
                        tokenFound = True
                        token = tokenToTry

                usedTokens.append(token)

                usedTokensFile = open("globalData/usedTokens.txt", "a")

                for usedToken in usedTokens:
                    usedTokensFile.write(str(usedToken))
                    usedTokensFile.write("\n")

                tokenFile = open(f'{str(path)}/token.txt', "w")
                tokenFile.write(str(token))

                passwordfile = open("globalData/passwords.txt", "a")
                usernamefile = open("globalData/usernames.txt", "a")

                usernamefile.write(f"{username} \n")

                passwordfile.write(f"{password} \n")

                print("[SERVER] User created a new account")

                return render_template("login.html")

            except FileExistsError:
                print("[SERVER] User tried to make an account that is already taken.")
                return render_template("accounttaken.html")


    @app.route("/createAssignment", methods=["POST"])
    def createAssignment():
        nameofuser = request.form["username_"].replace(" ", "")

        name = request.form["Name"]
        description = request.form["Description"]
        duedate = request.form["DueDate"]

        if assignment_action_timeout_handler(nameofuser, "create") == False:
            if not nameofuser:
                return render_template("homepage.html", username=nameofuser)

            file = open(f"userData/{nameofuser}/data.txt")
            lines = list(file.read().splitlines())
            length_ = len(lines)

            id_ = length_ + 1

            data_ = {
                "name": name,
                "description": description,
                "duedate": duedate,
                "id": id_,
            }

            path = f"userData/{nameofuser}/data.txt"

            import json

            try:

                with open(path, "r") as f:
                    data = f.read()

                data = str(data_) if data in ["", " "] else str(data) + "\n" + str(data_)

            except JSONDecodeError:
                data = data_

            with open(path, "w") as f:
                f.write(data)

            file = open(path, "r")
            data = list(file.read().splitlines())

            assignment_action_timeout_handler(nameofuser, "create", True)


            print("[SERVER] User created an assignment")

            return render_template("homepage.html", data=data, username=nameofuser)
        else:
            print("[SERVER] User resubmitted createAssignment method, but was handled.")

            assignment_action_timeout_handler(nameofuser, "create", False)

            return redirect(f"/createResubmitted?username={nameofuser}")


    @app.route("/deleteResubmitted")
    def deleteResubmitted():
        nameofuser = request.args.get("username")

        path = f"userData/{nameofuser}/data.txt"
        file = open(path, "r")
        data = list(file.read().splitlines())
        
        return render_template("homepage.html", data=data, username=nameofuser)


    @app.route("/createResubmitted")
    def createResubmitted():
        nameofuser = request.args.get("username")

        path = f"userData/{nameofuser}/data.txt"
        file = open(path, "r")
        data = list(file.read().splitlines())

        return render_template("homepage.html", data=data, username=nameofuser)


    @app.route("/deletebtn", methods=["GET"])
    def deletebtn():
        nameofuser = request.args.get("username")
        id_ = request.args.get("id_")
        if assignment_action_timeout_handler(nameofuser, "delete") == False:
            path = f"userData/{nameofuser}/data.txt"
            file = open(path, "r")

            i = 1
            for line in file.read().splitlines():
                if i == int(id_):
                    linetodelete = line
                    break
                else:
                    i = i + 1

            with open(path, "r") as file:
                lines = file.readlines()

            with open(path, "w") as newfile:
                for line in lines:
                    try:
                        if line.strip("\n") != linetodelete:
                            newfile.write(line)
                    except UnboundLocalError as e:
                        print(e)

            file = open(path, "r")
            data = list(file.read().splitlines())

            assignment_action_timeout_handler(nameofuser, "delete", True)

            print("[SERVER] User deleted a button")

            return render_template("homepage.html", data=data, username=nameofuser)
        else:
            print("[SERVER] User resubmitted deleteBtn method, but was handled.")

            assignment_action_timeout_handler(nameofuser, "delete", False)

            return redirect(f"/deleteResubmitted?username={nameofuser}")


    app.run(host=addr, port=port)

if __name__ == "__main__":
    installRequirements()
  
    currentPlatform = sys.platform

    if currentPlatform == "win32":
        os.system('cls')
    else:
        os.system('clear')
    
    print(banner)

    configFile = open("config.json")
    json = json.load(configFile)

    port = json['port']
    addr = json['ip']
    logs = json['logs']

    configStats = ("""
                  Settings in config.json  
          
                      Port >> """+str(port)+"""      
                      IPv4 >> """+str(addr)+"""
                      Logs >> """+str(logs)+"""                              
    """)

    print(configStats)

    input("                Press enter to start server")
  
    divider()

    T = threading.Thread(target=divider, args = [.1])
    T.start()
   
    server(addr, port, logs)