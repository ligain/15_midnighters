  
# Night Owls Detector
Simple tool to find out who of devman.org users pushes their code after midnight.
It utilizes this open [API](https://devman.org/api/challenges/solution_attempts/)
  
# Installation
**Python 3 should be already installed.**

0) Get source code
```bash
$ git clone https://github.com/ligain/15_midnighters.git
```

1) Create virtual environment in the directory where you want to place project.
```bash
$ cd 15_midnighters/
python3 -m venv .env
```

2) Activate virtual environment
```bash
$ . .env/bin/activate
```

3) Install all dependencies via pip
```bash  
pip install -r requirements.txt # alternatively try pip3  
```  
# Usage
```bash
$ cd 15_midnighters/
$ python3 seek_dev_nighters.py 
List of all midnighters on devman.com:
user1
user2
user3
...
```
  
# Project Goals  
  
The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)