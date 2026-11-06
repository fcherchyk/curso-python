from django.db import models
from django.urls import include, path
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView


class Task(models.Model):
    title = models.CharField(max_length=100)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "tasks"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "done", "created"]
        read_only_fields = ["id", "created"]

    def validate_title(self, value: str) -> str:
        value = value.strip()
        if value.lower() == "todo":
            raise serializers.ValidationError("Use a descriptive title")
        return value


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.order_by("id")
    serializer_class = TaskSerializer

    def get_queryset(self):  # type: ignore[no-untyped-def]
        qs = super().get_queryset()
        done = self.request.query_params.get("done")
        if done is not None:
            qs = qs.filter(done=done == "true")
        return qs

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):  # type: ignore[no-untyped-def]
        task = self.get_object()
        task.done = True
        task.save(update_fields=["done"])
        return Response(self.get_serializer(task).data)


class Stats(APIView):
    def get(self, request):  # type: ignore[no-untyped-def]
        total = Task.objects.count()
        done = Task.objects.filter(done=True).count()
        return Response({"total": total, "done": done, "pending": total - done})


router = DefaultRouter()
router.register("tasks", TaskViewSet)

urlpatterns = [
    path("api/stats/", Stats.as_view()),
    path("api/", include(router.urls)),
]
