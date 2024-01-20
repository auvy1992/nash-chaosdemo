import os
import redis

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)


myHostname = os.environ['REDIS_HOST']
myPassword = os.environ['REDIS_PASSWORD']

app = Flask(__name__)
r = redis.StrictRedis(host=myHostname, port=6380,
                      password=myPassword, ssl=True)


@app.route('/loaderio-c4f75562dbae5ba7a16d3b3b430ee149/')
def loader_io():
  return "loaderio-c4f75562dbae5ba7a16d3b3b430ee149"

@app.route('/')
def index():
  
   result = r.ping()
   print("Ping returned : " + str(result))

   result = r.set("Message", "Hello!, The cache is working with Python!")
   print("SET Message returned : " + str(result))

   result = r.get("Message")
   print("GET Message returned : " + result.decode("utf-8"))

   result = r.client_list()
   print("CLIENT LIST returned : ")
   for c in result:
       print(f"id : {c['id']}, addr : {c['addr']}")
      
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()
