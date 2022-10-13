from ._anvil_designer import form_SingleFileTemplate
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

class form_SingleFile(form_SingleFileTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def btn_Extract_click(self, **event_args):
    """This method is called when the button is clicked"""
    #Check if the user is clicking the button without providing medical text
    if len(self.txt_Input.text)==0:
      alert("Please insert medical text")
    else:
      #fresh start dictionaries, fields etc.
      ClientModule.empty_Dictionaries()
      self.txt_Condition.text = ""
      self.txt_Procedure.text = ""
      self.txt_Medication.text = ""
      strCondition = ""
      strCondition1 = ""
      strProcedure = ""
      strMedication = ""
      #send the medical text to AWS Comprehend on the server side code 
      lstEntities = anvil.server.call('AWS_MedicalComprehend', self.txt_Input.text)
      self.txt_Output.text = lstEntities[3]

      ClientModule.dictConditions = lstEntities[4]
      #self.txt_Condition.text = strCondition
      #self.txt_SnoMedConds.text = ClientModule.dictConditions.items() #type(lstEntities[4])
      self.repeating_panel_1.items = ClientModule.dictConditions["condition"]
      #self.txt_strip.text = ClientModule.dictConditions['condition']

      ClientModule.dictProcedures = lstEntities[5]
      self.repeating_panel_2.items = ClientModule.dictProcedures["procedure"]
      
      ClientModule.dictMedications = lstEntities[6]
      self.repeating_panel_3.items = ClientModule.dictMedications["medication"]
      
      self.btn_Clear.visible = 'true'
      self.btn_CSV.visible = 'true'
      self.btn_PDF.visible = 'true'
    pass
         
  def txt_Output_change(self, **event_args):
    """This method is called when the text in this text area is edited"""
    pass

  def btn_CSV_click(self, **event_args):
      """This method is called when the button is clicked"""
      #Conditions_Data =anvil.server.call("create_ConditionsFile", ClientModule.lstCondition)
      Conditions_Data =anvil.server.call("create_ConditionsFile", ClientModule.dictConditions["condition"])
      download(Conditions_Data)
      
      Medications_Data =anvil.server.call("create_MedicationsFile", ClientModule.dictMedications["medication"])
      download(Medications_Data)
      
      Procedures_Data =anvil.server.call("create_ProceduresFile", ClientModule.dictProcedures["procedure"])
      download(Procedures_Data)
                

  def txt_Input_focus(self, **event_args):
    """This method is called when the text area gets focus"""
    if "Please either " in self.txt_Input.text:
      self.txt_Input.text = ''
    pass

  def btn_Clear_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.txt_Input.text = ''
    #ClientModule.empty_Lists()
    lstEntities=[]
    self.repeating_panel_1.items = None 
    self.repeating_panel_2.items = None 
    self.repeating_panel_3.items = None 
    pass
 

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if file.name.find('.docx') > 0:
      self.txt_Input.text = anvil.server.call("read_docx_file", file)
    elif file.name.find('.pdf') > 0:
      self.txt_Input.text = anvil.server.call("read_pdf_file", file)
    else:
      alert("Please upload either 'docx' or 'pdf' file types")
      
    self.txt_Condition.text = ""
    self.txt_Procedure.text = ""
    self.txt_Medication.text = ""
    #ClientModule.empty_Lists()
    ClientModule.empty_Dictionaries()
    self.btn_Extract.enabled = 'true'
    
    pass

  def btn_PDF_click(self, **event_args):
    """This method is called when the button is clicked"""
    #open_form('frm_MedicalSummary', self.txt_Condition.text, self.txt_Medication.text, self.txt_Procedure.text)
    pdf = anvil.server.call('create_pdf', self.txt_Condition.text, self.txt_Medication.text, self.txt_Procedure.text)
    anvil.media.download(pdf)
    pass

 









