# WildNotes telegram bot

This telegram bot was created to track goods and analyze changes in prices of goods by article.

## Requirements

You will need:
+ Python version **3.8 >**
+ Create virtual python environment
```bash
python -m venv env
```

## Installing requirements
+ Clone this repo:
```bash
git clone https://github.com/5ato/WildNotes.git
cd WildNotes
```
+ Activate virtual python environment:
```bash
env/bin/activate
```

+ Install dependencies:
```bash
pip install -r requirements.txt
```

## Environment variables

1. ```token``` - Bot token received from BotFather
1. ```DBNAME``` - Postgresql database name
1. ```USERDB``` - Username of database user in postgresql
1. ```PASSWORDDB``` - Password of database user in postgresql
