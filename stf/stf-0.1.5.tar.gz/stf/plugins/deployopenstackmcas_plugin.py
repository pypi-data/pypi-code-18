#!/usr/bin/env python
import os,sys,shutil,time,subprocess,traceback
#from multiprocessing import Process,Lock,Queue
from novaclient import client as novaclient
from keystoneauth1 import loading
from keystoneauth1 import session
from neutronclient.v2_0 import client as neutronclient
from heatclient import client as heatclient
from stf.plugins.deploy_plugin import STFDeployPlugin
from stf.lib.logging.logger import Logger
logger = Logger.getLogger(__name__)
#openstack_res=Lock()
  
class STFDeployopenstackmcasPlugin(STFDeployPlugin):
    def __init__(self, plugins):
        super(STFDeployopenstackmcasPlugin, self).__init__(plugins)
          
    #derived class should override this API
    def preCheck(self):
        self.openstack={}
        try:
            self.openstack= {'authurl' : "http://"+self.variablePlugin.get('OpenStackIP','TestEnv')+":5000/v2.0", 
                    'username' : self.variablePlugin.get('OpenStackUser','TestEnv'),  
                    'password' : self.variablePlugin.get('OpenStackPass','TestEnv'),  
                    'projectname' : self.variablePlugin.get('OpenStackUser','TestEnv'), 
                    'tenantname': self.variablePlugin.get('OpenStackUser','TestEnv')}
            #print openstack
        except Exception,errmsg:
            logger.info( 'Cannot get configuration')
            logger.info( errmsg)
            return False
        self.adminopenstack={}
        self.adminopenstack.update(self.openstack)
        self.adminopenstack['username']='admin'
        self.adminopenstack['password']='admin'
        self.adminopenstack['projectname']='admin'
        self.adminopenstack['tenantname']='admin'
        self.nova = None
        self.neutron=None
        self.heat=None
        self.network=None
        self.subnet=None
        self.extnet=None
        self.secgroup=None
        try:
            loader=loading.get_plugin_loader('password')
            auth=loader.load_from_options(username=self.openstack['username'],
                                          password=self.openstack['password'],
                                          project_name=self.openstack['projectname'],
                                          auth_url=self.openstack['authurl'])
            sess=session.Session(auth=auth)
            self.nova = novaclient.Client(2,session=sess)
            self.neutron = neutronclient.Client(session=sess)
            self.heat=heatclient.Client(1,session=sess,service_type='orchestration',endpoint_type='publicURL')
        except Exception,errmsg:
            self.error=errmsg
            logger.info( errmsg)
            return False
        try:
            self.extnet = [x for x in self.neutron.list_networks()['networks'] if x['router:external']][0]
        except Exception,errmsg:
            self.error=errmsg
            logger.info( 'Cannot find external network')
            logger.info( errmsg)
            return False
        try:
            self.network=self.neutron.list_networks(name=self.openstack['username']+'_internal_net')['networks'][0]
            self.subnet=self.neutron.list_subnets(name=self.openstack['username']+'_internal_subnet')['subnets'][0]
        except Exception:
            logger.info( self.openstack['username'] + ' has no network defined. create new one')
            try:
                self.network=self.neutron.create_network({'network':{'name': self.openstack['username']+'_internal_net', 
                                                                     'admin_state_up': True,'shared':True}
                                                          })['network']
                logger.info( self.openstack['username']+'_internal_net is created : '+self.network['id'])
                self.subnet = self.neutron.create_subnet(body={'subnets': [{'name': self.openstack['username']+'_internal_subnet',
                                                                            'cidr': '192.168.99.0/24',
                                                                            'ip_version': 4, 
                                                                            'network_id': self.network['id']}]
                                                               })['subnets'][0]
                logger.info( self.openstack['username']+'_internal_net is created : '+self.subnet['id'])
                adminneutron=neutronclient.Client(username=self.adminopenstack['username'],
                                                  password=self.adminopenstack['password'],
                                                  tenant_name=self.adminopenstack['projectname'],
                                                  auth_url=self.adminopenstack['authurl'])
                router=adminneutron.list_routers(name='admin_router')['routers'][0]
                adminneutron.add_interface_router(router=router['id'],body={ 'subnet_id': self.subnet['id'] })
            except Exception,errmsg:
                self.error=errmsg
                logger.info( 'Cannot create network for '+self.openstack['username'])
                logger.info( errmsg)
                return False
        try:
            self.secgroup = self.nova.security_groups.find(name="default")
            try:
                self.nova.security_group_rules.create(self.secgroup.id, ip_protocol="tcp", from_port=1, to_port=65535)
            except Exception:
                pass
            try:
                self.nova.security_group_rules.create(self.secgroup.id, ip_protocol="udp", from_port=-1, to_port=-1)
            except Exception:
                pass
            try:
                self.nova.security_group_rules.create(self.secgroup.id, ip_protocol="icmp", from_port=-1, to_port=-1)
            except Exception:
                pass
        except Exception:
            pass
        return True
  
    #derived class should override this API
    def preAction(self):
        pass
      
    #derived class should override this API
    def deploy(self,idx,labpar):
        exist=False
        floatingip=None
        for x in labpar['VM']:
            #rvmdeployer.prepare()
            needfloat=(x['FloatingIP'] in ['true', '1', 't', 'y', 'yes', 'True','Yes','Y','T'])
            for i in range(0,int(x['count'])):
                logger.info( 'setup '+labpar['Name']+'_'+str(idx)+'_'+x['Name']+'_'+str(i))
                resmesg=self.setupVM(labpar['Name'],idx,i,x,needfloat,True)
                #logger.info( vmdeployer.setup(name+'_'+x['Name']+'_'+str(i),flavor=x['flavor'],image=x['image'],
                #floating=(x['floatingip'] in ['true', '1', 't', 'y', 'yes', 'True','Yes','Y','T']));
                logger.info(resmesg)
                if resmesg and resmesg['Result']:
                    if resmesg['Exist']:
                        exist=True
                    else:
                        if resmesg['VMIP'] is not None and resmesg['VMIP'] != "":
                            floatingip=resmesg['VMIP']
                else:
                    return False
        
        if exist:
            self.error=resmesg['ResultMsg']
            return True
        '''if floatingip == None:
            logger.info("Quit spa installation")
            return False
        if labpar['SPA'] is not None and labpar['SPA'] != "" :
            shutil.copy(os.path.dirname(os.path.abspath(__file__))+'/resources/mcas.py', 
                        os.getcwd()+'/install/'+self.openstack['username'])
            for spa in labpar['SPA'].split(","):
                logger.info('Downloading '+spa)
                proc=subprocess.Popen([os.path.dirname(os.path.abspath(__file__))+'/resources/copy.sftp',
                                       self.variablePlugin.get('user','Build:USER'),
                                       self.variablePlugin.get('pass','Build:USER'),
                                       self.variablePlugin.get('buildServer','Build:USER'),
                                       'download',
                                       self.variablePlugin.get('path','Build:USER')+"/"+spa+'.full.tar',
                                       os.getcwd()+'/install/'+self.openstack['username']], 
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                #'/n/spaS5001/lx64/'+spa+'/SU1R50/TAR/DEFAULT/full/'+spa+'.full.tar',
                for proc_line in iter(proc.stdout.readline,''):
                    logger.debug(proc_line)
                proc.wait()
                if proc.returncode!=0:
                    logger.info('Download spa '+spa+' failed')
                    return False
                else:
                    logger.info('Download spa '+spa+' succeeded')
                proc=subprocess.Popen([os.path.dirname(os.path.abspath(__file__))+'/CI_deploy/installspa',
                                       floatingip,spa+'.full.tar',
                                       os.getcwd()+'/install/'+self.openstack['username']], 
                                      stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                for proc_line in iter(proc.stdout.readline,''):
                    logger.debug(proc_line)
                proc.wait()
                if proc.returncode!=0:
                    logger.info('install spa '+spa+' failed')
                    return False
                else:
                    logger.info('install spa '+spa+' succeeded')'''
        return True

    
    #derived class should override this API
    def destroy(self,idx,labpar):
        for x in labpar['VM']:
            #vmdeployer.prepare()
            for i in reversed(range(0,int(x['count']))):
                logger.info( 'Destroying '+labpar['Name']+'_'+str(idx)+'_'+x['Name']+'_'+str(i))
                resmesg=self.destroyVM(labpar['Name'],idx,i,x)
                logger.info(resmesg)
                if resmesg and resmesg['Result']:
                    pass
                else:
                    self.error=resmesg['ResultMsg']
                    return False
        return True



    #derived class should override this API
    def get(self,idx,labpar):
        for x in labpar['VM']:
            for i in range(0,int(x['count'])):
                logger.info( 'get info of '+labpar['Name']+'_'+str(idx)+'_'+x['Name']+'_'+str(i))
                resmesg=self.getVM(labpar['Name'],idx,i,x)
                if resmesg and resmesg['Result']:
                    self.putLabIP(labpar['Name'], idx, x['Name'], i, resmesg['VMFloatingIP'], resmesg['VMIP'], resmesg['VMInternalIP'])
                else:
                    self.error=resmesg['ResultMsg']
                    return False
        return True



    #derived class should override this API
    def postAction(self):
        pass
  
    
    def destroyVM(self,labname,labindx,vmindx,vmpar):
        fip=None
        resmesg={'Result':True,
                 'Exist':False,
                 'ResultMsg':'',
                 'LabName': labname,
                 'LabIndex':labindx,
                 'VMName':vmpar['Name'],
                 'VMIndex':vmindx,
                 'VMIP':'',
                 'VMFloatingIP':'','VMInternalIP':''}
        if vmpar['CustomScript'] == 'heatinstall1':
            try:
                stack=self.heat.stacks.get(labname+str(labindx))
                if stack is not None:
                    server=self.nova.servers.find(name=labname+str(labindx)+'-0-0-1')
                    ports=self.neutron.list_ports(device_id=server.id)['ports']
                    for k in ports:
                        if k['fixed_ips'][0]['subnet_id'] == self.subnet['id']:
                            port=k
                            resmesg['VMIP']=port['fixed_ips'][0]['ip_address']
                        else:
                            resmesg['VMInternalIP']=k['fixed_ips'][0]['ip_address']
                    try:
                        fip=self.neutron.list_floatingips(fixed_ip_address=port['fixed_ips'][0]['ip_address'])['floatingips'][0]
                        resmesg['VMFloatingIP']=fip['floating_ip_address']
                        logger.info("Will release floating ip "+fip['floating_ip_address'])
                    except Exception,errmsg:
                        pass
                    stack.delete()
                    logger.info( 'destroy stack '+labname+str(labindx))
                    stack=self.heat.stacks.get(labname+str(labindx))
                    try:
                        while stack.status == 'IN_PROGRESS':
                            time.sleep(5)
                            stack=self.heat.stacks.get(labname+str(labindx))
                            logger.info('in progress')
                    except Exception:
                        pass
                    logger.info( labname+str(labindx)+' is destroyed')
                else:
                    logger.info(labname+str(labindx)+' is removed')
            except Exception,errmsg:
                logger.info(errmsg)
                logger.info(labname+str(labindx)+' not exist')
            #return True
        else:
            name=labname+'_'+str(labindx)+'_'+vmpar['Name']+'_'+str(vmindx)
            try:
                server=self.nova.servers.find(name=name)
                ports=self.neutron.list_ports(device_id=server.id)['ports']
                for k in ports:
                    if k['fixed_ips'][0]['subnet_id'] == self.subnet['id']:
                        port=k
                        resmesg['VMIP']=port['fixed_ips'][0]['ip_address']
                    else:
                        resmesg['VMInternalIP']=k['fixed_ips'][0]['ip_address']
                try:
                    fip=self.neutron.list_floatingips(fixed_ip_address=port['fixed_ips'][0]['ip_address'])['floatingips'][0]
                    resmesg['VMFloatingIP']=fip['floating_ip_address']
                except Exception,errmsg:
                    pass
            except Exception,errmsg:
                logger.info( 'Instance '+name +' not found')
                logger.info( errmsg)
                #return True #already detroy or input error?
            else:
                logger.info( 'Found '+name)
                logger.info( 'Its status is '+server.status)
                #if server.status == 'ACTIVE':
                logger.info( 'Bring down '+name)
                try:
                    server.delete()
                except Exception,errmsg:
                    logger.info( name+' bring down failure ')
                    logger.info( errmsg)
                    resmesg['Result']=False
                    resmesg['ResultMsg']=errmsg
        if fip is not None:
            self.neutron.delete_floatingip(fip['id'])
            logger.info(fip['floating_ip_address']+" released.")
        #self.queue.put(resmesg)
        return resmesg


    def getVM(self,labname,labindx,vmindx,vmpar):
        server=None
        resmesg={'Result':True,
                 'Exist':False,
                 'ResultMsg':'',
                 'LabName': labname,
                 'LabIndex':labindx,
                 'VMName':vmpar['Name'],
                 'VMIndex':vmindx,
                 'VMIP':'',
                 'VMFloatingIP':'',
                 'VMInternalIP':''}
        if vmpar['CustomScript'] == 'heatinstall1':
            name=labname+str(labindx)
            try:
                stack=self.heat.stacks.get(name)
                if stack is not None:
                    logger.info(name +' found ')
                try:
                    server=self.nova.servers.find(name=name+'-0-0-1')
                    ports=self.neutron.list_ports(device_id=server.id)['ports']
                    for k in ports:
                        if k['fixed_ips'][0]['subnet_id'] == self.subnet['id']:
                            port=k
                            resmesg['VMIP']=port['fixed_ips'][0]['ip_address']
                        else:
                            resmesg['VMInternalIP']=k['fixed_ips'][0]['ip_address']
                    try:
                        fip=self.neutron.list_floatingips(fixed_ip_address=port['fixed_ips'][0]['ip_address'])['floatingips'][0]
                        resmesg['VMFloatingIP']=fip['floating_ip_address']
                    except Exception,errmsg:
                        pass
                    resmesg['Exist']=True
                    #self.queue.put(resmesg)
                    return resmesg
                except Exception,errmsg:
                    logger.info('Cannot find ip for lab '+name+'.')
                    resmesg['Result']=False
                    resmesg['ResultMsg']=errmsg
                    #self.queue.put(resmesg)
                    return resmesg
            except Exception:
                logger.info(name+' is not found')
                resmesg['Result']=False
                resmesg['ResultMsg']='not found'
                #self.queue.put(resmesg)
                return resmesg
        else:
            name=labname+'_'+str(labindx)+'_'+vmpar['Name']+'_'+str(vmindx)
            try:
                server=self.nova.servers.find(name=name)
            except Exception,errmsg:
                logger.info(name+' is not found')
                resmesg['Result']=False
                resmesg['ResultMsg']='not found'
                #self.queue.put(resmesg)
                return resmesg
            else:
                logger.info( name+' is found')
                logger.info( 'Its status is '+server.status)
                #TODO return floating ip
                try:
                    ports=self.neutron.list_ports(device_id=server.id)['ports']
                    port=None
                    for k in ports:
                        if k['fixed_ips'][0]['subnet_id'] == self.subnet['id']:
                            port=k
                            resmesg['VMIP']=port['fixed_ips'][0]['ip_address']
                        else:
                            resmesg['VMInternalIP']=k['fixed_ips'][0]['ip_address']
                    if port is None:
                        raise Exception("Cannot find the local port for floating ip")
                    fip=self.neutron.list_floatingips(fixed_ip_address=port['fixed_ips'][0]['ip_address'])['floatingips'][0]
                    #resmesg['VMIP']=port['fixed_ips'][0]['ip_address']
                    resmesg['VMFloatingIP']=fip['floating_ip_address']
                    resmesg['Exist']=True
                    #self.queue.put(resmesg)
                    return resmesg
                except Exception,errmsg:
                    logger.info('Cannot find ip for lab '+name+'.')
                    resmesg['Result']=False
                    resmesg['ResultMsg']=errmsg
                    #self.queue.put(resmesg)
                    return resmesg


    def setupVM(self,labname,labindx,vmindx,vmpar,floating=False,updatecfg=False):
        server=None
        resmesg={'Result':True,
                 'Exist':False,
                 'ResultMsg':'',
                 'LabName': labname,
                 'LabIndex':labindx,
                 'VMName':vmpar['Name'],
                 'VMIndex':vmindx,
                 'VMIP':'',
                 'VMFloatingIP':'',
                 'VMInternalIP':''}
        if vmpar['CustomScript'] == 'heatinstall1':
            name=labname+str(labindx)
            try:
                stack=self.heat.stacks.get(name)
                if stack is not None:
                    logger.info(name +' is already exists ')
                try:
                    server=self.nova.servers.find(name=name+'-0-0-1')
                    ports=self.neutron.list_ports(device_id=server.id)['ports']
                    for k in ports:
                        if k['fixed_ips'][0]['subnet_id'] == self.subnet['id']:
                            port=k
                            resmesg['VMIP']=port['fixed_ips'][0]['ip_address']
                        else:
                            resmesg['VMInternalIP']=k['fixed_ips'][0]['ip_address']
                    try:
                        fip=self.neutron.list_floatingips(fixed_ip_address=port['fixed_ips'][0]['ip_address'])['floatingips'][0]
                        resmesg['VMFloatingIP']=fip['floating_ip_address']
                    except Exception,errmsg:
                        pass
                    resmesg['Exist']=True
                    #self.queue.put(resmesg)
                    return resmesg
                except Exception,errmsg:
                    logger.info('Cannot find lab '+name+'.')
                    resmesg['Result']=False
                    resmesg['ResultMsg']=errmsg
                    #self.queue.put(resmesg)
                    return resmesg
            except Exception:
                pass
            siteinfo={}
            siteinfo['SI_SYSTEM_PREFIX']=name
            siteinfo['SI_EXTERNAL_IP_A']='AUTO'
            siteinfo['SI_EXTERNAL_FLOATING_IP']='AUTO'
            siteinfo['SI_EXTERNAL_GATEWAY_IP']='osnet:'+self.network['id']
            siteinfo['SI_EXTERNAL_INTERFACE']='osnet:'+self.network['id']
            siteinfo['SI_TIMEZONE']='CST6CDT'
            siteinfo['SI_CLOUD_PROVIDER']='openstack-direct'
            siteinfo['SI_CLOUD_AUTH_URL']=self.openstack['authurl']
            siteinfo['SI_CLOUD_ALLOW_INSECURE']='yes'
            siteinfo['SI_CLOUD_TENANT']=self.openstack['tenantname']
            siteinfo['SI_CLOUD_USERNAME']=self.openstack['username']
            siteinfo['SI_CLOUD_PASSWORD']=self.openstack['password']
            siteinfo['SI_OVERRIDE_DHCP_DNS']='no'
            siteinfo['SI_DOMAIN_NAME']='openstacklocal'
            siteinfo['SI_PILOT_A_RCS']='0-0-1'
            siteinfo['SI_PILOT_A_MODEL']='vm'
            siteinfo['SI_PILOT_A_INTERNAL_INTERFACES']='tap0'
            siteinfo['SI_PILOT_A_SOL']='noredirect'
            siteinfo['SI_PILOT_A_OPTIONS']='RTDB,BILL,SUBMEAS,VXPROC,DGR'
            siteinfo['SI_PILOT_A_VMID']='AUTO'
            siteinfo['SI_PILOT_A_CLOUD_FLAVOR']=vmpar['Flavor']
            siteinfo['SI_PILOT_A_CLOUD_IMAGE']=vmpar['Image']
            siteinfo['SI_PILOT_A_CLOUD_SECURITY_GROUP']=self.secgroup.id
            siteinfo['SI_PILOT_A_CLOUD_AVAIL_ZONE']='nova'
            siteinfo['SI_PILOT_A_CLOUD_ADDL_VOLUME']='80'
            siteinfo['SI_PILOT_A_CLOUD_ADDL_VOLUME_AVAIL_ZONE']='nova'
            siteinfo['SI_MAS_CONFIG']='YES'
            siteinfo['SI_MAS_VLSN_HOST_1']='0-0-1'
            siteinfo['SI_CLOUD_HEAT_COMPAT_VERSION']='liberty'
            for k in vmpar['Siteinfo']:
                if vmpar['Siteinfo'][k] == '${SECURITY_GROUP}':
                    vmpar['Siteinfo'][k]=self.secgroup.id
            siteinfo.update(vmpar['Siteinfo'])
            if not os.path.exists(os.getcwd()+'/install/'+self.openstack['username']):
                os.makedirs(os.getcwd()+'/install/'+self.openstack['username'])
            shutil.copy(os.path.dirname(os.path.abspath(__file__))+'/resources/audit_siteinfo', os.getcwd()+'/install/'+self.openstack['username'])
            #print os.getcwd()+'/install/'+self.openstack['username']+'/siteinfo'
            with open(os.path.dirname(os.path.abspath(__file__))+'/resources/siteinfo') as file, open(os.getcwd()+'/install/'+self.openstack['username']+'/siteinfo','w') as outfile:
                for line in file:
                    if not line.startswith('#') and len(line.strip())!=0:
                        linekey=line.split('=')[0];
                        if siteinfo.has_key(linekey):
                            continue#line=linekey+'='+siteinfo[linekey]+'\n'
                    outfile.write(line)
            with open(os.getcwd()+'/install/'+self.openstack['username']+'/siteinfo','a') as outfile:
                for k,v in siteinfo.items():
                    outfile.write(k+'='+v+'\n')
            location=self.variablePlugin.get('serverType','Build:USER')
            for pkg in vmpar['Package'].split(","):
                if location=='Local':
                    proc=subprocess.Popen([os.path.dirname(os.path.abspath(__file__))+'/resources/copy.sftp',
                                           self.variablePlugin.get('user','Build:USER'),
                                           self.variablePlugin.get('pass','Build:USER'),
                                           self.variablePlugin.get('buildServer','Build:USER'),
                                           'download',
                                           self.variablePlugin.get('path','Build:USER')+"/"+pkg,
                                           os.getcwd()+'/install/'+self.openstack['username']], 
                                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                elif location=='NEXUS':
                    proc=subprocess.Popen([os.path.dirname(os.path.abspath(__file__))+'/resources/copy.nexus',
                                           self.variablePlugin.get('buildServer','Build:USER'),
                                           self.variablePlugin.get('path','Build:USER')+"/"+pkg,
                                           os.getcwd()+'/install/'+self.openstack['username']], 
                                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                for proc_line in iter(proc.stdout.readline,''):
                    logger.info(proc_line)
                '''for proc_line in iter(proc.stderr.readline,''):
                    logger.info(proc_line)'''
                proc.wait()
                if proc.returncode!=0:
                    logger.info('Download packages failed '+str(proc.returncode))
                    resmesg['Result']=False
                    resmesg['ResultMsg']='Download packages failed.'
                    #self.queue.put(resmesg)
                    return resmesg
            os.environ['PRODUCTS_DIR']=os.getcwd()+'/install/'+self.openstack['username']
            os.environ['LC_ALL']='C'
            os.environ['OS_NO_CACHE']='true'
            os.environ['OS_TENANT_NAME']=self.openstack['tenantname']
            os.environ['OS_PROJECT_NAME']=self.openstack['projectname']
            os.environ['OS_USERNAME']=self.openstack['username']
            os.environ['OS_PASSWORD']=self.openstack['password']
            os.environ['OS_AUTH_URL']=self.openstack['authurl']
            os.environ['OS_DEFAULT_DOMAIN']='default'
            os.environ['OS_AUTH_STRATEGY']='keystone'
            os.environ['OS_REGION_NAME']='RegionOne'
            os.environ['PATH']=os.environ['PATH']+':/usr/sbin'
            proc=subprocess.Popen(vmpar['CustomScript'],env=dict(os.environ),stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for proc_line in iter(proc.stdout.readline,''):
                logger.info(proc_line)
            '''for proc_line in iter(proc.stderr.readline,''):
                logger.info(proc_line)'''
            proc.wait()
            if proc.returncode!=0:
                logger.info('Deploy lab '+name+' failed:'+str(proc.returncode))
                resmesg['Result']=False
                resmesg['ResultMsg']='Deploy lab '+name+' failed.'
                #self.queue.put(resmesg)
                return resmesg
            try:
                server=self.nova.servers.find(name=name+'-0-0-1')
                name=name+"-0-0-1"
            except Exception,errmsg:
                logger.info('Cannot find lab '+name+'.')
                resmesg['Result']=False
                resmesg['ResultMsg']='Cannot find lab '+name+' after installation.'
                #self.queue.put(resmesg)
                return resmesg
        else:
            imagei=None
            falvori=None
            fipi=None
            name=labname+'_'+str(labindx)+'_'+vmpar['Name']+'_'+str(vmindx)
            try:
                server=self.nova.servers.find(name=name)
            except Exception,errmsg:
                pass
            else:
                logger.info( name+' is already launched')
                logger.info( 'Its status is '+server.status)
                #TODO return floating ip
                try:
                    ports=self.neutron.list_ports(device_id=server.id)['ports']
                    port=None
                    for k in ports:
                        if k['fixed_ips'][0]['subnet_id'] == self.subnet['id']:
                            port=k
                            resmesg['VMIP']=port['fixed_ips'][0]['ip_address']
                        else:
                            resmesg['VMInternalIP']=k['fixed_ips'][0]['ip_address']
                    if port is None:
                        raise Exception("Cannot find the local port for floating ip")
                    fip=self.neutron.list_floatingips(fixed_ip_address=port['fixed_ips'][0]['ip_address'])['floatingips'][0]
                    #resmesg['VMIP']=port['fixed_ips'][0]['ip_address']
                    resmesg['VMFloatingIP']=fip['floating_ip_address']
                    resmesg['Exist']=True
                    #self.queue.put(resmesg)
                    return resmesg
                except Exception,errmsg:
                    logger.info('Cannot find lab '+name+'.')
                    resmesg['Result']=False
                    resmesg['ResultMsg']=errmsg
                    #self.queue.put(resmesg)
                    return resmesg
            try:
                imagei=self.nova.images.find(name=vmpar['Image'])
            except Exception,errmsg:
                logger.info( 'Image '+vmpar['image']+' not found')
                logger.info( errmsg)
                resmesg['Result']=False
                resmesg['ResultMsg']=errmsg
                #self.queue.put(resmesg)
                return resmesg #should download image
            try:
                flavori=self.nova.flavors.find(name=vmpar['Flavor'])
            except Exception,errmsg:
                logger.info( 'Flavor '+vmpar['Flavor']+' not found')
                resmesg['Result']=False
                resmesg['ResultMsg']=errmsg
                #self.queue.put(resmesg)
                return resmesg#should create falvor
            '''try:
                neti=self.neutron.list_networks(name=netname)['networks'][0]['id']
            except Exception,errmsg:
                logger.info( 'Network '+netname+' not found'
                return None#should create falvor'''
            try:
                server=self.nova.servers.create(name=name,image=imagei,flavor=flavori,nics=[{'net-id':self.network['id']}])
                logger.info( 'Bring up '+name)
                while server.status == 'BUILD':
                    time.sleep(5)
                    server=self.nova.servers.get(server.id)
                logger.info( name+' is ready')
                
            except Exception,errmsg:
                logger.info( 'Creat instance '+name+' failed')
                logger.info( errmsg)
                resmesg['Result']=False
                resmesg['ResultMsg']=errmsg
                #self.queue.put(resmesg)
                return resmesg
        if server is not None:
            #retres={name:''}
            if floating :
                #openstack_res.acquire()
                try:
                    '''try:
                        fipi = [x for x in self.neutron.list_floatingips()['floatingips'] if not x['fixed_ip_address']][0]
                    except Exception:
                        try:
                            fipi = self.neutron.create_floatingip(body={'floatingip': {'floating_network_id':self.extnet['id']}})['floatingip']
                        except Exception,errmsg:
                            logger.info( 'Fail to create floating ip')
                            logger.info( errmsg)
                            resmesg['Result']=False
                            resmesg['ResultMsg']=errmsg
                    if fipi is not None:
                        try:'''
                            # Get the port corresponding to the instance
                    ports = self.neutron.list_ports(device_id=server.id)['ports']
                    port=None
                    for k in ports:
                        if k['fixed_ips'][0]['subnet_id'] == self.subnet['id']:
                            port=k
                            resmesg['VMIP']=port['fixed_ips'][0]['ip_address']
                        else:
                            resmesg['VMInternalIP']=k['fixed_ips'][0]['ip_address']
                    if port is None:
                        raise Exception("Cannot find the local port for floating ip")
                    fipi = self.neutron.create_floatingip(body={'floatingip': {'floating_network_id':self.extnet['id']}})['floatingip']
                    self.neutron.update_floatingip(fipi['id'],{'floatingip': {'port_id':port['id']}})
                    #server.add_floating_ip(fipi,fixed_address=server.networks[netname][0])
                    logger.info( 'Bind to '+fipi['floating_ip_address'])
                    '''retres[name]=fipi['floating_ip_address']
                    if updatecfg :
                        #cf.updateDynamic('Deploy',labname+'_'+str(labindx), fipi['floating_ip_address'])
                        queue.put({'Name':labname+'_'+str(labindx),'IPAddress': fipi['floating_ip_address']})
                        global retcount
                        retcount=retcount+1'''
                    #resmesg['VMIP']=port['fixed_ips'][0]['ip_address']
                    resmesg['VMFloatingIP']=fipi['floating_ip_address']
                    '''    except Exception,errmsg:
                            logger.info( 'Cannot bind to floating ip')
                            logger.info( errmsg)
                            resmesg['Result']=False
                            resmesg['ResultMsg']=errmsg
                    else:
                        logger.info( "Cannot get floating ip")
                        resmesg['Result']=False
                        resmesg['ResultMsg']="Cannot get floating ip"'''
                except Exception,errmsg:
                    traceback.print_exc(file=sys.stdout)
                    logger.info( "Cannot get floating ip")
                    logger.info(errmsg)
                    resmesg['Result']=False
                    resmesg['ResultMsg']="Cannot get floating ip"
                finally:
                    pass
                    #openstack_res.release()
            #self.queue.put(resmesg)
            return resmesg
        else:
            resmesg['Result']=False
            resmesg['ResultMsg']='Lab VM is not created at the end without any error.'
            #self.queue.put(resmesg)
            return resmesg