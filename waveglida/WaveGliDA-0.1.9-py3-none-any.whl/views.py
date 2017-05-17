import os
import json
from glob import glob
from flask import render_template, Blueprint, request, Response, send_file

from .read_wg_data import read_wg_flist
from .calculations import do_calculations as calcs
from flask import current_app as app


class DataObj(object):

    def __init__(self):
        self.df = None
        self.number_of_files = None
        self.map_selection = None
        self.plot_selection = [False, False]


views = Blueprint('views', __name__, template_folder='templates')
cache = DataObj()


@views.route('/')
@views.route('/about/', methods=['GET'])
def page_about():
    import re
    # from markdown2 import Markdown
    from inspect import getsourcelines
    from .calculations import water_vapour_pressure, \
        virial_expansion, \
        temperature_correction, \
        LI820_raw
    from pygments import highlight
    from pygments.lexers.python import Python3Lexer
    from pygments.formatters import HtmlFormatter

    calc_html = ''
    func_list = [water_vapour_pressure,
                 temperature_correction,
                 virial_expansion,
                 LI820_raw]
    for func in func_list:
        name = "<h2><code>{}</code></h2>".format(func.__name__)
        code = ''.join(getsourcelines(func)[0])
        code = highlight(code, Python3Lexer(), HtmlFormatter(style='colorful'))
        calc_html += '{}<br>{}'.format(name, code)

    calc_html = re.split('<h2>', calc_html, flags=re.DOTALL)
    calc_html = [[c] + grp.split('</h2>') for c, grp in enumerate(calc_html)][1:]

    info_path = os.path.join(app.root_path, app.template_folder, 'info.html')
    info_html = open(info_path).read()

    return render_template('about.html',
                           about_text=info_html,
                           info_text=calc_html)


@views.route('/import_data/', methods=['GET'])
def page_import_select():

    if cache.df is not None:
        table_html = dataframe_to_html(cache.df)
        return render_template("import.html", table=table_html, number_of_files=cache.number_of_files)
    else:
        return render_template("import.html")


@views.route('/import_data/', methods=['POST'])
def upload_files():

    # remove old files
    old_files = glob(os.path.join(app.config['UPLOAD_DIR'] + "/*"))
    print (old_files)
    for file in old_files:
        os.remove(file)

    # upload the new files
    file_objects = request.files.getlist('files[]')
    file_list = []
    for file in file_objects:
        fname = os.path.join(app.config['UPLOAD_DIR'], file.filename)
        file.save(fname)
        file_list += fname,
    file_list = sorted(file_list)

    num_files = "{} files uploaded".format(len(file_list))
    cache.number_of_files = num_files

    cache.df = read_wg_flist(file_list)
    cache.df = calcs(cache.df)
    table_html = dataframe_to_html(cache.df)

    return render_template("import.html",
                           number_of_files=num_files,
                           table=table_html)


@views.route('/download_csv/')
def download_csv():
    from datetime import datetime
    fname = datetime.today().strftime('wgData_%Y%m%d-%H%M.csv')
    return Response(cache.df.to_csv(None),
                    mimetype="text/csv",
                    headers={"Content-disposition":
                             "attachment; filename={}".format(fname)})


@views.route('/download_xls/')
def download_xls():
    from datetime import datetime
    from pyexcelerate import Workbook

    fname = app.config['UPLOAD_DIR'] + datetime.today().strftime('wgData_%Y%m%d-%H%M.xlsx')

    df = cache.df.reset_index()
    xls = [df.columns.tolist(), ] + df.values.tolist()
    wb = Workbook()
    ws = wb.new_sheet("Sheet 1", data=xls)
    ws.get_col_style(1).format.format = 'yyyy-mm-dd hh:mm'
    wb.save(fname)

    return send_file(fname, as_attachment=True)


@views.route('/plots_map/', methods=["GET", "POST"])
def plots_map_page():

    if cache.df is None:
        kwargs = {}
    else:
        plotting_vars = get_plotting_vars(cache.df)
        slct = request.form.getlist("selection[]")

        if (request.method.upper() == 'GET') & bool(cache.map_selection):
            slct = cache.map_selection
        else:
            slct = plotting_vars[0] if slct == [] else slct[0]
            cache.map_selection = slct

        map_ids, map_JSON = map_graph_ids(cache.df, slct)
        kwargs = {"selected": slct,
                  "data_processed": True,
                  "graphJSON": map_JSON,
                  "plot_vars": plotting_vars,
                  "ids": map_ids}

    return render_template('plots_map.html', **kwargs)


