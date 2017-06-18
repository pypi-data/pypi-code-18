# -*- coding: utf-8 -*-
import os
import sys
from enum import Enum

# usiamo la codifica utf8
reload(sys)
sys.setdefaultencoding('utf8')

#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
CHART_ROOT_PATH = os.path.join(os.path.dirname(__file__),'chartjslib/')

class Chart():
    TITLE = "$__TITLE__$"
    CONFIG_TYPE = "$__CONFIG_TYPE__$"
    LABEL_LIST = "$__LABEL_LIST__$"
    DATASET = "$__DATA_SET__$"
    SCALES = "$__SCALES__$"
    X_LABEL = "$__X_LABEL__$"
    Y_LABEL = "$__Y_LABEL__$"

    apici = ['label', 'type']
    none_value = [None]
    mapped_value = {True:'true', False:'false'}

    def __init__(self, canvas='myCanvas',
                       title='Chart.js Line Chart',
                       config_type='line',
                       x_label=None,
                       y_label=None):

        self.SCALES_DATA = """
                        scales: {
                            xAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: '""" + self.X_LABEL + """'
                                }
                            }],
                            yAxes: [{
                                display: true,
                                scaleLabel: {
                                    display: true,
                                    labelString: '""" + self.Y_LABEL + """'
                                }
                            }]
                        }
        """
        self.HTML_CODE = """<!doctype html>
        <html>

        <head>
            <title>Line Chart</title>
            <script SRC=/chartjslib/modules/Chart.bundle.min.js></script>
            <script SRC=/chartjslib/modules/utils.js></script>
            <style>
            canvas{
                -moz-user-select: none;
                -webkit-user-select: none;
                -ms-user-select: none;
            }
            </style>
        </head>

        <body>
            <div style='width:60%;'>
                <canvas id='""" + canvas + """'></canvas>
            </div>
            <script>
                var color = Chart.helpers.color;
                var config = {
                    type: '""" + self.CONFIG_TYPE + """',
                    data: {
                        labels: """ + self.LABEL_LIST + """,
                        datasets:  [""" + self.DATASET + """]
                    },
                    options: {
                        responsive: true,
                        title:{
                            display:true,
                            text: '""" + self.TITLE + """'
                        },
                        tooltips: {
                            mode: 'index',
                            intersect: false,
                        },
                        hover: {
                            mode: 'nearest',
                            intersect: true
                        },
                        animation: {
                            animateScale: true,
                            animateRotate: true
                        },
                        """ + self.SCALES + """
                    }
                };

                window.onload = function() {
                    var ctx = document.getElementById('"""+canvas+"""').getContext('2d');
                    window.myLine = new Chart(ctx, config);
                };
            </script>
        </body>

        </html>
        """
        self.canvas = canvas
        self.config_type = config_type
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.dataset = []

    def setlabel_list(self, label_list = list()):
        self.label_list = label_list

    def getlabel_list(self, ):
        return str(self.label_list)

    def createDataset(self, label='Unfilled',
                         type=None,
                         fill=False,
                         backgroundColor='window.chartColors.red',
                         borderColor='window.chartColors.red',
                         pointBackgroundColor='window.chartColors.red',
                         borderWidth=3,
                         borderDash=None,
                         data=list()):
        local_dict={}
        local_dict['label'] = label
        local_dict['type'] = type
        local_dict['fill'] = fill
        local_dict['backgroundColor'] = backgroundColor
        local_dict['pointBackgroundColor'] = pointBackgroundColor
        local_dict['borderColor'] = borderColor
        local_dict['borderWidth'] = borderWidth
        local_dict['borderDash'] = borderDash
        local_dict['data'] = data



        return local_dict

    def getdataset(self):
        ret_str = ''
        for ds in self.dataset:
            ret_str = ret_str + '{'
            for k in ds:
                if ds[k] not in self.none_value:
                    nv = ds[k]
                    if not isinstance(ds[k], (list)):
                        nv = self.mapped_value.get(ds[k],ds[k])
                    if k in self.apici:
                        ret_str = ret_str + k + ': "' + str(nv) + '",'
                    else:
                        ret_str = ret_str + k + ': ' + str(nv) + ','
            ret_str = ret_str + '},'

        return ret_str

    def getChart(self):
        #title = 'Chart.js Line Chart',
        #config_type = 'line',
        #label = '["G", "F", "M", "A"]',
        #x_label = 'Month',
        #y_label = 'Value'):

        main_page = self.HTML_CODE.replace(self.CONFIG_TYPE, self.config_type)
        main_page = main_page.replace(self.TITLE, self.title)
        main_page = main_page.replace(self.LABEL_LIST, self.getlabel_list())
        if self.x_label and self.y_label:
            main_page = main_page.replace(self.SCALES, self.SCALES_DATA)
            main_page = main_page.replace(self.X_LABEL, self.x_label)
            main_page = main_page.replace(self.Y_LABEL, self.y_label)
        else:
            main_page = main_page.replace(self.SCALES, '')

        main_page = main_page.replace(self.DATASET, self.getdataset())
        main_page = main_page.replace(self.DATASET, self.getdataset())

        #print main_page
        return main_page