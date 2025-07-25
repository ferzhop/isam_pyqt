import jwt
import datetime

SECRET_KEY = "isam_secret_key"

class AuthManager:
    @staticmethod
    def generate_token(username):
        payload = {
            "user": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return payload["user"]
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
