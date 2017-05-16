# -*- coding: utf-8 -*-
"""
Widget for entering frequency specifications

Author: Christian Münker
"""
from __future__ import print_function, division, unicode_literals, absolute_import
import sys
import logging
logger = logging.getLogger(__name__)

from ..compat import (QtCore, Qt,
                      QWidget, QLabel, QLineEdit, QFrame, QFont,
                      QVBoxLayout, QHBoxLayout, QGridLayout,
                      pyqtSignal, QEvent)

import pyfda.filterbroker as fb
from pyfda.pyfda_lib import rt_label, style_widget, safe_eval
from pyfda.pyfda_rc import params  # FMT string for QLineEdit fields, e.g. '{:.3g}'

class FreqSpecs(QWidget):
    """
    Build and update widget for entering the frequency
    specifications like F_sb, F_pb etc.
    """

    # class variables (shared between instances if more than one exists)
    sigSpecsChanged = pyqtSignal() # emitted when filter has been changed

    def __init__(self, parent, title = "Frequency Specs"):

        super(FreqSpecs, self).__init__(parent)
        self.title = title

        self.qlabels = []    # list with references to QLabel widgets
        self.qlineedit = []  # list with references to QLineEdit widgetss

        self.spec_edited = False # flag whether QLineEdit field has been edited

        self._construct_UI()

#-------------------------------------------------------------
    def _construct_UI(self):
        """
        Construct the User Interface
        """
        bfont = QFont()
        bfont.setBold(True)

        lblTitle = QLabel(str(self.title), self) # field for widget title
        lblTitle.setFont(bfont)
        lblTitle.setWordWrap(True)
        self.lblUnit = QLabel(self)
        self.lblUnit.setText("in " + rt_label(fb.fil[0]['freq_specs_unit']))

        layHTitle = QHBoxLayout()
        layHTitle.addWidget(lblTitle)
        layHTitle.addWidget(self.lblUnit)
        layHTitle.addStretch(1)
        
        # Create a gridLayout consisting of QLabel and QLineEdit fields
        # for the frequency specs:
        self.layGSpecs = QGridLayout() # sublayout for spec fields
        # set the title as the first (fixed) entry in grid layout. The other
        # fields are added and hidden dynamically in _show_entries and _hide_entries()
        self.layGSpecs.addLayout(layHTitle, 0, 0, 1, 2)
        self.layGSpecs.setAlignment(Qt.AlignLeft)

        self.frmMain = QFrame(self)
        self.frmMain.setLayout(self.layGSpecs)

        self.layVMain = QVBoxLayout() # Widget main layout
        self.layVMain.addWidget(self.frmMain)#, Qt.AlignLeft)
        self.layVMain.setContentsMargins(*params['wdg_margins'])
        self.setLayout(self.layVMain)

        self.n_cur_labels = 0 # number of currently visible labels / qlineedits        

        #----------------------------------------------------------------------
        # EVENT FILTER
        #----------------------------------------------------------------------
        # DYNAMIC SIGNAL SLOT CONNECTION:
        # Every time a field is edited, call self.store_entries 
        # This is achieved by dynamically installing and
        # removing event filters when creating / deleting subwidgets.
        # The event filter monitors the focus of the input fields.
        #----------------------------------------------------------------------
#------------------------------------------------------------------------------

    def eventFilter(self, source, event):
        """
        Filter all events generated by the QLineEdit widgets. Source and type
        of all events generated by monitored objects are passed to this eventFilter,
        evaluated and passed on to the next hierarchy level.

        - When a QLineEdit widget gains input focus (QEvent.FocusIn`), display
          the stored value from filter dict with full precision
        - When a key is pressed inside the text field, set the `spec_edited` flag
          to True.
        - When a QLineEdit widget loses input focus (QEvent.FocusOut`), store
          current value normalized to f_S with full precision (only if
          `spec_edited`== True) and display the stored value in selected format
        """
        if isinstance(source, QLineEdit): # could be extended for other widgets
            if event.type() == QEvent.FocusIn:
                self.spec_edited = False
                self.load_dict()
                # store current entry in case new value can't be evaluated:
                fb.data_old = source.text()
            elif event.type() == QEvent.KeyPress:
                self.spec_edited = True # entry has been changed
                key = event.key()
                if key in {QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter}:
                    self._store_entry(source)
                elif key == QtCore.Qt.Key_Escape: # revert changes
                    self.spec_edited = False                    
                    self.load_dict()
                
            elif event.type() == QEvent.FocusOut:
                self._store_entry(source)
        # Call base class method to continue normal event processing:
        return super(FreqSpecs, self).eventFilter(source, event)


#------------------------------------------------------------------------------
    def _store_entry(self, event_source):
        """
        _store_entry is triggered by `QEvent.focusOut` in the eventFilter:        
        When the textfield of `widget` has been edited (`self.spec_edited` =  True),
        sort and store all entries in filter dict, then reload the text fields. 
        Finally, emit a SpecsChanged signal.
        """
        if self.spec_edited:
            f_label = str(event_source.objectName())
            f_value = safe_eval(event_source.text(), fb.data_old) / fb.fil[0]['f_S']
            fb.fil[0].update({f_label:f_value})
            self.sort_dict_freqs()
            self.sigSpecsChanged.emit() # -> filter_specs
            self.spec_edited = False # reset flag

