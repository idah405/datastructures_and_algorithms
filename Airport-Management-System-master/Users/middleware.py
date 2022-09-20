from django.http import HttpResponseRedirect
from django.urls import reverse


class financemanagerRequiredMiddleware(object):
    """
    Middleware that checks that the logged in user is Finance,
    redirects to the log-in page if necessary.
    """
    FINANCEMANAGER_REQUIRED_URLS = ['financemanager/', "financemanager/change-password/", "financemanager/profile/", "financemanager/feedback/",
                             "financemanager/payments/", "financemanager/payments-pdf/"]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if path in self.FINANCEMANAGER_REQUIRED_URLS:
                return HttpResponseRedirect(reverse('financemanager:login'))
        elif request.user.is_authenticated and not request.user.is_financemanager:
            path = request.path_info.lstrip('/')
            if path in self.FINANCEMANAGER_REQUIRED_URLS:
                return HttpResponseRedirect(reverse('financemanager:login'))


class handymanRequiredMiddleware(object):
    """
    Middleware that checks that the logged in user is handyman,
    redirects to the log-in page if necessary.
    """
    HANDYMAN_REQUIRED_URLS = ['handyman/', "handyman/change-password/", "handyman/profile/", "handyman/feedback/",
                                  "handyman/Appointment/", "handyman/ClientService/", "handyman/electrician/", "handyman/ClientService-pdf/",
                                  "handyman/Appointment-pdf/"]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            print(f"{path}, user is not logged in")
            if path in self.HANDYMAN_REQUIRED_URLS:
                return HttpResponseRedirect(reverse('handyman:login'))
        elif request.user.is_authenticated and not request.user.is_handyman:
            path = request.path_info.lstrip('/')
            if path in self.HANDYMAN_REQUIRED_URLS:
                return HttpResponseRedirect(reverse('handyman:login'))


class managerRequiredMiddleware(object):
    """
    Middleware that checks that the logged in user is manager,
    redirects to the log-in page if necessary.
    """
    MANAGER_REQUIRED_URLS = ['manager/', "manager/change-password/", "manager/profile/", "manager/feedback/",
                             "manager/served/", "manager/served-pdf/"]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if path in self.MANAGER_REQUIRED_URLS:
                return HttpResponseRedirect(reverse('manager:login'))
        elif request.user.is_authenticated and not request.user.is_manager:
            path = request.path_info.lstrip('/')
            if path in self.MANAGER_REQUIRED_URLS:
                return HttpResponseRedirect(reverse('manager:login'))    

