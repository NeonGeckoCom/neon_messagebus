# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2022 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import json
import sys
import traceback

import ovos_messagebus.event_handler
from ovos_messagebus.event_handler import MessageBusEventHandler
from ovos_bus_client.message import Message
from ovos_utils import LOG


class NeonMessageBusEventHandler(MessageBusEventHandler):
    def __init__(self, *args, **kwargs):
        MessageBusEventHandler.__init__(self, *args, **kwargs)
        self._sessions = dict()

    def emit(self, channel_message):
        if isinstance(channel_message, Message):
            channel_message = channel_message.serialize()
        session = channel_message.context.pop('session', {})
        session_id = session.get('session_id')
        if session_id:
            channel_message.context['context']['session'] = {'session_id': session_id}
            self._sessions[session_id] = session
            # LOG.debug(f"Added {session_id} to known sessions")
        MessageBusEventHandler.emit(self, channel_message)

    def on_message(self, message: str):
        message = json.loads(message)
        if sess := message.get('context', {}).get('session',
                                                  {}).get('session_id'):
            # LOG.debug(f"Getting {sess} from known sessions")
            message['context']['session'] = self._sessions.get(sess,
                                                               message['context']['session'])
        MessageBusEventHandler.on_message(self, json.dumps(message))
