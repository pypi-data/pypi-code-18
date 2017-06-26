# -*- coding: utf-8 -*-


class LTPFileError(FileNotFoundError):
    def __init__(self):
        super(LTPFileError, self).__init__("LTP model not exist."
                                           " Please download models (v3.3.1) in following url: "
                                           "http://pan.baidu.com/share/link?shareid=1988562907&uk=2738088569")


