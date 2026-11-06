from django.db import models
from django.urls import include, path
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView


class Tarea(models.Model):
    titulo = models.CharField(max_length=100)
    hecha = models.BooleanField(default=False)
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "tareas"


class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ["id", "titulo", "hecha", "creada"]
        read_only_fields = ["id", "creada"]

    def validate_titulo(self, valor: str) -> str:
        valor = valor.strip()
        if valor.lower() == "todo":
            raise serializers.ValidationError("Poné un título descriptivo")
        return valor


class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.order_by("id")
    serializer_class = TareaSerializer

    def get_queryset(self):  # type: ignore[no-untyped-def]
        qs = super().get_queryset()
        hecha = self.request.query_params.get("hecha")
        if hecha is not None:
            qs = qs.filter(hecha=hecha == "true")
        return qs

    @action(detail=True, methods=["post"])
    def completar(self, request, pk=None):  # type: ignore[no-untyped-def]
        tarea = self.get_object()
        tarea.hecha = True
        tarea.save(update_fields=["hecha"])
        return Response(self.get_serializer(tarea).data)


class Estadisticas(APIView):
    def get(self, request):  # type: ignore[no-untyped-def]
        total = Tarea.objects.count()
        hechas = Tarea.objects.filter(hecha=True).count()
        return Response({"total": total, "hechas": hechas, "pendientes": total - hechas})


router = DefaultRouter()
router.register("tareas", TareaViewSet)

urlpatterns = [
    path("api/estadisticas/", Estadisticas.as_view()),
    path("api/", include(router.urls)),
]
