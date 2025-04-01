from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from .models import Event
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from .serializers import EventSerializer


class LoginView(APIView):  # True si la contraseña es correcta
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        return Response({"error": "Credenciales inválidas"}, status=400)
    
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]  # Solo los usuarios autenticados pueden acceder

    # 🔹 Personalizar el queryset para que un usuario solo vea sus eventos
    def get_queryset(self):
        return Event.objects.filter(created_by=self.request.user)

    # 🔹 Obtener todos los eventos del usuario autenticado
    @action(detail=False, methods=['get'])
    def my_events(self, request):
        user_events = Event.objects.filter(created_by=request.user)
        serializer = self.get_serializer(user_events, many=True)
        return Response(serializer.data)

    # 🔹 Obtener un evento específico por ID
    @action(detail=True, methods=['get'])
    def get_event_by_id(self, request, pk=None):
        try:
            event = Event.objects.get(id=pk, created_by=request.user)
            serializer = self.get_serializer(event)
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response({"error": "Evento no encontrado"}, status=404)

    # 🔹 Crear un nuevo evento
    def create(self, request, *args, **kwargs):
        # Agregar el usuario que crea el evento
        request.data['created_by'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user, modified_by=request.user)
            return Response(serializer.data, status=201)  # Evento creado
        return Response(serializer.errors, status=400)

    # 🔹 Modificar un evento existente
    def update(self, request, *args, **kwargs):
        evento = self.get_object()  # Obtiene el evento por el ID
        if evento.created_by != request.user:
            return Response({"error": "No tienes permiso para modificar este evento"}, status=403)

        serializer = self.get_serializer(evento, data=request.data, partial=True)  # Modificación parcial
        if serializer.is_valid():
            serializer.save(modified_by=request.user)
            return Response(serializer.data)  # Evento actualizado
        return Response(serializer.errors, status=400)

    # 🔹 Eliminar un evento
    def destroy(self, request, *args, **kwargs):
        evento = self.get_object()  # Obtiene el evento por el ID
        if evento.created_by != request.user:
            return Response({"error": "No tienes permiso para eliminar este evento"}, status=403)

        evento.delete()  # Elimina el evento
        return Response({"message": "Evento eliminado con éxito"}, status=204)

class EventAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        evento_id = request.data.get("id", None)

        if evento_id:
            try:
                evento = Event.objects.get(id=evento_id)
                serializer = EventSerializer(evento, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save(modified_by=request.user)
                    return Response(serializer.data, status=status.HTTP_200_OK)  # Código 200 para actualización
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Event.DoesNotExist:
                return Response({"error": "Evento no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = EventSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(created_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)  # Código 201 para creación
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

usuario = User.objects.get(username="ignaciog")
class GetEvents(APIView):
    # Event.objects.all().delete()
    def get(self, request):
        events = Event.objects.filter(created_by=usuario).order_by('start')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
class GetEventById(APIView):
    def get(self, request, id):
        try:
            evento = Event.objects.get(id=id)
            serializer = EventSerializer(evento)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({"error": "Evento no encontrado"}, status=status.HTTP_404_NOT_FOUND)


class DeleteEvent(APIView):
    def get(self, request, id):
        try:
            evento = Event.objects.get(id=id)
            serializer = EventSerializer(evento)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Event.DoesNotExist:
            return Response({"error": "Evento no encontrado"}, status=status.HTTP_404_NOT_FOUND)