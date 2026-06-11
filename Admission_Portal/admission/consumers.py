import json

from channels.generic.websocket import AsyncWebsocketConsumer


class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close()
            return

        # We group by authenticated user id so students receive only their updates.
        self.group_name = f"student_{user.id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def status_update(self, event):
        # event: { type: 'status_update', application_number, status, remarks, decided_at }
        await self.send(text_data=json.dumps(event))

    async def status(self, event):
        # compatibility if group_send uses type=status
        await self.status_update(event)


