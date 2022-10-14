from ._anvil_designer import form_mainMenuTemplate
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

class form_mainMenu(form_mainMenuTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.

  def btn_Multi_click(self, **event_args):
    #This method is called when the 'Process Multiple Documents' button is clicked
    open_form('form_processMultiFile')
    pass

  def btn_Single_click(self, **event_args):
    #This method is called when the 'Process Multiple Documents' button is clicked
    open_form('form_processSingleFile')
    pass





 