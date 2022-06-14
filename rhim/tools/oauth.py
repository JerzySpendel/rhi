from rest_framework.exceptions import NotAuthenticated


def oauth_required(view):
    def wrapped(self, request):
        if not request.session.has_key("user"):
            raise NotAuthenticated

        return view(self, request)

    return wrapped
