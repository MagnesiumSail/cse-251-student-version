"""
Course: CSE 251 
Lesson: L02 Prove
File:   prove.py
Author: Indiana Brown

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py" and leave it running.
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the description of the assignment.
  Note that the names are sorted.
- You are required to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a separate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class ThreadedClass(threading.Thread):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.data = None
        self.call_made = 0

    def run(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                self.data = response.json()
            self.call_made = 1
        except Exception as e:
            print(f"Error retrieving data from {self.url}: {e}")


# TODO Add any functions you need here

def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    top_api_thread = ThreadedClass(TOP_API_URL)
    top_api_thread.start()
    top_api_thread.join()

    total_calls = top_api_thread.call_made

    if top_api_thread.data:
        threads = []
        for url in top_api_thread.data.items():
            thread = ThreadedClass(url)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
            total_calls += thread.call_made

        # Display results
        for thread in threads:
            if thread.data:
                # Process and display the data
                log.write(f'{thread.url} => {len(thread.data)}')
            else:
                log.write(f'No data retrieved from {thread.url}')

        log.stop_timer('Total Time To complete')
        log.write(f'There were {total_calls} calls to the server')
    else:
        log.write('Failed to retrieve top API data')

    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()