from __future__ import print_function
from gevent.queue import Queue


class ErlProcess:
    """ Implements Erlang process semantic and lifetime
        Registers itself in the process registry, can receive and send messages
    """
    def __init__(self, node) -> None:
        """ Create a process and register itself. Pid is generated by the node
            :param node: 
        """
        self.messages = Queue()
        self.mailbox = ErlMailbox()
        self.pid = node.register_new_process(self)
