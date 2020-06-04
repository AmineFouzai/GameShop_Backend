from model import *
from uuid import uuid4
from halo import Halo
import json

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
    spinner.info(text="Creating Game => ")
    game1=Game(title="game1",description="game1 description",file_name="game1.exe",user_id="11111111")
    game2=Game(title="game2",description="game2 description",file_name="game2.exe",user_id="22222222")
    game3=Game(title="game3",description="game3 description",file_name="game3.exe",user_id="33333333")
    iserted_id=game1.add().inserted_id
    game2.add()
    game3.add()
    spinner.text_color="green"
    spinner.succeed(text="passed")
    print('+++++++++++++++++++++++++')
    spinner.text_color="blue"
    spinner.info(text="Recovering Games =>")
    docs=Game()
    print(json.dumps(docs.get(), indent=4, sort_keys=True))
    spinner.text_color="green"
    spinner.succeed(text="passed")
    print('+++++++++++++++++++++++++')
    spinner.text_color="blue"
    spinner.info(text="Recovering Game by id =>")
    print(json.dumps(game1.find_one_by_id(iserted_id), indent=4, sort_keys=True))
    spinner.text_color="green"
    spinner.succeed(text="passed")
    print('+++++++++++++++++++++++++')
    spinner.text_color="blue"
    spinner.info(text=" Deleting game by id =>")
    print(json.dumps(game1.delete(iserted_id), indent=4, sort_keys=True))
    spinner.text_color="green"
    spinner.succeed(text="passed")
except Exception as e:
    spinner.text_color="red"
    spinner.fail(str(e))
    raise e
spinner.stop()
