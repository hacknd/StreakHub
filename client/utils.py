from rest_framework import exceptions




class GamEngineException400(exceptions.APIException):
	status_code = 400
	default_detail = 'This is a No No'
	default_code = 'service_unavailable'