@views.route('/plots_timeseries/', methods=['GET', 'POST'])
def update_plot():
    if cache.df is None:
        kwargs = {}
    else:
        plotting_vars = get_plotting_vars(cache.df)
        slct_1 = request.form.getlist("selection_1[]")
        slct_2 = request.form.getlist("selection_2[]")

        if (request.method.upper() == 'GET') & any(cache.plot_selection):
            slct_1 = cache.plot_selection[0]
            slct_2 = cache.plot_selection[1]
        else:
            slct_1 = slct_2 if slct_1 == [] else slct_1
            slct_1 = [plotting_vars[0]] if slct_1 == [] else slct_1
            slct_2 = [] if slct_1 == slct_2 else slct_2
            cache.plot_selection = [slct_1, slct_2]

        ids, graphJSON = plot_graph_ids(cache.df[slct_1], cache.df[slct_2])

        kwargs = {"data_processed": True,
                  "plot_vars": plotting_vars,
                  "selected_1": slct_1,
                  "selected_2": slct_2,
                  "ids": ids,
                  "graphJSON": graphJSON,
                  }

    return render_template('plots_timeseries.html', **kwargs)


@views.route('/config_page/', methods=["GET"])
def config_page():
    make_table_json(app.config['PLOTTING_NAMES'])

    kwargs = {
        "latmin": app.config['MAP_DOMAIN']['lat'][0],
        "latmax": app.config['MAP_DOMAIN']['lat'][1],
        "lonmin": app.config['MAP_DOMAIN']['lon'][0],
        "lonmax": app.config['MAP_DOMAIN']['lon'][1],
        # "slct_browser": config.BROWSER,
        # "browser": browsers()
    }

    return render_template("config.html", **kwargs)


@views.route('/config_page/', methods=["POST"])
def update_config():

    app.config['PLOTTING_NAMES'] = json.loads(request.form.getlist("table_data")[0])
    app.config['MAP_DOMAIN']['lat'][0] = request.form.getlist("latmin")[0]
    app.config['MAP_DOMAIN']['lat'][1] = request.form.getlist("latmax")[0]
    app.config['MAP_DOMAIN']['lon'][0] = request.form.getlist("lonmin")[0]
    app.config['MAP_DOMAIN']['lon'][1] = request.form.getlist("lonmax")[0]
    make_table_json(app.config['PLOTTING_NAMES'])

    fname = os.path.join(app.root_path, "static/json/config.json")
    with open(os.path.normpath(fname), 'r') as f:
        data = json.load(f)
        data['plotting_names'] = app.config['PLOTTING_NAMES']
        data['map_defaults']['lat'] = app.config['MAP_DOMAIN']['lat']
        data['map_defaults']['lon'] = app.config['MAP_DOMAIN']['lon']

    os.remove(fname)
    with open(fname, 'w') as f:
        json.dump(data, f)

    kwargs = dict(
        latmin=app.config['MAP_DOMAIN']['lat'][0],
        latmax=app.config['MAP_DOMAIN']['lat'][1],
        lonmin=app.config['MAP_DOMAIN']['lon'][0],
        lonmax=app.config['MAP_DOMAIN']['lon'][1],
        # slct_browser=config.BROWSER,
        # browser=browsers(),
    )

    return render_template("config.html", **kwargs)


@views.route('/shutdown/', methods=['GET'])
def initiate_shutdown():
    # remove old files
    [os.remove(f) for f in glob(os.path.join(app.config['UPLOAD_DIR'] + "/*"))]

    func = request.environ.get('werkzeug.server.shutdown')
    try:
        func()
    except:
        print('Not running with the Werkzeug Server')

    return render_template('shutdown.html')


def make_table_json(plot_names):
    from json import dumps

    metadata = [
        {"name": "key", "label": "DATA KEY", "datatype": "string", "editable": False},
        {"name": "plot_name", "label": "PLOTTING NAME", "datatype": "string", "editable": True},
    ]

    json_dict = {"metadata": metadata, "data": []}
    for i, key in enumerate(plot_names):
        nice_name = plot_names[key]
        values = {"key": key, "plot_name": nice_name}
        line = {"id": i, "values": values}
        json_dict["data"] += line,

    fname = os.path.join(app.root_path, "static/json/pretty_names_table.json")
    file = open(os.path.normpath(fname), 'w')
    file.write(dumps(json_dict))
    file.close()


def dataframe_to_html(df):
    from re import findall, DOTALL
    """pd.DataFrame to HTML and changes class to table and removes border"""

    drop_names = df.filter(regex="Span|Pump|Zero|Ave|SD|Flags|Volt|Raw").columns
    i = list(range(72)) + list(range(-72, 0))
    i = i if df.shape[0] > len(i) else list(range(df.shape[0]))
    df = df.iloc[i].drop(drop_names, axis=1).copy()
    html = df.to_html(max_rows=140,
                      classes="table table-condensed table-striped table-bordered",
                      float_format='%.5g',)
    table = html.replace('border="1"', '')
    # removing second header row
    thead = findall('(<thead.*?>.*?</thead>)', table, flags=DOTALL)
    if thead is not []:
        thead = thead[0]

        rows = findall('(<tr.*?>.*?</tr>)', thead, flags=DOTALL)
        if len(rows) == 2:
            r0_col0 = findall('(<th.*?>.*?</th>)', rows[0])[0]
            r1_col0 = findall('(<th.*?>.*?</th>)', rows[1])[0]

            table = table.replace(rows[1], '')
            table = table.replace(r0_col0, r1_col0)

    return table


