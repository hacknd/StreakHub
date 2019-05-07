from rest_framework import exceptions

class GamEngineException400(exceptions.APIException):
	status_code = 400
	default_detail = 'This is a No No'
	default_code = 'service_unavailable'

class GamEngineException404(exceptions.APIException):
	status_code = 404
	default_detail="We couldn't find your request"
	default_code="Error in Viewing"

class GamEngineException500(exceptions.APIException):
	status_code = 500
	default_detail="Error in system functionality"
	default_code="Error in System"	

