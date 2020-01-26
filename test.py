from pyhouse.client import ClubhouseClient
from pyhouse.type2 import Story
import os
import json

key = os.environ.get("CLUBHOUSE_API_TOKEN")
if key is not None and key != '':        
    client = ClubhouseClient(key, debug=True)
    cat = client.listEntityTemplates()
