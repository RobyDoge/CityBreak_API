from datetime import date as Date
from typing import List,Any
from enum import Enum


class ReturnCode(Enum):
      OK = 200
      CREATED = 201
      NO_CONTENT = 204
      BAD_REQUEST = 400
      NOT_FOUND = 404




def str_to_date(date_str:str|None)->Date|None:
   if not date_str:
      return None
   
   date_list:List[int] = ([int(x) for x in date_str.split('-')])
   date:Date
   try:
       date = Date(year=date_list[0],month=date_list[1],day=date_list[2])
       if date < Date.today():
           raise ValueError
   except ValueError:
         return None
   else:
         return date
   
   