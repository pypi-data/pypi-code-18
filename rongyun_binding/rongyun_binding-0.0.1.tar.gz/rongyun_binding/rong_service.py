# coding=utf8
from singleton import singleton
from rongcloud import RongCloud
from sqlalchemy import Column, Integer, String, UniqueConstraint

Binding = object
session = None


def bind_models(Base, db_session):
    class DeviceBinding(Base):
        account_type = Column(Integer)
        account_id = Column(Integer)
        device_token = Column(String(100))
        rong_id = Column(String(64))
        rong_token = Column(String(100))
        __tablename__ = 'device_binding'
        __table_args__ = (
            UniqueConstraint('account_type', 'account_id', 'device_token',
                             name="acc_type_acc_id_dt_idx_unique"),
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
            need_update = True

        if force_update:
            need_update = True
            
        if need_update:
            response = self.rcloud.User.getToken(userId=devicebinding.rong_id, name=user_name,
                                                portraitUri=avatar)
            result = response.get()
            assert result['code'] == 200, u"获取融云token失败"
            devicebinding.rong_token = result['token']
            session.flush()
        return devicebinding.rong_id, devicebinding.rong_token

        
            

        
        
            



            


