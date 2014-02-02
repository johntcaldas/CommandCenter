"""
Utils Class

As much as I hate to have a "catchall" bucket such as this, I find it helps to use it -- "temporarily."
That is, the purpose of this file is as a temporary container for pieces of functionality that don't yet have enough
buddies to go form a club somewhere.

Also, although now this is hanging out in 'services', there should probably be another home for python code. The purpose
of services is to be high-level (just under web service-aware interfaces) functionality.

"""
import os


def get_command_output_by_line(self, command):
    """
    Pass 'command' to the operating system, and return a list of output lines.
    """

    # TODO: handle error?
    handle = os.popen(command)

    output_by_line = []

    for line in handle.readlines():
        output_by_line.append(line)

    return output_by_line
