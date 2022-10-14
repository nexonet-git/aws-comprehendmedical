from ._anvil_designer import form_processSingleFileTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from . import ClientModule
from functools import reduce
from itertools import chain
import re

class form_processSingleFile(form_processSingleFileTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def btn_Extract_click(self, **event_args):
    #This method is called when the Extract Clinical button is clicked
    #Check if the user is clicking the button without providing medical text
    if len(self.txt_Input.text)==0:
      alert("Please insert medical text")
    else:
      #fresh start dictionaries, fields etc.
      ClientModule.empty_Dictionaries()
      #strCondition = ""
      #strCondition1 = ""
      #strProcedure = ""
      #strMedication = ""
      
      #send the medical text to AWS Comprehend on the server side code and get the result
      lstEntities = anvil.server.call('AWS_MedicalComprehend', self.txt_Input.text)
      #self.txt_Output.text = lstEntities[3]

      #Populate the client side Conditions dictionary
      ClientModule.dictConditions = lstEntities[0]      
      #Populate the Medical Conditions Data Grid
      self.repeating_panel_1.items = ClientModule.dictConditions["condition"]

      #Populate the Medical Procedures Data Grid
      ClientModule.dictProcedures = lstEntities[1]    
      #Populate the Medical Medical Procedures Data Grid
      self.repeating_panel_2.items = ClientModule.dictProcedures["procedure"]

      #Populate the Mediations Data Grid
      ClientModule.dictMedications = lstEntities[2]    
      #Populate the Medications Data Grid
      self.repeating_panel_3.items = ClientModule.dictMedications["medication"]

      #Make visible the 'Clear Form' and 'Download CSV' buttons
      self.btn_Clear.visible = 'true'
      self.btn_CSV.visible = 'true'
    pass
         
  def btn_CSV_click(self, **event_args):
      #This method is called when the 'Download CSV'button is clicked
      #Call the server side functions and create and download the CSV files
      csv_Conditions =anvil.server.call("create_ConditionsFile", ClientModule.dictConditions["condition"])
      download(csv_Conditions)
      
      csv_Medications =anvil.server.call("create_MedicationsFile", ClientModule.dictMedications["medication"])
      download(csv_Medications)
      
      csv_Procedures =anvil.server.call("create_ProceduresFile", ClientModule.dictProcedures["procedure"])
      download(csv_Procedures)
               

  def txt_Input_focus(self, **event_args):
    #This method is called when the Medical Text area gets focus initially
    if "Please either " in self.txt_Input.text:
      self.txt_Input.text = ''
    pass

  def btn_Clear_click(self, **event_args):
    #This method is called when the 'Clear Form' button is clicked
    #Clear all fields, data grids and lists
    self.txt_Input.text = ''
    #ClientModule.empty_Lists()
    lstEntities=[]
    ClientModule.empty_Dictionaries()
    self.repeating_panel_1.items = None 
    self.repeating_panel_2.items = None 
    self.repeating_panel_3.items = None 
    pass
 

  def file_loader_1_change(self, file, **event_args):
    #This method is called when a new file is loaded into this FileLoader
    #If the document docx or pdf then process it
    if file.name.find('.docx') > 0:
      self.txt_Input.text = anvil.server.call("read_docx_file", file)
    elif file.name.find('.pdf') > 0:
      self.txt_Input.text = anvil.server.call("read_pdf_file", file)
    else:
      alert("Please upload either 'docx' or 'pdf' file types")
      
    ClientModule.empty_Dictionaries()
    self.btn_Extract.enabled = 'true'
    
    pass
    
  def btn_Menu_click(self, **event_args):
    #This method is called when the 'Main Menu' button is clicked
    open_form('form_mainMenu')
    pass

  def txt_Output_change(self, **event_args):
    """This method is called when the text in this text area is edited"""
    pass





 









