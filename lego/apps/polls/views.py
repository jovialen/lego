from rest_framework import decorators, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from lego.apps.achievements.promotion import check_poll_related_single_user
from lego.apps.permissions.api.views import AllowedPermissionsMixin
from lego.apps.permissions.constants import EDIT
from lego.apps.polls.models import Poll
from lego.apps.polls.serializers import (
    DetailedPollSerializer,
    HiddenResultsDetailedPollSerializer,
    PollCreateSerializer,
    PollSerializer,
    PollUpdateSerializer,
)


class PollViewSet(AllowedPermissionsMixin, viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    ordering = "-created_at"

    def get_serializer_class(self):
        if self.action == "create":
            return PollCreateSerializer
        if self.action in ["update", "partial_update"]:
            return PollUpdateSerializer
        if self.action in ["retrieve", "vote"]:
            # self.get_object() throws error when accessing /api-docs because
            # no poll is provided when using "vote"-action.
            # Therefore return the safe serializer.
            try:
                poll = self.get_object()
            except AssertionError:
                return HiddenResultsDetailedPollSerializer
            if poll.results_hidden and not self.request.user.has_perm(EDIT, poll):
                return HiddenResultsDetailedPollSerializer
            return DetailedPollSerializer
        return PollSerializer

    @decorators.action(
        detail=True, methods=["POST"], permission_classes=[IsAuthenticated]
    )
    def vote(self, request, *args, **kwargs):
        poll = self.get_object()
        poll.vote(request.user, request.data["option_id"])
        serializer = self.get_serializer_class()(poll, context={"request": request})
        check_poll_related_single_user(request.user)
        return Response(serializer.data)
