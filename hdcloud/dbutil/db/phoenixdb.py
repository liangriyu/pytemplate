# Copyright 2015 Lukas Lalinsky
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import math
import time

import logging

import _socket
import phoenixdb
from phoenixdb import errors, types
from phoenixdb.connection import Connection
from _socket import *

try:
    import httplib
except ImportError:
    import http.client as httplib

logger = logging.getLogger(__name__)

__all__ = ['connect', 'apilevel', 'threadsafety', 'paramstyle'] + types.__all__ + errors.__all__


apilevel = "2.0"
"""
This module supports the `DB API 2.0 interface <https://www.python.org/dev/peps/pep-0249/>`_.
"""

threadsafety = 1
"""
Multiple threads can share the module, but neither connections nor cursors.
"""

paramstyle = 'qmark'
"""
Parmetrized queries should use the question mark as a parameter placeholder.

For example::

 cursor.execute("SELECT * FROM table WHERE id = ?", [my_id])
"""

DictCursor=phoenixdb.cursor.DictCursor

def connect(url, max_retries=None,time_out=None, **kwargs):
    """
    Set a timeout on socket operations.  'timeout' can be a float,
        giving in seconds, or None.  Setting a timeout of None disables
        the timeout feature and is equivalent to setblocking(1).
        Setting a timeout of zero is the same as setblocking(0).
    """
    client = AvaticaClient(url, max_retries=max_retries,time_out=time_out)
    client.connect()
    return Connection(client, **kwargs)

class AvaticaClient(phoenixdb.AvaticaClient):

    def __init__(self, url, max_retries=None, time_out=None):
        self.time_out=time_out
        super(AvaticaClient, self).__init__(url,max_retries)

    def connect(self):
        """Opens a HTTP connection to the RPC server."""
        logger.debug("Opening connection to %s:%s", self.url.hostname, self.url.port)
        try:
            self.connection = httplib.HTTPConnection(self.url.hostname, self.url.port,timeout=self.time_out)
            self.connection.connect()
        except (httplib.HTTPException, _socket.error) as e:
            raise errors.InterfaceError('Unable to connect to the specified service', e)