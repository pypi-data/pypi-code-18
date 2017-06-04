import json

none = "d3043820717d74d9a17694c176d39733"


# region Elastigroup
class Elastigroup:
    def __init__(self, name=none, description=none, capacity=none, strategy=none,
                 compute=none, scaling=none,
                 scheduling=none, multai=none,
                 third_parties_integration=none):
        self.name = name
        self.description = description
        self.capacity = capacity
        self.strategy = strategy
        self.scaling = scaling
        self.scheduling = scheduling
        self.multai = multai
        self.thirdPartiesIntegration = third_parties_integration
        self.compute = compute


# endregion

# region Strategy
class Strategy:
    def __init__(self, availability_vs_cost=none, risk=none, utilize_reserved_instances=none,
                 fallback_to_od=none,
                 on_demand_count=none, draining_timeout=none,
                 spin_up_time=none, lifetime_period=none, signals=none,
                 scaling_strategy=none, persistence=none):
        self.risk = risk
        self.utilizeReservedInstances = utilize_reserved_instances
        self.fallbackToOd = fallback_to_od
        self.onDemandCount = on_demand_count
        self.availabilityVsCost = availability_vs_cost
        self.drainingTimeout = draining_timeout
        self.spinUpTime = spin_up_time
        self.lifetimePeriod = lifetime_period
        self.spinUpTime = spin_up_time
        self.signals = signals
        self.scalingStrategy = scaling_strategy
        self.persistence = persistence


class Signal:
    def __init__(self, name=none, timeout=none):
        self.name = name
        self.timeout = timeout


class ScalingStrategy:
    def __init__(self, terminate_at_end_of_billing_hour):
        self.terminateAtEndOfBillingHour = terminate_at_end_of_billing_hour


class Persistence:
    def __init__(self, should_persist_block_devices=none, should_persist_root_device=none,
                 should_persist_private_ip=none):
        self.shouldPersistBlockDevices = should_persist_block_devices
        self.shouldPersistRootDevice = should_persist_root_device
        self.shouldPersistPrivateIp = should_persist_private_ip


# endregion

# region Capacity
class Capacity:
    def __init__(self, minimum=none, maximum=none, target=none, unit=none):
        self.minimum = minimum
        self.maximum = maximum
        self.target = target
        self.unit = unit


# endregion

# region Scaling
class Scaling:
    def __init__(self, up=none, down=none):
        self.up = up
        self.down = down


class ScalingPolicyDimension:
    def __init__(self, name=none, value=none):
        self.name = name
        self.value = value


class ScalingPolicyAction:
    def __init__(self, type=none, adjustment=none, min_target_capacity=none,
                 max_target_capacity=none, target=none,
                 minimum=none,
                 maximum=none):
        self.type = type
        self.adjustment = adjustment
        self.minTargetCapacity = min_target_capacity
        self.maxTargetCapacity = max_target_capacity
        self.target = target
        self.minimum = minimum
        self.maximum = maximum


class ScalingPolicy:
    def __init__(self, namespace=none, metric_name=none, statistic=none,
                 evaluation_periods=none, period=none,
                 threshold=none,
                 cooldown=none, action=none, unit=none, operator=none,
                 dimensions=none, policy_name=none):
        self.policyName = policy_name
        self.namespace = namespace
        self.metricName = metric_name
        self.dimensions = dimensions
        self.statistic = statistic
        self.evaluationPeriods = evaluation_periods
        self.period = period
        self.threshold = threshold
        self.cooldown = cooldown
        self.action = action
        self.unit = unit
        self.operator = operator


# endregion

# region Scheduling
class Scheduling:
    def __init__(self, tasks=none):
        self.tasks = tasks


