from __future__ import print_function
from __future__ import division

from topiceval.usereval import senddata

import numpy as np

import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox
import topiceval.usereval.topicevalGUI as topicevalGUI
import os
import pickle

# try:
#     _fromUtf8 = QtCore.QString.fromUtf8
# except AttributeError:
#     def _fromUtf8(s):
#         return s


class TopicEvalWindowClass(QtWidgets.QDialog, topicevalGUI.Ui_Dialog):
    """Contains elements for the Warden GUI Window
    Sets up all elements of various function windows
    Opens with Login Window
    """

    def __init__(self, models, dirname, num_topics, threaded):

        QtWidgets.QDialog.__init__(self)
        self.setupUi(self)

        self.i = 0
        self.all_models = models
        self.dirname = dirname
        self.num_topics = num_topics
        self.threaded = threaded
        self.wordspertopic = 10
        self.states = [0]*3
        self.mapping = [0, 1, 2]

        self.listWidgets = [self.listWidget_1, self.listWidget_2, self.listWidget_3]
        self.showNext10PushButtons = [self.showNext10PushButton_1, self.showNext10PushButton_2, 
                                      self.showNext10PushButton_3]
        self.showPrevious10PushButtons = [self.showPrevious10PushButton_1, self.showPrevious10PushButton_2,
                                          self.showPrevious10PushButton_3]
        self.buttonGroups = [self.buttonGroup_1, self.buttonGroup_2, self.buttonGroup_3]

        path = os.path.dirname(os.path.abspath(__file__)) + "/resources/icon.png"
        self.setWindowIcon(QtGui.QIcon(path))

        path = os.path.dirname(os.path.abspath(__file__)) + "/resources/bkdimage.jpg"
        self.bkdLabel.setPixmap(QtGui.QPixmap(path))
        self.bkdLabel.setScaledContents(True)

        self.nextCommandLinkButton.clicked.connect(self.show_next_topic)

        # TODO: Fix this, using lambda in for loop is not working as it takes the final value of i for every button
        self.showNext10PushButtons[0].clicked.connect(lambda: self.show_next_10(0))
        self.showNext10PushButtons[1].clicked.connect(lambda: self.show_next_10(1))
        self.showNext10PushButtons[2].clicked.connect(lambda: self.show_next_10(2))
        self.showPrevious10PushButtons[0].clicked.connect(lambda: self.show_previous_10(0))
        self.showPrevious10PushButtons[1].clicked.connect(lambda: self.show_previous_10(1))
        self.showPrevious10PushButtons[2].clicked.connect(lambda: self.show_previous_10(2))
        for buttonGroup in self.buttonGroups:
            buttonGroup.buttonClicked.connect(self.groupbutton_clicked)
        for i in range(len(self.states)):
            # self.showNext10PushButtons[i].clicked.connect(lambda: self.show_next_10(i))
            # self.showPrevious10PushButtons[i].clicked.connect(lambda: self.show_previous_10(i))
            self.update_gui(i)

        # self.topicimageLabel.setPixmap(QtGui.QPixmap(dirname + '/topic%d.png' % self.i))
        # self.topicimageLabel.setScaledContents(True)

        # self.label_2.setPixmap(QtGui.QPixmap(('src/ui/resources/bkd1edit2.jpg')))
        # self.label_2.setScaledContents(True)
        #
        # self.label_3.setPixmap(QtGui.QPixmap(('src/ui/resources/bkd1edit2.jpg')))
        # self.label_3.setScaledContents(True)
        #
        # self.label_5.setPixmap(QtGui.QPixmap(('src/ui/resources/bkd1edit2.jpg')))
        # self.label_5.setScaledContents(True)
        #
        # self.label_6.setPixmap(QtGui.QPixmap(('src/ui/resources/bkd1edit2.jpg')))
        # self.label_6.setScaledContents(True)
        #
        # self.label_7.setPixmap(QtGui.QPixmap(('src/ui/resources/bkd1edit2.jpg')))
        # self.label_7.setScaledContents(True)
        #
        # self.label_9.setPixmap(QtGui.QPixmap(('src/ui/resources/bkd1edit2.jpg')))
        # self.label_9.setScaledContents(True)
        #
        # self.label_32.setPixmap(QtGui.QPixmap(('src/ui/resources/bkd1edit2.jpg')))
        # self.label_32.setScaledContents(True)

        # self.pushButton_10.clicked.connect(self.password_validate)
        # self.pushButton.clicked.connect(self.submit_grant_request)
        # self.pushButton_2.clicked.connect(self.fire_worker)
        # self.pushButton_3.clicked.connect(self.hire_new_worker)
        # self.pushButton_4.clicked.connect(self.print_account_statement)
        # self.pushButton_5.clicked.connect(self.pay_salaries)
        # self.pushButton_6.clicked.connect(self.gen_salary_list)
        # self.pushButton_7.clicked.connect(self.view_complaint_button)
        # self.pushButton_8.clicked.connect(self.post_atr_button)

    # def show_next_image(self):
    #     if self.i >= self.num_topics:
    #         return
    #     self.topicimageLabel.setPixmap(QtGui.QPixmap(self.dirname + '/topic%d.png' % self.i))
    #     self.topicimageLabel.setScaledContents(True)
    #     self.i += 1
    #     if self.i >= self.num_topics:
    #         self.nextCommandLinkButton.setText("Finish!")
    #     return

    def scores_update(self):
        for i, group in enumerate(self.buttonGroups):
            score = int(group.checkedButton().text())
            modelnum = self.mapping[i]
            self.all_models[modelnum].representative_topics_scores.append(score)
        return

    def unselect_radiobuttons(self):
        for buttonGroup in self.buttonGroups:
            buttonGroup.setExclusive(False)
            for button in buttonGroup.buttons():
                button.setChecked(False)
            buttonGroup.setExclusive(True)
        return

    def groupbutton_clicked(self):
        all_selected_flag = True
        for group in self.buttonGroups:
            if group.checkedId() == -1:
                all_selected_flag = False
                break
        if all_selected_flag:
            self.nextCommandLinkButton.setEnabled(True)
        else:
            self.nextCommandLinkButton.setEnabled(False)
        return

    def show_next_10(self, i):
        self.states[i] += 1
        self.update_gui(i)
        return

    def show_previous_10(self, i):
        self.states[i] -= 1
        self.update_gui(i)
        return

    def show_next_topic(self):
        self.i += 1
        self.mapping = np.random.choice(len(self.all_models), 3, replace=False)
        self.scores_update()
        if self.i >= self.num_topics:
            self.states = [-1]*len(self.states)
        else:
            self.states = [0] * len(self.states)
        for i in range(len(self.states)):
            self.update_gui(i)
        return

    def show_topic(self, i):
        start = (self.states[i]-1)*self.wordspertopic
        end = start + self.wordspertopic
        total_weight, strings = self.tuples_to_strings(start=start, end=end, i=i)
        self.listWidgets[i].addItems(["Total Wt (%d:%d)" % (start+1, end), "(%0.3f)" % total_weight, ""])
        self.listWidgets[i].item(1).setTextAlignment(132)   # centering
        self.listWidgets[i].item(0).setTextAlignment(132)   # centering
        self.listWidgets[i].addItems(strings)
        return

    def update_gui(self, i):
        state = self.states[i]
        if state == 0:
            self.states[i] = 1
            self.listWidgets[i].clear()
            self.show_topic(i)
            self.showNext10PushButtons[i].setEnabled(True)
            self.showPrevious10PushButtons[i].setEnabled(False)
            self.unselect_radiobuttons()
            self.nextCommandLinkButton.setEnabled(False)
        if state == 1:
            self.listWidgets[i].clear()
            self.show_topic(i)
            self.showNext10PushButtons[i].setEnabled(True)
            self.showPrevious10PushButtons[i].setEnabled(False)
            # self.nextCommandLinkButton.setEnabled(False)
        elif state == 2:
            self.listWidgets[i].clear()
            self.show_topic(i)
            self.showNext10PushButtons[i].setEnabled(True)
            self.showPrevious10PushButtons[i].setEnabled(True)
            # self.nextCommandLinkButton.setEnabled(True)
        elif state == 3:
            self.listWidgets[i].clear()
            self.show_topic(i)
            self.showNext10PushButtons[i].setEnabled(False)
            self.showPrevious10PushButtons[i].setEnabled(True)
            # self.nextCommandLinkButton.setEnabled(True)
        elif state == -1:
            for listWidget in self.listWidgets:
                listWidget.clear()
            for showPrevious10PushButton in self.showPrevious10PushButtons:
                showPrevious10PushButton.setEnabled(False)
            for showNext10PushButton in self.showNext10PushButtons:
                showNext10PushButton.setEnabled(False)
            self.nextCommandLinkButton.setEnabled(True)
            self.nextCommandLinkButton.setText("Submit")
            self.nextCommandLinkButton.clicked.connect(self.showdialog)
        return

    def showdialog(self):
        os.remove(self.dirname + "corpus.npy")
        os.remove(self.dirname + "dfindices_in_corpus.npy")
        os.remove(self.dirname + "emails.pkl")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Thank you! Ready to send results!")
        msg.setInformativeText("The results will be sent via email. Privacy is of utmost importance and only the "
                               "topic matrix (the top words of which you scored) and the scores will be sent.")
        msg.setWindowTitle("Submit Results")
        msg.setDetailedText("The details of files being sent are as follows: 1) topic matrices: the word-probability"
                            " distribution of topics, the top words were shown and ranked by you. "
                            "2) Your scores for the topics "
                            "3) This data will be sent to t-avsriv@microsoft.com")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        msg.buttonClicked.connect(self.msgbtn)
        sys.exit(msg.exec_())

    def msgbtn(self, i):
        if i.text() == "OK":
            self.submit()
        else:
            buttonReply = QMessageBox.question(self, 'Really Quit', "The scores won't be sent. Quit(Yes) "
                                                                    "or Submit(\"No\")?",
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                self.close()
            else:
                self.submit()
        return

    def submit(self):
        threaded = self.threaded
        shown_topic_tuples = []
        shown_topic_scores = []
        for model in self.all_models:
            if model.modelname == "bcd":
                model.save_H_matrix(self.dirname + "bcd_threaded" + str(threaded) + "_H_matrix.npy")
                model.save_W_matrix(self.dirname + "bcd_threaded" + str(threaded) + "_W_matrix.npy")
            else:
                model.save_M_matrix(self.dirname + model.modelname + "_threaded" + str(threaded) + "_M_matrix.npy")
            shown_topic_tuples.append([model.modelname, threaded,
                                       model.representative_topic_tuples[:self.num_topics]])
            shown_topic_scores.append(model.representative_topics_scores)

        with open(self.dirname + "shown_topic_tuples.npy", "wb") as handle:
            pickle.dump(shown_topic_tuples, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(self.dirname + "shown_topic_scores.npy", "wb") as handle:
            pickle.dump(shown_topic_scores, handle, protocol=pickle.HIGHEST_PROTOCOL)
        # np.save(dirname + "shown_topic_tuples.npy", shown_topic_tuples)
        # np.save(dirname + "shown_topic_scores.npy", shown_topic_scores)
        senddata.makezip(self.dirname)
        senddata.sendmail()
        QMessageBox.information(self, 'Success', "Results sent successfully!")
        return

    def tuples_to_strings(self, start, end, i):
        if self.i >= self.num_topics:
            return
        tuple_list = self.all_models[self.mapping[i]].representative_topic_tuples[self.i][start:end]
        strings = ["%s (%0.3f)" % (tup[0], tup[1]) for tup in tuple_list]
        total_weight = 0.
        for tup in tuple_list:
            total_weight += tup[1]
        return total_weight, strings

    # def closeEvent(self, event):
    #
    #     quit_msg = "Are you sure you want to exit the program?"
    #     reply = QMessageBox.question(self, 'Message',
    #                                        quit_msg, QMessageBox.Yes, QMessageBox.No)
    #
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()


def main(models, dirname, num_topics, threaded):
    app = QApplication(sys.argv)
    window = TopicEvalWindowClass(models=models, dirname=dirname, num_topics=num_topics, threaded=threaded)
    window.show()
    app.exec_()
    return
