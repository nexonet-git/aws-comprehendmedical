import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# This is a module client global module.
# We can define variables and functions here, and use them from any form. 

#Define global dictionaries
dictConditions = {}
dictProcedures = {}
dictMedications = {}

def empty_Dictionaries():
#This function empties global dictionaries
  dictConditions.clear()  
  dictProcedures.clear()
  dictMedications.clear()


