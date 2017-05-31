# coding=utf8
import time
from singleton import singleton
from rongcloud import RongCloud
from sqlalchemy import Column, Integer, String, UniqueConstraint, Index

Binding = object
session = None


def bind_models(Base, db_session):
    class DeviceBinding(Base):
        account_type = Column(Integer)
        account_id = Column(Integer)
        device_token = Column(String(100))
        rong_id = Column(String(64))
        rong_token = Column(String(100))
        last_update = Column(Integer)
        __tablename__ = 'device_binding'
        __table_args__ = (
            UniqueConstraint('account_type', 'account_id', 'device_token',
                             name="acc_type_acc_id_dt_idx_unique"),
            Index('device_binding_query_idx', 'account_type', 'account_id', 'last_update')
        )
    global Binding, session
    Binding = DeviceBinding
    session = db_session


@singleton.Singleton
class RongService(object):
    def __init__(self, api_key, api_sec):
        self.rcloud = RongCloud(api_key, api_sec)
        

    def update_token(self, account_type, account_id, device_token, user_name='', avatar='', force_update=False):
        """
        更新token
        :param account_type: 
        :type account_type: 
        :param account_id: 
        :type account_id: 
        :param device_token: 
        :type device_token: 
        :return: 
        :rtype: 
        """
        need_update = False

        # 先获取最新的绑定记录
        devicebinding = session.query(Binding).filter(Binding.account_type == account_type,
                                                      Binding.account_id == account_id,
                                                      ).order_by(Binding.last_update.desc()).first()
        if devicebinding:
            if devicebinding.device_token == device_token:
                # 如果就是这个设备就直接返回
                if force_update:
                    self.fetch_token_from_rongyun(avatar, devicebinding, user_name)
                return devicebinding.rong_id, devicebinding.rong_token

        devicebinding = session.query(Binding).filter(Binding.account_type == account_type,
                                             Binding.account_id == account_id,
                                             Binding.device_token == device_token).first()
        if not devicebinding:
            devicebinding = Binding(
                account_type=account_type,
                account_id=account_id,
                device_token=device_token,
                rong_id="ry-%s-%s" % (account_type, account_id)
            )
            session.add(devicebinding)
            session.flush()

        self.fetch_token_from_rongyun(avatar, devicebinding, user_name)
        return devicebinding.rong_id, devicebinding.rong_token


    def fetch_token_from_rongyun (self, avatar, devicebinding, user_name):
        response = self.rcloud.User.getToken(userId=devicebinding.rong_id, name=user_name,
                                             portraitUri=avatar)
        result = response.get()
        assert result ['code'] == 200, u"获取融云token失败"
        devicebinding.rong_token = result ['token']
        devicebinding.last_update = int(time.time())
        session.flush()

        
            

        
        
            



            


