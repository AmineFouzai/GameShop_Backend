from model import *
from uuid import uuid4
from halo import Halo
import json
spinner=Halo(text_color="blue")
spinner.start()
try:    
    spinner.info(text="initializing test")
    #User test
    SessionID=str(uuid4())
    spinner.info(text="Creating User => ")
    user=User(name="usertest",email="usertest@gmail.com",password="userpassword",SessionID=SessionID)
    user.add_user()
    spinner.text_color="green"
    spinner.succeed(text="passed")
    print('+++++++++++++++++++++++++')
    spinner.text_color="blue"
    spinner.info(text="Recovering User =>")
    document=user.find_user_by_SessionID(SessionID)
    document['_id']=str(document['_id'])
    print(json.dumps(document, indent=4, sort_keys=True))
    spinner.text_color="green"
    spinner.succeed(text="passed")
    print('+++++++++++++++++++++++++')
    spinner.text_color="blue"
    spinner.info(text="Loging User =>")
    print(user.login(SessionID))
    spinner.text_color="green"
    spinner.succeed(text="passed")
except Exception as e:
    spinner.text_color="red"
    spinner.fail(str(e))
    raise e
spinner.stop()