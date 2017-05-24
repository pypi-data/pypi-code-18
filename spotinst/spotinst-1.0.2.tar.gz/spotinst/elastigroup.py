import json
# region Elastigroup
class Elastigroup:
    def __init__(self, name, description, capacity, strategy, compute, scaling=None,
                 scheduling=None, multai=None,
                 thirdPartiesIntegration=None):
        self.name = name
        self.description = description
        self.capacity = capacity
        self.strategy = strategy
        self.scaling = scaling
        self.scheduling = scheduling
        self.multai = multai
        self.thirdPartiesIntegration = thirdPartiesIntegration
        self.compute = compute


# endregion

# region Strategy
class Strategy:
    def __init__(self, availabilityVsCost, risk=None, utilizeReservedInstances=None, fallbackToOd=None,
                 onDemandCount=None, drainingTimeout=None,
                 spinUpTime=None, lifetimePeriod=None, signals=None):
        self.risk = risk
        self.utilizeReservedInstances = utilizeReservedInstances
        self.fallbackToOd = fallbackToOd
        self.onDemandCount = onDemandCount
        self.availabilityVsCost = availabilityVsCost
        self.drainingTimeout = drainingTimeout
        self.spinUpTime = spinUpTime
        self.lifetimePeriod = lifetimePeriod
        self.spinUpTime = spinUpTime
        self.signals = signals


class Signal:
    def __init__(self, name, timeout=None):
        self.name = name
        self.timeout = timeout


class Persistence:
    def __init__(self, shouldPersistBlockDevices=None, shouldPersistRootDevice=None, shouldPersistPrivateIp=None):
        self.shouldPersistBlockDevices = shouldPersistBlockDevices
        self.shouldPersistRootDevice = shouldPersistRootDevice
        self.shouldPersistPrivateIp = shouldPersistPrivateIp


# endregion

# region Capacity
class Capacity:
    def __init__(self, minimum, maximum, target, unit=None):
        self.minimum = minimum
        self.maximum = maximum
        self.target = target
        self.unit = unit


# endregion

# region Scaling
class Scaling:
    def __init__(self, up=None, down=None):
        self.up = up
        self.down = down


class ScalingPolicyDimension:
    def __init__(self, name, value):
        self.name = name
        self.value = value


class ScalingPolicyAction:
    def __init__(self, type, adjustment=None, minTargetCapacity=None, maxTargetCapacity=None, target=None,
                 minimum=None,
                 maximum=None):
        self.type = type
        self.adjustment = adjustment
        self.minTargetCapacity = minTargetCapacity
        self.maxTargetCapacity = maxTargetCapacity
        self.target = target
        self.minimum = minimum
        self.maximum = maximum


class ScalingPolicy:
    def __init__(self, namespace, metricName, statistic, evaluationPeriods, period, threshold,
                 cooldown, action, unit, dimensions=None, policyName=None):
        self.policyName = policyName
        self.namespace = namespace
        self.metricName = metricName
        self.dimensions = dimensions
        self.statistic = statistic
        self.evaluationPeriods = evaluationPeriods
        self.period = period
        self.threshold = threshold
        self.cooldown = cooldown
        self.action = action
        self.unit = unit


# endregion

# region Scheduling
class Scheduling:
    def __init__(self, tasks):
        self.tasks = tasks


class ScheduledTask:
    def __init__(self, taskType, scaleTargetCapacity=None,
                 scaleMinCapacity=None,
                 scaleMaxCapacity=None, batchSizePercentage=None, gracePeriod=None, adjustment=None,
                 adjustmentPercentage=None, isEnabled=None,
                 frequency=None, cronExpression=None, ):
        self.isEnabled = isEnabled
        self.frequency = frequency
        self.cronExpression = cronExpression
        self.taskType = taskType
        self.scaleTargetCapacity = scaleTargetCapacity
        self.scaleMinCapacity = scaleMinCapacity
        self.scaleMaxCapacity = scaleMaxCapacity
        self.batchSizePercentage = batchSizePercentage
        self.gracePeriod = gracePeriod
        self.adjustment = adjustment
        self.adjustmentPercentage = adjustmentPercentage