class ScheduledTask:
    def __init__(self, task_type=none, scale_target_capacity=none,
                 scale_min_capacity=none,
                 scale_max_capacity=none, batch_size_percentage=none, grace_period=none,
                 adjustment=none,
                 adjustment_percentage=none, is_enabled=none,
                 frequency=none, cron_expression=none, ):
        self.isEnabled = is_enabled
        self.frequency = frequency
        self.cronExpression = cron_expression
        self.taskType = task_type
        self.scaleTargetCapacity = scale_target_capacity
        self.scaleMinCapacity = scale_min_capacity
        self.scaleMaxCapacity = scale_max_capacity
        self.batchSizePercentage = batch_size_percentage
        self.gracePeriod = grace_period
        self.adjustment = adjustment
        self.adjustmentPercentage = adjustment_percentage


# endregion

# region Multai
class Multai:
    def __init__(self, token=none, balancers=none):
        self.token = token
        self.balancers = balancers


class MultaiLoadBalancer:
    def __init__(self, project_id=none, balancer_id=none, target_set_id=none, az_awareness=none,
                 auto_weight=none):
        self.projectId = project_id
        self.balancerId = balancer_id
        self.targetSetId = target_set_id
        self.azAwareness = az_awareness
        self.autoWeight = auto_weight


# endregion

# region ThirdPartyIntegrations
class Rancher:
    def __init__(self, access_key=none, secret_key=none, master_host=none):
        self.accessKey = access_key
        self.secretKey = secret_key
        self.masterHost = master_host


class Mesosphere:
    def __init__(self, api_server=none):
        self.apiServer = api_server


class ElasticBeanstalk:
    def __init__(self, environment_id=none, deployment_preferences=none):
        self.environmentId = environment_id
        self.deploymentPreferences = deployment_preferences


class DeploymentPreferences:
    def __init__(self, automatic_roll=none, batch_size_percentage=none, grace_period=none,
                 strategy=none):
        self.automaticRoll = automatic_roll
        self.batchSizePercentage = batch_size_percentage
        self.gracePeriod = grace_period
        self.strategy = strategy


class BeanstalkDeploymentStrategy:
    def __init__(self, action=none, should_drain_instances=none):
        self.action = action
        self.shouldDrainInstances = should_drain_instances


class EcsConfiguration:
    def __init__(self, cluster_name=none):
        self.clusterName = cluster_name


class KubernetesConfiguration:
    def __init__(self, api_server=none, token=none):
        self.apiServer = api_server
        self.token = token


class RightScaleConfiguration:
    def __init__(self, account_id=none, refresh_token=none):
        self.accountId = account_id
        self.refreshToken = refresh_token


class OpsWorksConfiguration:
    def __init__(self, layer_id=none):
        self.layerId = layer_id


class ChefConfiguration:
    def __init__(self, chef_server=none, organization=none, user=none, pem_key=none,
                 chef_version=none):
        self.chefServer = chef_server
        self.organization = organization
        self.user = user
        self.pemKey = pem_key
        self.chefVersion = chef_version


class ThirdPartyIntegrations:
    def __init__(self, rancher=none, mesosphere=none, elastic_beanstalk=none, ecs=none,
                 kubernetes=none, right_scale=none,
                 ops_works=none, chef=none):
        self.rancher = rancher
        self.mesosphere = mesosphere
        self.elasticBeanstalk = elastic_beanstalk
        self.ecs = ecs
        self.kubernetes = kubernetes
        self.rightScale = right_scale
        self.opsWorks = ops_works
        self.chef = chef


# endregion

# region Compute
class Compute:
    def __init__(self, launch_specification=none, instance_types=none, product=none,
                 availability_zones_list=none,
                 elastic_ips_string_list=none,
                 ebs_volumes_list=none):
        self.elasticIps = elastic_ips_string_list
        self.instanceTypes = instance_types
        self.availabilityZones = availability_zones_list
        self.product = product
        self.ebsVolumePool = ebs_volumes_list
        self.launchSpecification = launch_specification


class AvailabilityZone:
    def __init__(self, name=none, subnet_id=none, subnet_ids=none, placement_group_name=none):
        self.name = name
        self.subnetId = subnet_id
        self.subnetIds = subnet_ids
        self.placementGroupName = placement_group_name


