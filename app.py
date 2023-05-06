import os
import uuid
from flask import Flask, flash, request, redirect
import librosa
import pickle
import soundfile as sf
import pandas as pd
import os
import sys
import librosa
import soundfile as sf
import speech_recognition as SR
import whisper
sound_model = whisper.load_model("small")
import pyttsx3
import threading
import time
import win32com.client as wincl
engine = pyttsx3.init()

import nltk
nltk.download('punkt')
nltk.download('stopwords')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

english_words = set(nltk.corpus.words.words())
english_stopwords = set(stopwords.words('english'))

mobile_phone_companies = [
    'Apple',
    'Samsung',
    'Huawei',
    'Xiaomi',
    'Oppo',
    'Vivo',
    'OnePlus',
    'Google',
    'Motorola',
    'LG',
    'Sony',
    'Nokia',
    'HTC',
    'Lenovo',
    'Asus'
]


from transformers import AutoModel, BertTokenizerFast
# Load the BERT tokenizer
tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
# Import BERT-base pretrained model
bert = AutoModel.from_pretrained('bert-base-uncased')
from transformers import DistilBertTokenizer, DistilBertModel
# Load the DistilBert tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
# Import the DistilBert pretrained model
bert = DistilBertModel.from_pretrained('distilbert-base-uncased')

from flask import Flask, request, render_template
import re
import random
import torch
import numpy as np
import pickle
import torch.nn as nn
import pandas as pd
import numpy as np


# levanstine distance
df =pd.read_csv('smartphones.csv', sep='^')
phones = df['Product Name'].tolist()