# endregion

# region Multai
class Multai:
    def __init__(self, token, balancers):
        self.token = token
        self.balancers = balancers


class MultaiLoadBalancer:
    def __init__(self, projectId, balancerId, targetSetId, azAwareness=None, autoWeight=None):
        self.projectId = projectId
        self.balancerId = balancerId
        self.targetSetId = targetSetId
        self.azAwareness = azAwareness
        self.autoWeight = autoWeight


# endregion

# region ThirdPartyIntegrations
class RancherConfiguration:
    def __init__(self, accessKey, secretKey, masterHost):
        self.accessKey = accessKey
        self.secretKey = secretKey
        self.masterHost = masterHost


class MesosphereConfiguration:
    def __init__(self, apiServer):
        self.apiServer = apiServer


class ElasticBeanstalkConfiguration:
    def __init__(self, environmentId, deploymentPreferences):
        self.environmentId = environmentId
        self.deploymentPreferences = deploymentPreferences


class ElasticBeanstalkConfigurationDeploymentPreferences:
    def __init__(self, automaticRoll, batchSizePercentage=None, gracePeriod=None, strategy=None):
        self.automaticRoll = automaticRoll
        self.batchSizePercentage = batchSizePercentage
        self.gracePeriod = gracePeriod
        self.strategy = strategy


class ElasticBeanstalkConfigurationDeploymentPreferencesStrategy:
    def __init__(self, action, shouldDrainInstances=None):
        self.action = action
        self.shouldDrainInstances = shouldDrainInstances


class EcsConfiguration:
    def __init__(self, clusterName):
        self.clusterName = clusterName


class KubernetesConfiguration:
    def __init__(self, apiServer, token):
        self.apiServer = apiServer
        self.token = token


class RightScaleConfiguration:
    def __init__(self, accountId, refreshToken):
        self.accountId = accountId
        self.refreshToken = refreshToken


class OpsWorksConfiguration:
    def __init__(self, accessKey, secretKey, masterHost):
        self.accessKey = accessKey
        self.secretKey = secretKey
        self.masterHost = masterHost


class ChefConfiguration:
    def __init__(self, chefServer, organization, user, pemKey, chefVersion):
        self.chefServer = chefServer
        self.organization = organization
        self.user = user
        self.pemKey = pemKey
        self.chefVersion = chefVersion


class ThirdPartyIntegrations:
    def __init__(self, rancher=None, mesosphere=None, elasticBeanstalk=None, ecs=None, kubernetes=None, rightScale=None,
                 opsWorks=None, chef=None):
        self.rancher = rancher
        self.mesosphere = mesosphere
        self.elasticBeanstalk = elasticBeanstalk
        self.ecs = ecs
        self.kubernetes = kubernetes
        self.rightScale = rightScale
        self.opsWorks = opsWorks
        self.chef = chef


# endregion

# region Compute
class Compute:
    def __init__(self, launchSpecification, instanceTypes, product, availabilityZonesList, elasticIps=None,
                 ebsVolumesList=None):
        self.elasticIps = elasticIps
        self.instanceTypes = instanceTypes
        self.availabilityZones = availabilityZonesList
        self.product = product
        self.ebsVolumePool = ebsVolumesList
        self.launchSpecification = launchSpecification


class AvailabilityZone:
    def __init__(self, name, subnetId=None, subnetIds=None, placementGroupName=None):
        self.name = name
        self.subnetId = subnetId
        self.subnetIds = subnetIds
        self.placementGroupName = placementGroupName


class InstanceTypes:
    def __init__(self, ondemand, spotTypesList, instanceTypeWeightsList=None):
        self.ondemand = ondemand
        self.spot = spotTypesList
        self.weights = instanceTypeWeightsList