class InstanceTypes:
    def __init__(self, ondemand=none, spot_types_list=none, instance_type_weights_list=none):
        self.ondemand = ondemand
        self.spot = spot_types_list
        self.weights = instance_type_weights_list


class Weight:
    def __init__(self, instance_type=none, weighted_capacity=none):
        self.instanceType = instance_type
        self.weightedCapacity = weighted_capacity


class EbsVolume:
    def __init__(self, device_name=none, volume_ids=none):
        self.deviceName = device_name
        self.volumeIds = volume_ids


class LaunchSpecification:
    def __init__(self, security_group_ids_list=none, image_id=none, monitoring=none,
                 health_check_type=none,
                 load_balancers_config=none,
                 health_check_grace_period=none, health_check_unhealthy_duration_before_replacement=none,
                 ebs_optimized=none, tenancy=none, i_am_role=none, key_pair=none,
                 user_data=none, shutdown_script=none,
                 block_device_mappings_list=none,
                 network_interfaces_list=none, tags_list=none):
        self.loadBalancersConfig = load_balancers_config
        self.healthCheckType = health_check_type
        self.healthCheckGracePeriod = health_check_grace_period
        self.healthCheckUnhealthyDurationBeforeReplacement = health_check_unhealthy_duration_before_replacement
        self.securityGroupIds = security_group_ids_list
        self.monitoring = monitoring
        self.ebsOptimized = ebs_optimized
        self.imageId = image_id
        self.tenancy = tenancy
        self.iamRole = i_am_role
        self.keyPair = key_pair
        self.userData = user_data
        self.shutdownScript = shutdown_script
        self.blockDeviceMappings = block_device_mappings_list
        self.networkInterfaces = network_interfaces_list
        self.tags = tags_list


class LoadBalancersConfig:
    def __init__(self, load_balancers_list=none):
        self.loadBalancers = load_balancers_list


class LoadBalancer:
    def __init__(self, type=none, arn=none, name=none):
        self.name = name
        self.arn = arn
        self.type = type


class IAmRole:
    def __init__(self, name=none, arn=none):
        self.name = name
        self.arn = arn


class BlockDeviceMapping:
    def __init__(self, device_name=none, ebs=none, no_device=none, virtual_name=none):
        self.deviceName = device_name
        self.ebs = ebs
        self.noDevice = no_device
        self.virtualName = virtual_name


class EBS:
    def __init__(self, delete_on_termination=none, encrypted=none, iops=none, snapshot_id=none,
                 volume_size=none,
                 volume_type=none):
        self.deleteOnTermination = delete_on_termination
        self.encrypted = encrypted
        self.iops = iops
        self.snapshotId = snapshot_id
        self.volumeSize = volume_size
        self.volumeType = volume_type


class Tag:
    def __init__(self, tag_key=none, tag_value=none):
        self.tagKey = tag_key
        self.tagValue = tag_value


class NetworkInterface:
    def __init__(self, delete_on_termination=none, device_index=none, description=none,
                 secondary_private_ip_address_count=none,
                 associate_public_ip_address=none, groups_list=none, network_interface_id=none,
                 private_ip_address=none,
                 private_ip_addresses=none, subnet_id=none,
                 associate_ipv6_address=none):
        self.description = description
        self.deviceIndex = device_index
        self.secondaryPrivateIpAddressCount = secondary_private_ip_address_count
        self.associatePublicIpAddress = associate_public_ip_address
        self.deleteOnTermination = delete_on_termination
        self.groups = groups_list
        self.networkInterfaceId = network_interface_id
        self.privateIpAddress = private_ip_address
        self.privateIpAddresses = private_ip_addresses
        self.subnetId = subnet_id
        self.associateIpv6Address = associate_ipv6_address


class PrivateIpAddress:
    def __init__(self, private_ip_address=none, primary=none):
        self.privateIpAddress = private_ip_address
        self.primary = primary


# endregion

class ElastigroupCreationRequest:
    def __init__(self, elastigroup):
        self.group = elastigroup

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class ElastigroupUpdateRequest:
    def __init__(self, elastigroup):
        self.group = elastigroup

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
