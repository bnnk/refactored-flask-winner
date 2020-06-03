from flask import Flask,jsonify,request,send_file,json
from pyotp import *
from base64 import *
from qrcode import *
from base64 import standard_b64encode
from _io import BytesIO
app = Flask(__name__)
app.config["SECRET_KEY"] = "Flask OTP API V4"
@app.route("/getauthcode")
def get__():
        dict_ = json.loads(request.get_json())
        totp_ = totp.TOTP(dict_["auth_vendor_id"])
        return jsonify({"code":totp_.now()})
@app.route("/createuser")
def create():
        totp_ = totp.TOTP(random_base32())
        outn = BytesIO()
        img = make(totp_.provisioning_uri("python.access.server@gmail.com",issuer_name = "Cinara-Lyca Network Co.LTD"))
        img.save(outn)
        data = standard_b64encode(outn.getvalue())
        data_uri = "data:image/png;base64," + data.decode()
        return jsonify({"qr_code_url":data_uri,"auth_vendor_id":totp_.secret})
@app.route("/verify")
def verify():
        dict_ = json.loads(request.get_json())
        totp_ = totp.TOTP(dict_["auth_vendor_id"])
        condition = totp_.verify(dict_["code"])
        return jsonify(condition)
app.run()
