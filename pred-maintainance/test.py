import logging
from random import randint
from dataBaseAccess_main import dbc
dbco = dbc()
print('hi')
abc = dbco.last5DaysfullCurrent()
print(abc)
