from beton.models import Userinfo

class CheckUser:

    @staticmethod
    def check_user(username, password, email):
        obj =  Userinfo.objects.get(username=username.lower())
        if obj.password != password:
            return "error", "Password incorrect"
        return "success", "Password correct"

    @staticmethod
    def update_user(username, password, email):
        try:
            obj = Userinfo.objects.get(username=username)
            obj.emailID = email
            obj.save()
            return "success", "Update success"
        except Exception as e:
            return "exception", str(e)


    @staticmethod
    def get_user(username):
        print(username)
        try:
            obj = Userinfo.objects.get(username=username.lower())
            return {"status": "success" , "username" : obj.username, "email": obj.emailID }
        except Exception as e:
            return {"status": "exception", "message" : str(e)}
