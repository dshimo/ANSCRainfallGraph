Rainfall Graph pulled from USGS for ANSC

**Team 5:**  
Nick Dant  
Naomi Martinez  
David Shi  
Sid Srikumar  
Christy Tran  

# Setting up environment for Unix machines

This is intended for the team if working on the CS machines.  

Set up your virtual environment and source it:  
```
virtualenv -p python3.5 ~/venv/ANSCRainfallGraph  
source ~/venv/ANSCRainfallGraph/bin/activate  
```
Deactivate your virtual environment by simply using:  
```
deactivate  
```

Get the code:  

SSH:
```
git clone git@github.com:dshimo/ANSCRainfallGraph.git  
```

HTTP:
```
git@github.com:dshimo/ANSCRainfallGraph.git  
```

Install the dependencies:
```
pip install -r requirements.txt  
```

Run apiworker.py to build the database  
```
python apiworker.py  
```

To view the database, use your own SQLite viewer.  
A console viewer you can use is `sqlite3`  
