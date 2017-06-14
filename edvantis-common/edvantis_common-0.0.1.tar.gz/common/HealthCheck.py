from flask_restful import Resource


class HealthCheck(Resource):
    """
    This is a required health check
    that k8s uses to automatically
    restart pods
    """
    def get(self):
        return {u"success": u"alive"}
