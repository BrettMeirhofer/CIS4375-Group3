from django.http import HttpResponse


def index(request):
    out = """Hello, world. You're at the jeans index. Brett Meirhofer"""
    return HttpResponse(out)
