from flask import Flask, request, render_template, redirect
import urllib.parse, urllib.request, urllib.error, json, time
CLIENT_ID = '1260113467868987'
CLIENT_SECRET='1df80be64b333fc0ab9b892430370205'
TOKEN='IGQVJWbWFjS3JmendEYk5Ibzh2bXdmQ01wby0zNlR1MzFGdjNaaGZAON1lEVmRjcVVMbnZAGa1V4b21aQWN4OWtCaEJWaVZA1RzI1YldndnNENWhnU0t5OGN3MXMwbGx1ZAXF1M29xeTNOalJQbS1HMlBNegZDZD'
# By default, App Engine will look for an app called `app` in `main.py`.
app = Flask(__name__)
@app.route("/")
def main():
    name =  request.args.get('username')
    content = render_template("submitform.html",hello="hi")
    return content
    
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
        #headers = {'content-type': 'application/x-www-form-urlencoded'}
        url = "  https://api.instagram.com/oauth/access_token"
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req,data=data)
        response_dict = json.loads(response.read())
        access_token = response_dict["access_token"]
        user_id = response_dict["user_id"] 

        #GET profile now
        user_url = "https://graph.instagram.com/" + str(user_id) + "?fields=id,username&access_token=" + str(access_token)
        user_res = json.loads(safe_get(user_url).read())
        username = user_res['username']

        content = render_template("submitform.html",hello="hi",ig=username)
        return content
    
    else:
        #GET verification code if not got
        args = {}
        args['client_id']= CLIENT_ID
        args['redirect_uri']=request.base_url
        args['scope']='user_profile,user_media'
        args['response_type']='code'
        url = "https://api.instagram.com/oauth/authorize?" + urllib.parse.urlencode(args)
        return redirect(url)

if __name__ == "__main__":
# Used when running locally only. 
# When deploying to Google AppEngine, a webserver process will
# serve your app. 
    app.run(host="localhost", port=8080, debug=True)

# def pretty(obj):
#     return json.dumps(obj, sort_keys=True, indent=2)

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

# baseurl = "https://ridb.recreation.gov/api/v1/"
# apikey = "921d7a47-53b3-44be-94ea-9a13ed3af560"
# def get_places(latitude=47.653457, longitude=-122.30755, radius=5, state="CA"):
#     params = {}
#     params["latitude"] = latitude
#     params["longitude"] = longitude
#     params["radius"] = radius
#     # params["state"] = state
#     params["limit"] = 10
#     params["apikey"] = apikey
#     requesturl = baseurl + "recareas?" + urllib.parse.urlencode(params)
#     print(requesturl)
#     return json.loads(safe_get(requesturl).read())

# def show_places(latitude=44.459095, longitude = -110.603442, radius=5, state="CA"):
#     obj = get_places(latitude, longitude, radius)
#     print("found %d rec areas within %d miles:"%(obj["METADATA"]["RESULTS"]["TOTAL_COUNT"],radius))
#     for recarea in obj["RECDATA"]:
#         distance = math.sqrt((latitude-recarea["RecAreaLatitude"])**2 + (longitude-recarea["RecAreaLongitude"])**2)*54.6
#         print("\t"+recarea["RecAreaName"])
#         requesturl = baseurl + "/recareas/{}/facilities".format(recarea["RecAreaID"]) + "?apikey=" + apikey
#         facilities = json.loads(safe_get(requesturl).read())
#         for fac in facilities["RECDATA"]:
#             print("\t\t"+fac["FacilityName"])

# show_places(44.459095, -110.603442, 25)