#-------------------------------------------------------------
    def update_UI(self, new_labels = ()):
        """
        Set labels and get corresponding values from filter dictionary.
        When number of entries has changed, the layout of subwidget is rebuilt,
        using

        - `self.qlabels`, a list with references to existing QLabel widgets,
        - `new_labels`, a list of strings from the filter_dict for the current
          filter design
        - 'num_new_labels`, their number
        - `self.n_cur_labels`, the number of currently visible labels / qlineedit
          fields
        """
        state = new_labels[0]
        new_labels = new_labels[1:]
            
        self.lblUnit.setText(" in " + rt_label(fb.fil[0]['freq_specs_unit']))
        num_new_labels = len(new_labels)
        # hide / show labels / create new subwidgets if neccessary:
        self._show_entries(num_new_labels)

#        W_lbl = max([self.qfm.width(l) for l in new_labels]) # max. label width in pixel

        #---------------------------- logging -----------------------------
        logger.debug("update_UI: {0}-{1}-{2}".format(
                            fb.fil[0]['rt'],fb.fil[0]['fc'],fb.fil[0]['fo']))

        for i in range(num_new_labels):
            # Update ALL labels and corresponding values 
            self.qlabels[i].setText(rt_label(new_labels[i]))
            
            self.qlineedit[i].setText(str(fb.fil[0][new_labels[i]]))
            self.qlineedit[i].setObjectName(new_labels[i])  # update ID
            style_widget(self.qlineedit[i], state)

        self.n_cur_labels = num_new_labels # update number of currently visible labels
        self.sort_dict_freqs() # sort frequency entries in dictionary and update display

#-------------------------------------------------------------        
    def load_dict(self):
        """
        Reload textfields from filter dictionary 
        Transform the displayed frequency spec input fields according to the units
        setting (i.e. f_S). Spec entries are always stored normalized w.r.t. f_S 
        in the dictionary; when f_S or the unit are changed, only the displayed values
        of the frequency entries are updated, not the dictionary!

        load_dict is called during init and when the frequency unit or the
        sampling frequency have been changed.

        It should be called when sigSpecsChanged or sigFilterDesigned is emitted
        at another place, indicating that a reload is required.
        """

        # recalculate displayed freq spec values for (maybe) changed f_S
        logger.debug("exec load_dict")
        for i in range(len(self.qlineedit)):
            f_name = str(self.qlineedit[i].objectName()).split(":",1)
            f_label = f_name[0]
            f_value = fb.fil[0][f_label] * fb.fil[0]['f_S']

            if not self.qlineedit[i].hasFocus():
                # widget has no focus, round the display
                self.qlineedit[i].setText(params['FMT'].format(f_value))
            else:
                # widget has focus, show full precision
                self.qlineedit[i].setText(str(f_value))

#------------------------------------------------------------------------
    def _show_entries(self, num_new_labels):
        """
        - check whether subwidgets need to be shown or hidden       
        - check whether enough subwidgets (QLabel und QLineEdit) exist for the 
          the required number of `num_new_labels`: 
              - create new ones if required 
              - initialize them with dummy information
              - install eventFilter for new QLineEdit widgets so that the filter 
                  dict is updated automatically when a QLineEdit field has been 
                  edited.
        - if enough subwidgets exist already, make enough of them visible to
          show all spec fields
        """

        num_tot_labels = len(self.qlabels) # number of existing labels (vis. + invis.)

        # less new subwidgets than currently displayed -> _hide some
        if num_new_labels < self.n_cur_labels: # less new labels/qlineedit fields than before
            for i in range (num_new_labels, num_tot_labels):
                self.qlabels[i].hide()
                self.qlineedit[i].hide()
        # enough hidden subwidgets but need to make more labels visible
        elif num_tot_labels >= num_new_labels:
            for i in range(self.n_cur_labels, num_new_labels):
                self.qlabels[i].show()
                self.qlineedit[i].show()

        else: # new subwidgets need to be generated
            for i in range(num_tot_labels, num_new_labels):                   
                self.qlabels.append(QLabel(self))
                self.qlabels[i].setText(rt_label("dummy"))
    
                self.qlineedit.append(QLineEdit(""))
                self.qlineedit[i].setObjectName("dummy")
                self.qlineedit[i].installEventFilter(self)  # filter events

                # first entry is the title
                self.layGSpecs.addWidget(self.qlabels[i],i+1,0)
                self.layGSpecs.addWidget(self.qlineedit[i],i+1,1)

#------------------------------------------------------------------------------
    def sort_dict_freqs(self):
        """
        - Sort visible filter dict frequency spec entries with ascending frequency if 
             the sort button is activated
        - Update the visible QLineEdit frequency widgets

        The method is called when:
        - update_UI has been called after changing the filter design algorithm                                # that the response type has been changed 
          eg. from LP -> HP, requiring a different order of frequency entries
        - a frequency spec field has been edited
        - the sort button has been clicked (from filter_specs.py)
        """
        
        if fb.fil[0]['freq_specs_sort']:
            f_specs = [fb.fil[0][str(self.qlineedit[i].objectName())]
                                            for i in range(self.n_cur_labels)]
            f_specs.sort()
            for i in range(self.n_cur_labels):
                fb.fil[0][str(self.qlineedit[i].objectName())] = f_specs[i]
                
        self.load_dict()


#------------------------------------------------------------------------------

if __name__ == '__main__':

    from ..compat import QApplication
    app = QApplication(sys.argv)
    mainw = FreqSpecs(None)

    mainw.update_UI(new_labels = ['F_SB','F_SB2','F_PB','F_PB2'])
#    mainw.update_UI(new_labels = ['F_PB','F_PB2'])

    app.setActiveWindow(mainw) 
    mainw.show()
    sys.exit(app.exec_())
