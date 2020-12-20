import s3fs
import hashlib
import requests
import json
import urllib.parse
import pickle
from astra_env import *
from tags import generate_tags

"""
Given a PDF file:
1. Hash it.
2. Generate tags.
3. Store the hash | {tags} in the database.
4. Store the file in S3 with name {hash}.pdf
"""

# Datastax stuff
ASTRA_DB_ID='2e739356-b1aa-4645-a4ca-90f4097f692c' # same as the cluster id
ASTRA_DB_REGION='us-east1'	# same as the cluster region
ASTRA_DB_USERNAME='rmren'
ASTRA_DB_KEYSPACE='keyname'
ASTRA_DB_PASSWORD='password'

# S3 stuff
ACCESS_KEY_ID = 'AKIA4XGHRM73GDU52D3X'
ACCESS_SECRET_KEY = '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'
BUCKET_NAME = 'hackumass2020'

s3 = s3fs.S3FileSystem(key=ACCESS_KEY_ID, secret=ACCESS_SECRET_KEY)

def upload(pdf_file, title='untitled', desc='desc', school='umass', courseid='0000'):
  # assert is_pdf(pdf_file)

  # Open the PDF
  f = open(pdf_file, 'rb')
  data = f.read(65536)

  # Generate the hash
  md5_hash = hashlib.md5(data).hexdigest()
  hash_pdf = md5_hash + '.pdf'
  rpath = BUCKET_NAME + '/' + hash_pdf
  # Generate tags.
  tags = generate_tags(pdf_file)
  # tags = {'math':1, 'biology':0, 'cs':1, 'english':0}  # temp code.
  # Upload to Datastax Astra
  ## Get auth token
  auth_token = get_auth_key()

  title = pdf_file.split('/')[-1].split('.')[0]
  ## Add entry to table
  item = {
    'hash': md5_hash,
    'courseid': courseid,
    'desc': desc,
    'file_url': rpath,
    'school': school,
    'title': title,
    'tags': json.dumps(tags)
  }
  row = []
  for (k,v) in item.items():
    row.append({'name':k, 'value':v})

  data = json.dumps({'columns': row})
  url = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v1/keyspaces/' + ASTRA_DB_KEYSPACE + '/tables/test11/rows'
  headers = {'accept': 'application/json', 'x-cassandra-token': auth_token, 'content-type': 'application/json'}
  r = requests.post(url=url, headers=headers, data=data)
  print(r.json())

  # Upload to S3
  s3.put(lpath = pdf_file, rpath = rpath)


  # Save keys
  text = s3.open('hackumass2020/keys.txt', 'r').read()
  with s3.open('hackumass2020/keys.txt', 'w') as f:
    f.write(text + md5_hash + '\n')
    f.close()

  print("Done")

def get_auth_key():
  url='https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v1/auth'
  headers = {'Content-Type': 'application/json'}
  data = json.dumps({'username': ASTRA_DB_USERNAME, 'password': ASTRA_DB_PASSWORD})
  r = requests.post(url=url, data=data, headers=headers)
  auth_token = r.json()['authToken']
  print(auth_token)
  return auth_token

def createCollection(name):
  auth_token = get_auth_key()
  url = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v2/schemas/namespaces/' + ASTRA_DB_KEYSPACE + '/collections'
  headers = {'accept': 'application/json', 'x-cassandra-token': auth_token, 'content-type': 'application/json'}

  data = { "name" : name }
  response = requests.request("POST", url, headers=headers)
  print(response.text)

def createDocument(data):
  data = { "school" : "UMass",
            "tags": [{"a": "b"}]
         }
  auth_token = get_auth_key()
  url = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v2/schemas/namespaces/' + ASTRA_DB_KEYSPACE + '/collections'
  headers = {'accept': 'application/json', 'x-cassandra-token': auth_token, 'content-type': 'application/json'}

  response = requests.request("POST", url, headers=headers, data=json.dumps(data))
  print(response.text)

