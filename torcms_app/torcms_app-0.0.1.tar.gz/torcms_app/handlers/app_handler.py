# -*- coding:utf-8 -*-

'''
App计算的扩展处理
'''
import os

from torcms.handlers.post_handler import PostHandler
from torcms_app.model.ext_model import MCalcInfo


class YuansuanHandler(PostHandler):
    '''
    App计算的扩展处理
    '''

    def initialize(self, **kwargs):
        super(YuansuanHandler, self).initialize()
        self.mcalcinfo = MCalcInfo()
        if 'kind' in kwargs:
            self.kind = kwargs['kind']
        else:
            self.kind = 's'

    def ext_tmpl_view(self, rec):
        html_path = rec.extinfo['html_path']
        if os.path.exists('templates/jshtml/{0}.html'.format(html_path)):
            pass
        else:
            '''
            如果正常找不到，则在模板文件夹下面进行搜索。
            这个比较费时间
            '''
            html_path = ''
            getit = False
            for wroot, wdirs, wfiles in os.walk('./templates/jshtml'):
                for wfile in wfiles:
                    if wfile == '{0}.html'.format(rec.uid):
                        html_path = os.path.join(wroot, wfile[:-5])[len('./templates/jshtml'):]
                        getit = True
                        break
                if getit:
                    break

        if html_path == '':
            return False

        post_data = self.get_post_data()
        runid = ''

        if 'runid' in post_data:
            runid = post_data['runid']

        return 'jshtml/{0}.html'.format(html_path)

    def ext_view_kwd(self, info_rec):
        '''
        The additional information.
        :param info_rec:
        :return: directory.
        '''

        app_hist_recs = None
        if self.userinfo:
            app_hist_recs = self.mcalcinfo.query_hist_recs(self.userinfo.uid, info_rec.uid)

        kwd = {}
        post_data = self.get_post_data()
        # runid: 保存过的运行的数据
        runid = ''
        if 'runid' in post_data:
            runid = post_data['runid']
        kwd['runid'] = runid
        kwd['app_hist_recs'] = app_hist_recs
        return kwd
