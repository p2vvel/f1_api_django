from rest_framework.throttling import AnonRateThrottle, UserRateThrottle



class AnonBurstThrottle(AnonRateThrottle):
    scope = "anon_burst"

class AnonSustainedThrottle(AnonRateThrottle):
    scope = "anon_sustained"

class UserBurstThrottle(UserRateThrottle):
    scope = "user_burst"

class UserSustainedThrottle(UserRateThrottle):
    scope = "user_sustained"



class ViewThrottle:
    """
    Class defining throttle rates for views, must be inherited by them (views)
    """
    throttle_classes = [
        AnonBurstThrottle, 
        AnonSustainedThrottle,
        UserBurstThrottle,
        UserSustainedThrottle]