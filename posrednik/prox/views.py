from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .actions import Storage, Server

"""ну.. что то более менее похожее на что то более менее"""
s1 = Server(Storage())


def index(request):
    return HttpResponse("Hello. Available URL's: http://127.0.0.1:8000/send_request/, "
                        "http://127.0.0.1:8000/requests/, http://127.0.0.1:8000/delete_data/")


class AddressView(APIView):
    def get(self, request):

        message = s1.get_all_users()
        if any(message):  # проверка на отсутсвие адресов
            return JsonResponse(message)
        else:
            return JsonResponse({"response": "Companion has not yet sent a connection request"})


@api_view(['POST'])
def add_request(request):
    param = str(request.data["ip"]) + ":" + str(request.data["port"])
    s1.add_user(request.data["name"], param)
    return JsonResponse({"response": "Request added"})


@api_view(['DELETE'])
def delete_data(request):
    name = request.data["name"]
    s1.delete_user(name)
    return JsonResponse({"response": "Request deleted"})