def get_plotting_vars(df):
    from numpy import sort

    plotting_vars = []
    for key in app.config['PLOTTING_NAMES']:
        has_name = app.config['PLOTTING_NAMES'][key] != ""
        is_indata = key in df.keys()
        if has_name & is_indata:
            dtype = df[key].dtype
            if (dtype == float) | (dtype == int):
                plotting_vars += key,

    return sort(plotting_vars)


def map_graph_ids(df, varname):
    from .plotly_json import PlotlyJSONEncoder
    from json import dumps

    scl = (  # jet equivalent
        [0.000, "rgb(255, 0, 0)"],
        [0.125, "rgb(255, 111, 0)"],
        [0.250, "rgb(255, 234, 0)"],
        [0.375, "rgb(151, 255, 0)"],
        [0.500, "rgb(44, 255, 150)"],
        [0.625, "rgb(0, 152, 255)"],
        [0.750, "rgb(0, 25, 255)"],
        [0.875, "rgb(0, 0, 200)"],
        [1.000, "rgb(150,0,90)"],
    )

    qL, qU = df[varname].quantile([.01, .99]).values

    data = [dict(
        lat=df['Latitude'],
        lon=df['Longitude'],
        text=df[varname].astype(str),
        marker=dict(
            color=df[varname].clip(qL, qU),
            colorscale=scl,
            reversescale=True,
            symbol='circle',
            opacity=0.7,
            size=4,
            colorbar=dict(
                thickness=15,
                title=app.config['PLOTTING_NAMES'][varname],
                xanchor='left',
                x=1.0,
                xpad=0,
                ypad=0,
                titleside="right",
                outlinecolor="rgba(68, 68, 68, 0)",
                ticklen=0,
            ),
        ),
        type='scattergeo'
    )]

    map_tick_interval = 5
    layout = dict(
        colorbar=True,
        margin={'l': 0, 'r': 70, 't': 30, 'b': 20},
        geo=dict(
            projection=dict(type="orthographic"),
            resolution=85,
            framecolor='#EEE',
            showland=True,
            landcolor="rgb(250, 250, 250)",
            countrycolor="rgb(217, 217, 217)",
            countrywidth=0.5,
            lonaxis=dict(
                showgrid=True,
                gridwidth=0.5,
                range=app.config['MAP_DOMAIN']['lon'],
                dtick=map_tick_interval
            ),
            lataxis=dict(
                showgrid=True,
                gridwidth=0.5,
                range=app.config['MAP_DOMAIN']['lat'],
                dtick=map_tick_interval,
            ),
        ),
    )

    graphs = [dict(layout=layout,
                   data=data,
                   displaylogo=False,
                   showlink=True)]

    map_ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
    map_json = dumps(graphs, cls=PlotlyJSONEncoder)

    return map_ids, map_json


def plot_graph_ids(df1, df2):
    from .plotly_json import PlotlyJSONEncoder
    from json import dumps

    layout = dict(height=440,
                  showledgend=True,
                  margin=dict(l=70, r=70, t=40, b=70),
                  legend=dict(orientation='h', yanchor="top", xanchor="center", x=0.5, y=-0.1),
                  xaxis=dict(showlines=True, linewidths=1, mirror='all', linecolor='#EEE', ticklen=0),
                  yaxis=dict(showlines=True, linewidths=1, mirror='all', linecolor='#EEE', ticklen=0),)

    lines = []
    for key in df1:
        lines += dict(x=df1.index, y=df1[key], name=key, yaxis='y1'),
    layout['yaxis']['title'] = app.config['PLOTTING_NAMES'][key] if df1.shape[1] == 1 else ''

    if df2.keys().tolist() != []:
        for key in df2:
            lines += dict(x=df2.index, y=df2[key], name=key, yaxis='y2'),
        layout['yaxis2'] = dict(showlines=True,
                                linewidths=1,
                                title=app.config['PLOTTING_NAMES'][key] if df2.shape[1] == 1 else '',
                                mirror='all',
                                linecolor='#EEE',
                                ticklen=0,
                                zeroline=False,
                                overlaying='y',
                                side='right',
                                showgrid=False,
                                zerolines=False)

    graphs = [dict(layout=layout, data=lines, displaylogo=False, displayModeBar=True, showlink=True)]

    ids = ['graph-{}'.format(i) for i, _ in enumerate(graphs)]
    graphJSON = dumps(graphs, cls=PlotlyJSONEncoder)

    return ids, graphJSON


def browsers():

    browsers = {
        "default": "Operating system default",
        "safari": "Safari (OS X only)",
        "firefox": "Mozilla Firefox",
        "opera": "Opera browser",
        "google-chrome": "Google Chrome",
    }
    return browsers
