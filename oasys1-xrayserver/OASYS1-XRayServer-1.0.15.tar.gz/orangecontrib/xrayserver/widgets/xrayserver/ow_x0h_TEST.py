__author__ = "Luca Rebuffi"

from orangewidget import gui
from orangewidget.settings import Setting
from oasys.widgets import gui as oasysgui
from oasys.widgets.exchange import DataExchangeObject
from oasys.util.oasys_util import ShowHtmlDialog

import urllib
from http import server

from orangecontrib.xrayserver.util.xrayserver_util import HttpManager, XRayServerPhysics, XRayServerGui
from orangecontrib.xrayserver.widgets.gui.ow_xrayserver_widget import XrayServerWidget, XrayServerException

from PyQt5 import QtGui, QtCore

import platform
if platform.system() == 'Darwin':
    from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
elif platform.system() == 'Linux':
    from PyQt5.QtWebKit import QWebView

APPLICATION = "/cgi/X0h_form.exe"

raise NotImplementedError()

class X0h(XrayServerWidget):
    name = "X0h TEST"
    description = "X0h TEST"
    icon = "icons/x0h.png"
    maintainer = "Luca Rebuffi"
    maintainer_email = "luca.rebuffi(@at@)elettra.eu"
    priority = 1
    category = "X0h"
    keywords = ["data", "file", "load", "read"]

    want_main_area = 1

    outputs = [{"name": "xrayserver_data",
                "type": DataExchangeObject,
                "doc": "xrayserver_data",
                "id": "xrayserver_data"}, ]


    xway = Setting(2)
    wave = Setting(0.0)
    line = Setting("Cu-Ka1")

    coway = Setting(0)
    code = Setting("Silicon")
    amor = Setting("")
    chem = Setting("")
    rho = Setting(0.0)

    i1 = Setting(1)
    i2 = Setting(1)
    i3 = Setting(1)

    df1df2 = Setting(1)
    detail = Setting(1)

    def __init__(self):
        super().__init__()


        self.setMaximumHeight(self.geometry().height())
        self.setMaximumWidth(self.geometry().width()+200)

        left_box_1 = oasysgui.widgetBox(self.controlArea, "X0h Request Form", addSpace=True, orientation="vertical",
                                         width=610, height=750)



        html = self.clear_input_form(HttpManager.send_xray_server_direct_request("/cgi/www_form.exe?template=X0h_form.htm"))

        html = html.split("<input type=SUBMIT value=\"Get X0h!\"><input type=RESET> <br>")[0]
        html += "\n</form>"
        html += "\n</td></tr></table>"
        html += "\n</td></tr></table>"
        html += "\n</body>"
        html += "\n</html>"

        print(html)

        self.x0h_input = QWebView(left_box_1)
        self.x0h_input.setHtml(html)

        left_box_1.layout().addWidget(self.x0h_input)

        self.x0h_input.setFixedHeight(520)
        self.x0h_input.setFixedWidth(590)

        gui.rubber(self.controlArea)

        self.tabs = []
        self.tabs_widget = oasysgui.tabWidget(self.mainArea)
        self.initializeTabs()

        self.x0h_output = QWebView(self.tabs[0])

        self.tabs[0].layout().addWidget(self.x0h_output)

        self.x0h_output.setFixedHeight(600)
        self.x0h_output.setFixedWidth(740)


    def clear_input_form(self, html):
        temp_1 = html.split("<body onload=\"setOnloads()\">")[0]
        temp_2 = html.split("<table cellspacing=0 cellpadding=0 border=0 bgcolor=\"#c1c1c1\"><tr><td>")[1]

        html = temp_1 + "\n<table cellspacing=0 cellpadding=0 border=0 bgcolor=\"#c1c1c1\"><tr><td>\n" + temp_2

        return html

    def getLeftPartWidth(self):
        return 620

    def set_xway(self):
        self.box_wave.setVisible(self.xway!=2)
        self.box_line.setVisible(self.xway==2)

    def set_coway(self):
        self.box_crystal.setVisible(self.coway==0)
        self.box_other.setVisible(self.coway==1)
        self.box_chemical.setVisible(self.coway==2)

    def set_rho(self):
        if not self.chem is None:
            if not self.chem.strip() == "":
                self.chem = self.chem.strip()
                self.rho = XRayServerPhysics.getMaterialDensity(self.chem)

    def initializeTabs(self):
        current_tab = self.tabs_widget.currentIndex()

        size = len(self.tabs)

        for index in range(0, size):
            self.tabs_widget.removeTab(size-1-index)

        self.tabs = [gui.createTabPage(self.tabs_widget, "X-ray Server Ouput"),
                     gui.createTabPage(self.tabs_widget, "Critical Angle for TER"),
                     gui.createTabPage(self.tabs_widget, "Darwin Curve (" + u"\u03C3" + " Pol.)"),
                     gui.createTabPage(self.tabs_widget, "Darwin Curve (" + u"\u03C0" + " Pol.)"),
                     ]

        for tab in self.tabs:
            tab.setFixedHeight(650)
            tab.setFixedWidth(750)

        self.plot_canvas = [None, None, None]

        self.tabs_widget.setCurrentIndex(current_tab)

    def submit(self):
        self.progressBarInit()
        self.setStatusMessage("Submitting Request")
        
        self.checkFields()

        parameters = {}

        parameters.update({"xway" : str(self.xway + 1)})
        parameters.update({"wave" : str(self.wave)})
        parameters.update({"line" : self.line})
        parameters.update({"coway" : str(self.coway)})
        parameters.update({"code" : self.code})
        parameters.update({"amor" : self.amor})
        parameters.update({"chem" : self.chem})
        parameters.update({"rho" : str(self.rho)})

        parameters.update({"i1" : str(self.i1)})
        parameters.update({"i2" : str(self.i2)})
        parameters.update({"i3" : str(self.i3)})
        parameters.update({"df1df2" : self.decode_df1df2()})

        parameters.update({"modeout" : "0" })
        parameters.update({"detail" : str(self.detail)})

        try:
            response = HttpManager.send_xray_server_request_POST(APPLICATION, parameters)
            response = self.clear_response(response)

            self.tabs_widget.setCurrentIndex(0)
            self.x0h_output.setHtml(response)

            data0, data1, data2 = self.extract_plots(response)

            exchange_data = DataExchangeObject("XRAYSERVER", "X0H")
            exchange_data.add_content("reflectivity", data0)
            exchange_data.add_content("reflectivity_units_to_degrees", 1.0)
            exchange_data.add_content("x-ray_diffraction_profile_sigma", data1)
            exchange_data.add_content("x-ray_diffraction_profile_sigma_units_to_degrees", 0.000277777805)
            exchange_data.add_content("x-ray_diffraction_profile_pi", data2)
            exchange_data.add_content("x-ray_diffraction_profile_pi_units_to_degrees", 0.000277777805)

            self.send("xrayserver_data", exchange_data)

        except urllib.error.HTTPError as e:
            self.x0h_output.setHtml('The server couldn\'t fulfill the request.\nError Code: '
                                    + str(e.code) + "\n\n" +
                                    server.BaseHTTPRequestHandler.responses[e.code][1])
            raise e

        except urllib.error.URLError as e:
            self.x0h_output.setHtml('We failed to reach a server.\nReason: '
                                    + e.reason)
            raise e

        except XrayServerException as e:
            ShowHtmlDialog.show_html("X-ray Server Error", e.response, width=750, height=500, parent=self)

            raise e
        except Exception as e:
            self.x0h_output.setHtml('We failed to reach a server.\nReason: '
                                    + str(e))

            raise e

        self.setStatusMessage("")
        self.progressBarFinished()

    def clear_response(self, response):
        # remove links
        output = response.split("<hr>")[0] + "\n</body></html>"

        # remove "get the curve" images
        output = "".join(output.split("<input type=image src=\"images/get_the_curve.gif\" border=0 width=102 height=12 alt=\"Get the reflectivity curve\">"))
        output = "".join(output.split("<input type=image src=\"images/get_the_curve.gif\" border=0 width=102 height=12 alt=\"Get the Bragg curve (sigma)\">"))
        output = "".join(output.split("<input type=image src=\"images/get_the_curve.gif\" border=0 width=102 height=12 alt=\"Get the Bragg curve (pi)\">"))
        # remove question mark images and links
        output = "".join(output.split("<a  href=\"javascript:void(0)\" onClick=\"Wfloat(\'images/x0h_help_0.gif\',\'x0h_0\',740,357);\"><b>?</b></a> &nbsp;"))
        output = "".join(output.split("<a  href=\"javascript:void(0)\" onClick=\"Wfloat(\'images/x0h_help_h.gif\',\'x0h_h\',705,853);\"><b>?</b></a> &nbsp;"))

        return output

    def checkFields(self):
        pass

    def decode_df1df2(self):
        if self.df1df2 == 0: return "-1"
        elif self.df1df2 == 1: return "0"
        elif self.df1df2 == 2: return "2"
        elif self.df1df2 == 3: return "4"
        elif self.df1df2 == 4: return "10"

    def extract_plots(self, response):
        form_1_begin = False
        form_2_begin = False
        form_3_begin = False

        form_1 = None
        form_2 = None
        form_3 = None

        rows = response.split("\r\n")

        for row in rows:
            if form_1_begin:
                if "<td>" in row:
                    form_1_begin = False
            elif form_2_begin:
                if "<td>" in row:
                    form_2_begin = False
            elif form_3_begin:
                if "<td>" in row:
                    form_3_begin = False

            if form_1_begin:
                form_1.append(row)
            elif form_2_begin:
                form_2.append(row)
            elif form_3_begin:
                form_3.append(row)

            if "/cgi/ter_form.pl" in row:
                if form_1 is None:
                    form_1 = []
                    form_1_begin = True

            if "/cgi/gid_form.pl" in row:
                if form_2 is None:
                    form_2 = []
                    form_2_begin = True
                elif form_3 is None:
                    form_3 = []
                    form_3_begin = True

        self.setStatusMessage("Plotting Results")

        if not form_1 is None:
            x_1, y_1 = self.get_plots_from_form("/cgi/ter_form.pl", form_1)

            self.plot_histo(x_1, y_1, 40, 1, 0, "Critical Angle for TER", "Incidence angle [degrees]", "Reflectivity")
            self.tabs_widget.setCurrentIndex(1)
        else:
            x_1 = None
            y_1 = None
            
        if not form_2 is None:
            x_2, y_2 = self.get_plots_from_form("/cgi/gid_form.pl", form_2)

            self.plot_histo(x_2, y_2, 60, 2, 1, "Darwin Curve ($\sigma$ Pol.)", "Scan Angle [arcsec]", "Diffracted Intensity")
            self.tabs_widget.setCurrentIndex(2)
        else:
            x_2 = None
            y_2 = None

        if not form_3 is None:
            x_3, y_3 = self.get_plots_from_form("/cgi/gid_form.pl", form_3)

            self.plot_histo(x_3, y_3, 80, 3, 2, "Darwin Curve ($\pi$ Pol.)", "Scan Angle [arcsec]", "Diffracted Intensity")
            self.tabs_widget.setCurrentIndex(3)
        else:
            x_3 = None
            y_3 = None

        return [x_1, y_1], [x_2, y_2], [x_3, y_3]


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    w = X0h()
    w.show()
    app.exec()
    w.saveSettings()


