from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get('jwt-auth')
        if raw_token is None:
            header = self.get_header(request)
            if header is None:
                return None
            raw_token = self.get_raw_token(header)
            if raw_token is None:
                return None
        try:
            validated_token = self.get_validated_token(raw_token)            
            return self.get_user(validated_token), validated_token
        except Exception as e:
            return None