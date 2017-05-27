# -*- coding: utf-8 -*-
import os
import sys
import logging
import time

# usiamo la codifica utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')
CHART_ROOT_PATH = os.path.join(os.path.dirname(__file__),'js/')

HTML_CODE = """<!doctype html>
<html>

<head>
    <title>Line Chart</title>
    <script SRC=/js/module/Chart.bundle.min.js></script>
    <script SRC=/js/module/utils.js></script>
    <style>
    canvas{
        -moz-user-select: none;
        -webkit-user-select: none;
        -ms-user-select: none;
    }
    </style>
</head>

<body>
    <div style="width:60%;">
        <canvas id="myCanvas"></canvas>
    </div>
    <script>
        var config = {
            type: 'line',
            data: {
                labels: ["G", "F", "M", "A"],
                datasets: [{
                    label: "Unfilled",
                    fill: false,
                    backgroundColor: window.chartColors.blue,
                    borderColor: window.chartColors.blue,
                    data: [
                        10, 
                        20, 
                        8, 
                        6
                    ],
                }, {
                    label: "Dashed",
                    fill: false,
                    backgroundColor: window.chartColors.green,
                    borderColor: window.chartColors.green,
                    borderDash: [5, 5],
                    data: [
                        15, 
                        11, 
                        22, 
                        3
                    ],
                }, {
                    label: "Filled",
                    backgroundColor: window.chartColors.red,
                    borderColor: window.chartColors.red,
                    data: [
                        88, 
                        16, 
                        21, 
                        11
                    ],
                    fill: true,
                }]
            },
            options: {
                responsive: true,
                title:{
                    display:true,
                    text:'Chart.js Line Chart'
                },
                tooltips: {
                    mode: 'index',
                    intersect: false,
                },
                hover: {
                    mode: 'nearest',
                    intersect: true
                },
                scales: {
                    xAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Month'
                        }
                    }],
                    yAxes: [{
                        display: true,
                        scaleLabel: {
                            display: true,
                            labelString: 'Value'
                        }
                    }]
                }
            }
        };

        window.onload = function() {
            var ctx = document.getElementById("myCanvas").getContext("2d");
            window.myLine = new Chart(ctx, config);
        };
    </script>
</body>

</html>
"""

class Chart():
    def __init__(self, name):
        self.name = name

    def getChart(self):
        return HTML_CODE
