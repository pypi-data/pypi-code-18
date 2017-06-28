"""This is the docstring for the example.py module.  Modules names should
have short, all-lowercase names.  The module name may have underscores if
this improves readability.
Every module should have a docstring at the very top of the file.  The
module's docstring may extend over multiple lines.  If your docstring does
extend over multiple lines, the closing three quotation marks must be on
a line by itself, preferably preceded by a blank line."""

__copyright__ = "tba"
__license__ = "tba"
__author__ = "tba"


"""This is the docstring for the example.py module.  Modules names should
have short, all-lowercase names.  The module name may have underscores if
this improves readability.
Every module should have a docstring at the very top of the file.  The
module's docstring may extend over multiple lines.  If your docstring does
extend over multiple lines, the closing three quotation marks must be on
a line by itself, preferably preceded by a blank line."""

__copyright__ = "tba"
__license__ = "tba"
__author__ = "tba"


This is the docstring for the example.py module.  Modules names should
have short, all-lowercase names.  The module name may have underscores if
this improves readability.
Every module should have a docstring at the very top of the file.  The
module's docstring may extend over multiple lines.  If your docstring does
extend over multiple lines, the closing three quotation marks must be on
a line by itself, preferably preceded by a blank line.

__copyright__ = "tba"
__license__ = "tba"
__author__ = "tba"


import pandas as pd
import os
from egopowerflow.tools.tools import oedb_session
from dataprocessing.tools import io
import json
from geoalchemy2.shape import to_shape
from bokeh.models import GeoJSONDataSource
from bokeh.plotting import figure, output_file, save
from bokeh.embed import file_html
from bokeh.resources import CDN

def get_test_geojson(table, gid, features=None):

    sql = """
        SELECT row_to_json(f) As feature
        FROM (SELECT 'Feature' As type
        , ST_AsGeoJSON(geom)::json As geometry
        , row_to_json((SELECT l FROM (SELECT {1} AS feat_id) As l)) As properties
        FROM {0} As l where l.gid = {2}) As f;
        """.format(table, features, gid)

    return sql

def json2file(geojson, file):

    with open(file, "w") as text_file:
        # print(json, file=text_file)

        #### Test code #####
        # pprint.pprint(json.dumps(geojson))
        # print(type(geojson))
        # exit(0)

        # print(type(geojson))
        output_file("/home/guido/.egopowerflow/visualization/visualize_grid2.html", title="line plot example")
        geojson = json.dumps(geojson)
        geo = GeoJSONDataSource(geojson=geojson)
        import pprint
        # pprint.p
        print(geo['id'])


        p = figure()
        p.patches(alpha=0.9, source=geo)

        save(p)

        # html = file_html(p, CDN,
        #                  "/home/guido/.egopowerflow/visualization/geojson.html")
        # print(html)
        # with open("/home/guido/.egopowerflow/visualization/geojson.html",
        #           "wb") as html_h:
        #     write(html_h)

        #### Test code ####

        json.dump(geojson, text_file)

if __name__ == '__main__':

    conn = io.oedb_session(section='oedb')

    table = 'orig_vg250.vg250_2_lan'
    gid = 5
    features = 'gen'
    sql = get_test_geojson(table, gid, features=features)

    geojson = conn.execute(sql).fetchall()[0][0]
    geojson['geometry']['coordinates'] = geojson['geometry']['coordinates'][0][
        0]

    feature_collection = {"type": "FeatureCollection"   ,
                          "features": [geojson]}

    json2file(feature_collection,
              '/home/guido/.egopowerflow/visualization/test_data.json')


    # Use ColumnDataSource with the help of DataFrame
    # df = pd.read_sql_table('vg250_2_lan', conn, 'orig_vg250')
    # for idx, row in df.iterrows():
    #     wkt_geom = to_shape(row['geom'])
    #
    #     row.loc[idx, 'x'] = wkt_geom.x
    #     row.loc[idx, 'y'] = wkt_geom.y
    # print(df)
