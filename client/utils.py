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

def GamEngineRedirectAuthorizationBackend(backend, code):
		"""
		Authorization information for the backends to the redirect feature
		"""
		if code == None:
			try:
				backend_class=get_backend(AUTHENTICATION_BACKENDS, backend)
				authorization_url=backend_class.AUTHORIZATION_URL
				url_parameters={
					'redirect_uri':('http://{}{}').format(Site.objects.get_current().domain, reverse('account-social-login', args=(backend,))),
					'response_type':backend_class.RESPONSE_TYPE,
					'scope':[scope for scope in backend_class.DEFAULT_SCOPE if scope != 'openid'][0],
					'client_id':config('SOCIAL_AUTH_'+backend.upper().replace('-','_')+'_KEY')
				}
				final_url=authorization_url+'?'+__import__('urllib').parse.urlencode(url_parameters)
				print(final_url)
			except:
				raise GamEngineException(code=status.HTTP_501_NOT_IMPLEMENTED,detail=__('Missing Backend'))
			
			return redirect(final_url)
		
		data = {
			"code":code,
			"redirect_uri":('http://{}{}').format(Site.objects.get_current().domain, reverse('account-social-login', args=(backend,))),
			"provider":backend
		}
		return	data
