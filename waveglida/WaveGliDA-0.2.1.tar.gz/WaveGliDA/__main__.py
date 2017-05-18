#!/usr/bin/env python
# -*- coding: utf-8 -*-


def main():

    from WaveGliDA import app
    import webbrowser

    url = "localhost:{}".format(app.config['PORT'])
    webbrowser.open(url)

    app.run(port=app.config['PORT'])


if __name__ == '__main__':
    main()
