from datetime import datetime
import pickle
import main
def Save(path,window):
    CurrentTime = datetime.now()
    with open('objs.pkl', 'w') as f:  # Python 3: open(..., 'wb')
        pickle.dump([main.Rest_times], f)

def Load(path,window):
    text_file = open(path, "r")
    text_file.close()
