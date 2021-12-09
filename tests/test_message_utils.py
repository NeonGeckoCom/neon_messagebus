# # NEON AI (TM) SOFTWARE, Software Development Kit & Application Development System
# # All trademark and other rights reserved by their respective owners
# # Copyright 2008-2021 Neongecko.com Inc.
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

import os
import sys
import unittest
from time import time
from threading import Event

from mycroft_bus_client import MessageBusClient, Message

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from neon_messagebus.service import NeonBusService


class TestMessageUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.service = NeonBusService(debug=True, daemonic=True)
        cls.service.start()
        cls.service.started.wait()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.service.shutdown()

    def test_get_messagebus(self):
        from neon_messagebus.util.message_utils import get_messagebus
        bus = get_messagebus()
        self.assertIsInstance(bus, MessageBusClient)
        self.assertTrue(bus.connected_event.is_set())
        self.assertTrue(bus.started_running)

        bus = get_messagebus(False)
        self.assertIsInstance(bus, MessageBusClient)
        self.assertFalse(bus.connected_event.is_set())
        self.assertFalse(bus.started_running)

    def test_send_message(self):
        from neon_messagebus.util.message_utils import get_messagebus, send_message
        received: Message = None
        received_event = Event()
        received_event.clear()

        def message_handler(message):
            nonlocal received
            received = message
            received_event.set()

        client_bus = get_messagebus()
        client_bus.on("unit_test_message", message_handler)

        test_msg = Message("unit_test_message", {"time": time()}, {"test": "send Message Object"})
        send_message(test_msg)
        received_event.wait()
        self.assertEqual(test_msg.serialize(), received.serialize())
        received_event.clear()
        received = None

        send_message(test_msg.serialize())
        received_event.wait()
        self.assertEqual(test_msg.serialize(), received.serialize())
        received_event.clear()
        received = None

        send_message(test_msg.msg_type, test_msg.data, test_msg.context)
        received_event.wait()
        self.assertEqual(test_msg.serialize(), received.serialize())
        received_event.clear()

# TODO: Test binary file methods DM


if __name__ == '__main__':
    unittest.main()
