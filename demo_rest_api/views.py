from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid


# Simulación de base de datos local en memoria
data_list = []

# Datos iniciales
data_list.append({
    'id': str(uuid.uuid4()),
    'name': 'User01',
    'email': 'user01@example.com',
    'is_active': True
})

data_list.append({
    'id': str(uuid.uuid4()),
    'name': 'User02',
    'email': 'user02@example.com',
    'is_active': True
})

data_list.append({
    'id': str(uuid.uuid4()),
    'name': 'User03',
    'email': 'user03@example.com',
    'is_active': False
})


class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
        active_items = [item for item in data_list if item.get("is_active", False)]
        return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy() if hasattr(request.data, "copy") else dict(request.data)

        if "name" not in data or "email" not in data:
            return Response(
                {
                    "error": "Los campos name y email son obligatorios"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        data["id"] = str(uuid.uuid4())
        data["is_active"] = True

        data_list.append(data)

        return Response(
            {
                "message": "Dato guardado exitosamente.",
                "data": data
            },
            status=status.HTTP_201_CREATED
        )
class DemoRestApiItem(APIView):

    def put(self, request, item_id):
        for item in data_list:
            if item["id"] == item_id:

                # Mantener el id original
                new_data = request.data

                if "id" not in new_data:
                    return Response(
                        {
                            "error": "El campo id es obligatorio"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                if new_data["id"] != item_id:
                    return Response(
                        {
                            "error": "El id no puede modificarse"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

                item.clear()
                item.update(new_data)

                return Response(
                    {
                        "message": "Elemento actualizado completamente",
                        "data": item
                    },
                    status=status.HTTP_200_OK
                )

        return Response(
            {
                "error": "Elemento no encontrado"
            },
            status=status.HTTP_404_NOT_FOUND
        )


    def patch(self, request, item_id):
        for item in data_list:
            if item["id"] == item_id:

                item.update(request.data)

                return Response(
                    {
                        "message": "Elemento actualizado parcialmente",
                        "data": item
                    },
                    status=status.HTTP_200_OK
                )

        return Response(
            {
                "error":"Elemento no encontrado"
            },
            status=status.HTTP_404_NOT_FOUND
        )


    def delete(self, request, item_id):

        for item in data_list:
            if item["id"] == item_id:

                item["is_active"] = False

                return Response(
                    {
                        "message": "Elemento eliminado lógicamente",
                        "data": item
                    },
                    status=status.HTTP_200_OK
                )

        return Response(
            {
                "error": "Elemento no encontrado"
            },
            status=status.HTTP_404_NOT_FOUND
        )
