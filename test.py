import requests
import time
import json
import os
from tqdm import tqdm

BASE_URL = "http://35.200.185.69:8000"
# VERSIONS = ["/v1"]
ENDPOINT = "/v1/autocomplete?query="
CHARS= "!@$%^*()_~{}:|<>?|\/.,\';][=-`]"

all_names=[]
version_names=[]


# for v in VERSIONS:
#     this_version_names=[]
#     for c in CHARS:
#         url=BASE_URL+v+ENDPOINT+c
#         response = requests.get(url)
#         print(response.status_code)
#         data=response.json()
#         print(data)
#         if data["count"]!=0:
#             this_version_names+=data["results"]
#         # this_version_names+=data["results"]
#     version_names.append(this_version_names)

# cnt=0
# cnt2=0
# url=BASE_URL+ENDPOINT;
# while True:
#     response=requests.get(url)
#     if cnt==0:
#         cnt2+=1
#     if response.status_code == 429:
#         time.sleep(1)
#         cnt+=1
#         continue
#     if cnt>0:
#         break
    
# print(cnt,cnt2)

for c in CHARS:
    url=BASE_URL+ENDPOINT+c
    response=requests.get(url)
    data=response.json()
    print(data)

# for vname in version_names:
#     print(len(vname))
    # print(vname)
print("Programme End")