def createNamespace(name):
  auth_token = get_auth_key()
  url = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v2/schemas/namespaces/'
  headers = {'accept': 'application/json', 'x-cassandra-token': auth_token, 'content-type': 'application/json'}

  data = { "name" : name }
  response = requests.request("POST", url, headers=headers, data=json.dumps(data))

  print(response.text)

def listNamespaces():
  auth_token = get_auth_key()
  url = 'https://' + ASTRA_DB_ID + '-' + ASTRA_DB_REGION + '.apps.astra.datastax.com/api/rest/v2/schemas/namespaces/'
  headers = {'accept': 'application/json', 'x-cassandra-token': auth_token, 'content-type': 'application/json'}

  response = response = requests.request("GET", url, headers=headers)

  print(response.text)

def mathew_run():
  listNamespaces()
  createNamespace("hi")
  return
#createNamespace("hi")
#createCollection("hi")

def download(hashed_pdf):
  rpath = BUCKET_NAME + '/' + hashed_pdf
  try:
    return s3.open(rpath)
  except:
    print("s3test.download() failed!")



def get_data():
  auth_token = get_auth_key()
  data = []
  with s3.open('hackumass2020/keys.txt', 'r') as f:
    for line in f.readlines():
      line = line.rstrip()
      print("Line", line)
      url = "https://2e739356-b1aa-4645-a4ca-90f4097f692c-us-east1.apps.astra.datastax.com/api/rest/v1/keyspaces/keyname/tables/test11/rows/" + line
      headers = {
        "Accept": "application/json",
        "X-Cassandra-Token": auth_token
      }
      r = requests.request("GET", url, headers=headers)
     # print(r.json())
      data.append(r.json()['rows'][0])
    f.close()
  return data


# def get_data():
#   auth_token = get_auth_key()
#   url = "https://2e739356-b1aa-4645-a4ca-90f4097f692c-us-east1.apps.astra.datastax.com/api/rest/v1/keyspaces/keyname/tables/test11/rows/1"

#   headers = {
#       "Accept": "application/json",
#       "X-Cassandra-Token": auth_token
#   }

#   response = requests.request("GET", url, headers=headers)

#   print(response.text)

'''
void get_data(): list<dict>()

dict: {
  title: t,
  desc: d,
  school: s,
  courseid: cid,
  fileurl: f,
  tags: [
         { tagname: tag1,
           confidence: c1
         },
         { tagname: tag2,
           confidence: c2
         }
        ]
}
'''

# curl -L -X GET 'http://localhost:8082/v2/keyspaces/users_keyspace/users?where=\{"firstname":\{"$eq":"Mookie"\}\}' \
# --header "X-Cassandra-Token: $AUTH_TOKEN" \
# --header 'Content-Type: application/json'




#get_data()
# import requests


def clear_key():
  s3.open('hackumass2020/keys.txt', 'w').close()

# url = "https:///2e739356-b1aa-4645-a4ca-90f4097f692c-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/keyname/test0"
# querystring = {"where":"[object Object]","sort":"[object Object]"}
# headers = {"Accept": "application/json"}
# response = requests.request("GET", url, headers=headers, params=querystring)
# print(response.text)

#upload('healthcare.pdf')
#upload('pdf-test.pdf')
#retrieve_rows('a')
#print(get_data())

# curl --request GET \
#   --url 'https:///2e739356-b1aa-4645-a4ca-90f4097f692c-us-east1.apps.astra.datastax.com/api/rest/v2/keyspaces/keyname/test0?where=%5Bobject%20Object%5D&sort=%5Bobject%20Object%5D&raw=false' \
#   --header 'Accept: application/json'



  # payload = {
  #   'columnNames': ['file_url'],
  #   'filters': [
  #     {
  #       'value': ['0'],
  #       'operator': 'gt',
  #       'columnName': 'hash',
  #     },
  # ] }




  # curl --request GET \
  # --url 'https://2e739356-b1aa-4645-a4ca-90f4097f692c-us-east1.apps.astra.datastax.com/v2/keyspaces/keyname/test11/9db3b66632f250efbd61ad43130cf966' \
  # --header 'Accept: application/json'