def lev_distance(s, t):
    """Returns the Levenshtein distance between two strings."""
    m, n = len(s), len(t)
    d = [[0] * (n+1) for _ in range(m+1)]
    for i in range(m+1):
        d[i][0] = i
    for j in range(n+1):
        d[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s[i-1] == t[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = 1 + min(d[i-1][j], d[i][j-1], d[i-1][j-1])
    return d[m][n]

def find_min_distance_item(lst, query):
    """Finds the item in a list that has the minimum Levenshtein distance to a query string."""
    min_distance = float('inf')
    min_item = None
    for item in lst:
        distance = lev_distance(query, item.lower())
        if distance < min_distance:
            min_distance = distance
            min_item = item
    return min_item





max_seq_len = 8
device = torch.device('cpu')
import pandas as pd

#loading questions
df=pd.read_csv('MORE DATA.csv')
df= df.drop('Unnamed: 2',axis=1)

temp = pd.read_csv('Neo4jQUERY.csv')
c = temp['field'].tolist()
c.remove('Demo Video'); c.remove('Weight')
temp =[]
l1 = df['Label'].to_list()
for i in l1:
    try:
        temp.append(i.strip())
    except:
        temp.append('')

df['col'] = temp
df = df[df['col'].isin(c)]

# Converting the labels into encodings
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['col'] = le.fit_transform(df['col'])


#loading model responses

response = pd.read_csv('Responses.csv')
response.drop('Unnamed: 2',axis=1)
# coverting data into dictionary
tag = response['tag'].tolist()
msg = response['message'].tolist()

from collections import defaultdict
RES = defaultdict(list)

for i,j in zip(tag,msg):
    RES[i].append(j)



class BERT_Arch(nn.Module):
   def __init__(self, bert):      
       super(BERT_Arch, self).__init__()
       self.bert = bert 
      
       # dropout layer
       self.dropout = nn.Dropout(0.2)
      
       # relu activation function
       self.relu =  nn.ReLU()
       # dense layer
       self.fc1 = nn.Linear(768,512)
       self.fc2 = nn.Linear(512,256)
       self.fc3 = nn.Linear(256,60)
       #softmax activation function
       self.softmax = nn.LogSoftmax(dim=1)
       #define the forward pass
   def forward(self, sent_id, mask):
      #pass the inputs to the model  
      cls_hs = self.bert(sent_id, attention_mask=mask)[0][:,0]
      
      x = self.fc1(cls_hs)
      x = self.relu(x)
      x = self.dropout(x)
      
      x = self.fc2(x)
      x = self.relu(x)
      x = self.dropout(x)
      # output layer
      x = self.fc3(x)
   
      # apply softmax activation
      x = self.softmax(x)
      return x

with open('DarazChat.pkl', 'rb') as f:
	model = pickle.load(f)

Quries = pd.read_csv('Neo4JQUERY.csv')
INTENTS = Quries['field'].to_numpy()
QUERIES = Quries['query'].tolist()
from neo4j import GraphDatabase
# Set up the connection to the Neo4j database
uri = "bolt://localhost:7687"
username = "neo4j"
password = "12345678"
driver = GraphDatabase.driver(uri, auth=(username, password))

def get_prediction(str):
 str = re.sub(r'[^a-zA-Z ]+', '', str)
 test_text = [str]
 model.eval()
 
 tokens_test_data = tokenizer(
 test_text,
 max_length = max_seq_len,
 pad_to_max_length=True,
 truncation=True,
 return_token_type_ids=False
 )
 test_seq = torch.tensor(tokens_test_data['input_ids'])
 test_mask = torch.tensor(tokens_test_data['attention_mask'])
 
 preds = None
 with torch.no_grad():
   preds = model(test_seq.to(device), test_mask.to(device))
 preds = preds.detach().cpu().numpy()
 preds = np.argmax(preds, axis = 1)
 print("PREDS: ", preds)
 print('Intent Identified:', le.inverse_transform(preds)[0])
 return le.inverse_transform(preds)[0]



def get_response(message,item=''): 
    intent = get_prediction(message).strip()
    try:
      result = random.choice(RES[intent])
    except:
      result = 'No Data'

    if intent in INTENTS:
      
      if intent in ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10', 'Q11', 'Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q17', 'Q18', 'Q19', 'Q20', 'Q21', 'Q22', 'Q23', 'Q24', 'Q25', 'Q26', 'Q27', 'Q28', 'Q29', 'Q30', 'Q31', 'Q32', 'Q33', 'Q34', 'Q35', 'Q36', 'Q37', 'Q38', 'Q39', 'Q40', 'Q41', 'Q42', 'Q43', 'Q44', 'Q45', 'Q46']:
          return result

      #levenstine dist
      ITEM = find_min_distance_item(phones, item)
      if item == '':
          result = 'PLEASE ENTER THE ITEM AND SUBMIT QUERY AGAIN'
          return result
      c = int(np.where(INTENTS == intent)[0])
      q = QUERIES[c]
      q=q.replace('xxx',ITEM)
      result = result.replace('item',ITEM)
      #data retrival

      with driver.session() as session:
        temp = session.run(q)
        result = str(result) + ' ' + str(temp.single()[0])
        print("return response: ", result)
    return result


UPLOAD_FOLDER = 'files'
hop_length = 512


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def remove_english_words(sentence):
    words = word_tokenize(sentence)
    filtered_words = []
    for word in words:
        if word.lower() in mobile_phone_companies or word.lower() not in english_words:
            filtered_words.append(word)
    return ' '.join(filtered_words)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        message = request.form['message']
        #item_name = request.form.get('itemname')

        item_name = remove_english_words(message)

        result = get_response(message,item_name).strip()

        print("The result in route / ", result)

        return render_template('index.html', result=result)
    return render_template('index.html')

'''
@app.route('/')
def root():
    return app.send_static_file('index.html')'''


@app.route('/save-record', methods=['POST'])
def save_record():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    file_name = "sound.wav"
    #C:\\Users\\A1D\\Desktop\\RECORDER
    full_file_name = os.path.join('C:\\Users\\A1D\\Desktop\\NLP ASSIGNMENT 4 (CHAT BOT)\\VOICE', file_name)
    file.save(full_file_name)
    
    #sample_rate = 44100
    #channels = 2
    #audio_data,_ = sf.read(file)
    #sf.write('this.mp3', audio_data, sample_rate, subtype='PCM_16')  # save the audio data to a file    

    return '<h1>Success</h1>'

audMsg=""
def speak():
     speaker = wincl.Dispatch("SAPI.SpVoice")
     # Speak the text
     speaker.Speak(audMsg)
     #engine.say(audMsg)
     #threading.Thread(target=speaker.Speak(),args=audMsg).start()
     #engine.runAndWait()
     #time.sleep(5)
     #engine.stop()
     #engine.endLoop()
     print("audio msg finished")

@app.route('/get-data', methods=['GET'])
def get_flask_response():
   # Retrieve some data to return to frontend
   response = "Hello, frontend!"
   audio_file = "C:\\Users\\A1D\\Desktop\\NLP ASSIGNMENT 4 (CHAT BOT)\\VOICE\\sound.wav"
   #audio_file = AudioSegment.from_file(audio)


   # read audio file using librosa
   y, sr = librosa.load(r'./sound.wav', sr=None)

   # resample audio to 16kHz to improve ASR performance
   y_resampled = librosa.resample(y,orig_sr=sr,target_sr=16000)

   # write resampled audio to disk
   sf.write(r'./test.wav', y_resampled, 16000)

   # create a recognizer object
   r = SR.Recognizer()

   # load audio file
   with SR.AudioFile('./test.wav') as source:
   	audio = r.record(source)

   # transcribe audio using Google Speech Recognition API
   try:
        text = sound_model.transcribe("test.wav")
        item_name = remove_english_words(text['text'])
        response = get_response(text['text'],item_name).strip()
        result = "Audio Query: " + text['text'] + "......................... Response:........>" + response 
        global audMsg
        audMsg = response
        speak()
        print("The result in route / ", result)
        return result
   except SR.UnknownValueError:
   	text = "Try again"
   except SR.RequestError as e:
   	text = "Try again"
   

    
   return text





if __name__ == '__main__':
    app.run()      