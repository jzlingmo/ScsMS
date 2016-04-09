# -*- coding: utf-8 -*-
__author__ = 'jz'

from scs_app import app, config

if __name__ == '__main__':
    app.debug = config.DEBUG
    app.run(port=1000)