class InstanceTypesWeights:
    def __init__(self, instanceType, weightedCapacity):
        self.instanceType = instanceType
        self.weightedCapacity = weightedCapacity


class EbsVolume:
    def __init__(self, deviceName, volumeIds):
        self.deviceName = deviceName
        self.volumeIds = volumeIds


class LaunchSpecification:
    def __init__(self, securityGroupIdsList, imageId, monitoring, healthCheckType=None, loadBalancersList=None,
                 healthCheckGracePeriod=None, healthCheckUnhealthyDurationBeforeReplacement=None,
                 ebsOptimized=None, tenancy=None, iamRole=None, keyPair=None, userData=None, shutdownScript=None,
                 blockDeviceMappingsList=None,
                 networkInterfacesList=None, tagsList=None):
        self.loadBalancersConfig = loadBalancersList
        self.healthCheckType = healthCheckType
        self.healthCheckGracePeriod = healthCheckGracePeriod
        self.healthCheckUnhealthyDurationBeforeReplacement = healthCheckUnhealthyDurationBeforeReplacement
        self.securityGroupIds = securityGroupIdsList
        self.monitoring = monitoring
        self.ebsOptimized = ebsOptimized
        self.imageId = imageId
        self.tenancy = tenancy
        self.iamRole = iamRole
        self.keyPair = keyPair
        self.userData = userData
        self.shutdownScript = shutdownScript
        self.blockDeviceMappings = blockDeviceMappingsList
        self.networkInterfaces = networkInterfacesList
        self.tags = tagsList


class LaunchSpecLBConfig:
    def __init__(self, loadBalancers):
        self.loadBalancers = loadBalancers


class LaunchSpecLBConfigLoadBalancer:
    def __init__(self, type, arn=None, name=None):
        self.name = name
        self.arn = arn
        self.type = type


class LaunchSpecIAmRole:
    def __init__(self, name, arn):
        self.name = name
        self.arn = arn


class LaunchSpecBlockDeviceMapping:
    def __init__(self, deviceName, ebs, noDevice=None, virtualName=None):
        self.deviceName = deviceName
        self.ebs = ebs
        self.noDevice = noDevice
        self.virtualName = virtualName


class LaunchSpecBlockDeviceMappingEBS:
    def __init__(self, deleteOnTermination=None, encrypted=None, iops=None, snapshotId=None, volumeSize=None,
                 volumeType=None):
        self.deleteOnTermination = deleteOnTermination
        self.encrypted = encrypted
        self.iops = iops
        self.snapshotId = snapshotId
        self.volumeSize = volumeSize
        self.volumeType = volumeType


class LaunchSpecTag:
    def __init__(self, tagKey, tagValue):
        self.tagKey = tagKey
        self.tagValue = tagValue


class LaunchSpecNetworkInterface:
    def __init__(self, deleteOnTermination, deviceIndex=None, description=None, secondaryPrivateIpAddressCount=None,
                 associatePublicIpAddress=None, groupsList=None, networkInterfaceId=None, privateIpAddress=None,
                 privateIpAddresses=None, subnetId=None,
                 associateIpv6Address=None):
        self.description = description
        self.deviceIndex = deviceIndex
        self.secondaryPrivateIpAddressCount = secondaryPrivateIpAddressCount
        self.associatePublicIpAddress = associatePublicIpAddress
        self.deleteOnTermination = deleteOnTermination
        self.groups = groupsList
        self.networkInterfaceId = networkInterfaceId
        self.privateIpAddress = privateIpAddress
        self.privateIpAddresses = privateIpAddresses
        self.subnetId = subnetId
        self.associateIpv6Address = associateIpv6Address


class LaunchSpecNetworkInterfacePrivateIpAddress:
    def __init__(self, privateIpAddress, primary):
        self.privateIpAddress = privateIpAddress
        self.primary = primary


# endregion

class ElastigroupCreationRequest:
    def __init__(self, elastigroup):
        self.group = elastigroup

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)