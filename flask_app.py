from flask import Flask, request, render_template, redirect
import urllib.parse, urllib.request, urllib.error, json, time
global access_token
global user_id
global artist
artist={}
CLIENT_ID = '1260113467868987'
CLIENT_SECRET='1df80be64b333fc0ab9b892430370205'
TOKEN='IGQVJWbWFjS3JmendEYk5Ibzh2bXdmQ01wby0zNlR1MzFGdjNaaGZAON1lEVmRjcVVMbnZAGa1V4b21aQWN4OWtCaEJWaVZA1RzI1YldndnNENWhnU0t5OGN3MXMwbGx1ZAXF1M29xeTNOalJQbS1HMlBNegZDZD'
# By default, App Engine will look for an app called `app` in `main.py`.
app = Flask(__name__)
@app.route("/")
def main():
    return render_template("ig.html")

@app.route("/getIG")
def getIG():
    verification_code = request.args.get("code")
    if verification_code:
        args = {}
        args['client_id']= CLIENT_ID
        args['client_secret']=CLIENT_SECRET
        args['grant_type']="authorization_code"
        args['redirect_uri']=request.base_url #'https://tootopus.pythonanywhere.com/'
        args['code']=verification_code
        data = urllib.parse.urlencode(args).encode("utf-8")
        # We need to make a POST request
        url = "  https://api.instagram.com/oauth/access_token"
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req,data=data)
        response_dict = json.loads(response.read())
        global access_token 
        access_token = response_dict["access_token"]
        global user_id
        user_id = response_dict["user_id"] 
        #GET profile now
        user_url = "https://graph.instagram.com/" + str(user_id) + "?fields=id,username&access_token=" + str(access_token)
        user_res = json.loads(safe_get(user_url).read())
        global artist
        # newartist=artist
        # newartist['ig'] = user_res['username']
        artist={'ig': user_res['username']}
        return render_template("info.html",ig=artist['ig'])
    else:
        #GET verification code if not got
        args = {}
        args['client_id']= CLIENT_ID
        args['redirect_uri']=request.base_url
        args['scope']='user_profile,user_media'
        args['response_type']='code'
        url = "https://api.instagram.com/oauth/authorize?" + urllib.parse.urlencode(args)
        return redirect(url)

@app.route("/info")
def getInfo():
    global artist
    if 'ig' in artist:
        return render_template("info.html", ig=artist['ig'])
    return render_template("info.html", ig='')

@app.route("/works")
def pickWorks():
    global artist
    if 'ig' in artist:
        global user_id
        global access_token
        user_url = "https://graph.instagram.com/" + str(user_id) + "?fields=id,media,media_count,username&access_token=" + str(access_token)
        user_res = json.loads(safe_get(user_url).read())
        media = user_res['media']
        media_list = []
        for post in media['data']:
            user_url = "https://graph.instagram.com/" + str(post['id']) + "?fields=id,media_url&access_token=" + str(access_token)
            user_res = json.loads(safe_get(user_url).read())
            media_list.append(user_res)
        content = render_template("works.html",ig=artist['ig'], media=media_list)
        artist = request.args
    else:
        artist = request.args
        # artist['site']='https://www.instagram.com/'+ artist['ig']
        content = render_template("done.html",artist=artist, media=[])
    return content

@app.route("/done")
def done():
    global artist
    photoids = request.args.get('photoids')
    media_list = []
    if photoids:
        global user_id
        global access_token
        for pid in photoids.split(","):
            user_url = "https://graph.instagram.com/" + pid + "?fields=id,media_url&access_token=" + str(access_token)
            user_res = json.loads(safe_get(user_url).read())
            media_list.append(user_res)
    # artist['site']='https://www.instagram.com/'+ artist['ig']
    content = render_template("done.html",artist=artist, media=media_list)
    return content



# for pickWorks()
    # verification_code = request.args.get("code")
    # if verification_code:
    #     args = {}
    #     args['client_id']= CLIENT_ID
    #     args['client_secret']=CLIENT_SECRET
    #     args['grant_type']="authorization_code"
    #     args['redirect_uri']=request.base_url #'https://tootopus.pythonanywhere.com/'
    #     args['code']=verification_code
    #     data = urllib.parse.urlencode(args).encode("utf-8")
    #     # We need to make a POST request
    #     #headers = {'content-type': 'application/x-www-form-urlencoded'}
    #     url = "  https://api.instagram.com/oauth/access_token"
    #     req = urllib.request.Request(url)
    #     response = urllib.request.urlopen(req,data=data)
    #     response_dict = json.loads(response.read())
    #     access_token = response_dict["access_token"]
    #     user_id = response_dict["user_id"] 

    #     #GET works now
    #     user_url = "https://graph.instagram.com/" + str(user_id) + "?fields=id,media,media_count,username&access_token=" + str(access_token)
    #     user_res = json.loads(safe_get(user_url).read())
    #     media = user_res['media']

    #     media_list = []
    #     for post in media['data']:
    #         user_url = "https://graph.instagram.com/" + str(post['id']) + "?fields=media_url&access_token=" + str(access_token)
    #         user_res = json.loads(safe_get(user_url).read())
    #         media_list.append(user_res)

    #     content = render_template("works.html",ig=username, media=media_list)
    #     return content
    
    # else:
    #     #GET verification code if not got
    #     args = {}
    #     args['client_id']= CLIENT_ID
    #     args['redirect_uri']=request.base_url
    #     args['scope']='user_profile,user_media'
    #     args['response_type']='code'
    #     url = "https://api.instagram.com/oauth/authorize?" + urllib.parse.urlencode(args)
    #     return redirect(url)

if __name__ == "__main__":
# Used when running locally only. 
# When deploying to Google AppEngine, a webserver process will
# serve your app. 
    app.run(host="localhost", port=8080, debug=True)

def safe_get(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        if hasattr(e, 'code'):
            print("server couldn't fulfil the request")
            print("Error code: ", e.code)
        elif hasattr(e, 'reason'):
            print("failed to reach a server")
            print("Reason: ", e.reason)
    return None