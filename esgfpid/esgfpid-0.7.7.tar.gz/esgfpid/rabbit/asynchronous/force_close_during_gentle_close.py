'''
Test case that tests...

We provide one perfectly fine RabbitMQ node.

We connect, send 500 messages, and gently close.
During this gentle-close, we force close after one
second.

Between these things, we leave enough time for
the tasks to finish without overlap.
'''
from helpers_for_testing import *


def run(logfile, name):
    print_testcase(name)

    # Code to be tested:
    connector = init_connector([node_ok])
    wait(10)
    send_messages(500, connector)
    gentle_close(connector)
    wait(1)
    force_close(connector)

    # Define expected contents of logfile:
    lines = []
    # (1) When we send, the connection is already complete. No sending before that:
    lines.append('Ready to publish messages to RabbitMQ. No messages waiting yet.')
    # (2) All messages were acked:
    lines.append(['Received ack for delivery tag 100. Waiting for 0 confirms.',
                 'Received ack for delivery tag 100 and all below. Waiting for 0 confirms.'])
    # (3) When we finish, all messages were already sent/acked:
    lines.append('Gentle finish (iteration 0): No more pending')
    # (4) At the end, the thread is joined:
    lines.append('[MainThread]: Joining... done')

    # Check contents of logfile:
    if all_lines_found(lines, logfile):
        return True
    else:
        return False
