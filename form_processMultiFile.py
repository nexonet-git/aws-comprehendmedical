from ._anvil_designer import form_processMultiFileTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from . import ClientModule
from functools import reduce
from itertools import chain
import re
#from termcolor import color

class form_processMultiFile(form_processMultiFileTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
  
  def btn_AWSs3_click(self, **event_args):
   #This method is called when the Process Medical documents button is clicked
   #Get the document names from the S3 bucket 
    lstBucket = anvil.server.call('Get_S3Files')
    i=0
    #Process each document
    for doc in lstBucket:
      #Get the text from the document and display it to the uesr
      self.txt_Input.text = anvil.server.call('Process_S3File', doc)
      #Pass the file to the server side for it to be proceeesd by AWS Comprehend
      #Get the results (dictionaries)
      lstEntities = anvil.server.call('AWS_MedicalComprehend', self.txt_Input.text)
      if i == 0:
        ClientModule.dictConditions = lstEntities[0]
        ClientModule.dictProcedures = lstEntities[1]
        ClientModule.dictMedications = lstEntities[2]
      else:
        ClientModule.dictConditionsComb = {key:[*ClientModule.dictConditions[key], *lstEntities[0][key]] for key in ClientModule.dictConditions}
        ClientModule.dictProceduresComb = {key:[*ClientModule.dictProcedures[key], *lstEntities[1][key]] for key in ClientModule.dictProcedures}
        ClientModule.dictMedicationsComb = {key:[*ClientModule.dictMedications[key], *lstEntities[2][key]] for key in ClientModule.dictMedications}
      i = i+1
    
    #Call the server side functions and create and download the CSV files
    csv_Conditions = anvil.server.call("create_ConditionsFile", ClientModule.dictConditionsComb["condition"])
    download(csv_Conditions)
    csv_Medications =anvil.server.call("create_MedicationsFile", ClientModule.dictMedicationsComb["medication"])
    download(csv_Medications)
    csv_Procedures =anvil.server.call("create_ProceduresFile", ClientModule.dictProceduresComb["procedure"])
    download(csv_Procedures)
    alert ('your CSV files are ready in your Downloads folder')
    ClientModule.empty_Dictionaries()

  def btn_Menu_click(self, **event_args):
    #This method is called when the 'Main Menu' button is clicked"""
    open_form('form_mainMenu')
    pass

