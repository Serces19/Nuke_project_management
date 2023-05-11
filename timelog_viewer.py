import nuke
import getpass
import shutil
import json
import os
import nukescripts

CURRENT_USER =  getpass.getuser()
LOG_DIR = ''



class Panel(nukescripts.PythonPanel):
    def __init__(self, name):
        super(Panel,self).__init__(name)
        self.setMinimumSize(500,500)
        self.date_combo_box = nuke.Enumeration_Knob('date', 'Date',[])
        self.delete_push_button = nuke.Pyscript_Knob('delete', 'Delete', '')
        self.log_knob = nuke.Multiline_Eval_String_Knob('text','Log','')

        self.addKnob(self.date_combo_box)
        self.addKnob(self.delete_push_button)
        self.addKnob(self.log_knob)
        
        self.build_date_combo_box()

    def build_date_combo_box(self):
        log_dir = '%s/%s' % (LOG_DIR, CURRENT_USER)
        self.date_combo_box.setValues(os.walk(log_dir).next()[1])

    def get_log(self):
        date = self.date_combo_box.value()

    def build_log_text(self, log):
        text = ''
        for i in log:
            time = log[i]
            text += '%s\n%s\n\n' % (i, self.seconds)
            self.log_knob.setValue(text)

    def knobChanged(self, knob):
        if knob.name() == 'date':
            self.build_log_text(self.get_log())

        if knob.name() == 'dalete':
            self.delete_log()

    def seconds_to_str(self, sec):
    
    def delete_log(self):
        message = nuke.ask('Estas seguro de eliminar este tiempo registrado?')
        if not message:
            return
    
        date = self.date_combo_box.value()
        path = '%s/%s/%s' %(LOG_DIR, CURRENT_USER, date)
        shutil.rmtree(path)
        self.log_knob.setValue('')
        self.build_date_combo_box()

panel = Panel('Timelog')
panel.showModalDialog()
