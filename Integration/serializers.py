from rest_framework import serializers


class GmailWatchSerializer(serializers.Serializer):
    """
    Class for serializing the request data.
    """
    watch_request = serializers.JSONField()
