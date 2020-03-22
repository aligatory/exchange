# Exchange

### Description:
    бот закупает валюту и пытается ее продать с выгодой 
    на указанный проецент. Чем больше процент, тем меньше 
    вероятность уйти в плюс.

### Bot usage
    -c - currency id
    -p - желаемая выгода (0-100)
    -s - начальный закуп на сумму
    
    Например
    
    start_bot -c 1 -p 1 -s 1
    

### Add default currencies:
    make currencies    

### Clear db
    make db_clear
    
### Create venv:
    make venv

### Run tests:
    make test
    
### Run linters:
    make lint
    
### Run formatters:
    make format
   
    
    
