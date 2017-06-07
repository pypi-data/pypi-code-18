import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def qc_plots(measurement_group, output_dir,
             start_date, end_date, w, tz):
    """Make PDF of all measurements in Measurement Group

       :param MeasurementGroup measurement_group: MeasurementGroup object to QC
       :param str output_dir: Path to directory where PDF file is written
       :param str start_date: Left x-axis bound of plots
       :param str end_date: Right x-axis bound of plots
       """
    fig_list = list()
    concat_method = measurement_group.concat_method
    start = pd.to_datetime(start_date).tz_localize(tz)
    end = pd.to_datetime(end_date).tz_localize(tz)
    if concat_method == 'concat_measurements':
        for m in measurement_group.meas_list:
            ts = m.data.loc[start:end]
            ts[start] = 0
            ts[end] = 0
            ts.sort_index(inplace=True)
            ts = ts.resample(w).mean()
            fig = plt.figure()
            if 'State' in m.quant:
                plt.step(ts.index, ts.values, color='b', rasterized=True,
                         label=m.label)
                plt.ylim(top=1.1, bottom=-0.1)
            elif 'Counts' in m.quant:
                plt.plot(ts, color='b', rasterized=True, label=m.label)
                plt.ylim(bottom=-1)
            else:
                plt.plot(ts.index, ts.values, color='b',
                         rasterized=True, label=m.label)
            mng = plt.get_current_fig_manager()
            mng.window.showMaximized()
            plt.title(m.name.split('_')[0])
            plt.legend(loc='upper right')
            plt.ylabel(m.quant + ' ' + '[' + m.dim + ']')
            plt.xlabel('Time')
            plt.grid()
            fig_list.extend(
                [manager.canvas.figure
                 for manager in
                 matplotlib._pylab_helpers.Gcf.get_all_fig_managers()])
            plt.close('all')
    elif concat_method == 'concat_dataframes':
        for column_name in measurement_group.meas_df:
            mng = plt.get_current_fig_manager()
            mng.window.showMaximized()
            plt.plot(measurement_group.meas_df[column_name], color='b',
                     rasterized=True)
            plt.title(column_name)
            plt.xlabel('Time')
            plt.grid()
            fig_list.extend(
                [manager.canvas.figure
                 for manager in
                 matplotlib._pylab_helpers.Gcf.get_all_fig_managers()])
            plt.close('all')
    pdf_path = output_dir + '\\' + measurement_group.name + ' QC Plots.pdf'
    pdf = PdfPages(pdf_path)
    for fig in fig_list:
        pdf.savefig(fig)
    pdf.close()
