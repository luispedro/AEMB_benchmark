from collections import namedtuple

ResourceUsage = namedtuple('ResourceUsage', ['running_time', 'memory_usage'])


def parse_time_output(log_file):
    ''' Parse the output of a time command
    Args:
        log_file (str): The path to the log file to parse.
    Returns:
        ResourceUsage: A named tuple containing the running time and memory usage.
    '''
    with open(log_file) as fh:
        running_time = 0
        memory = 0
        for line in fh:
            if line.strip().startswith("Command exited with non-zero"):
                raise ValueError(f'Error in the process {log_file}, exit status is not 0')

            name, value = line.strip().split(": ")
            value = value.strip('"')

            if name == "Exit status":
                if int(value) != 0:
                    raise ValueError(f'Error in the process {log_file}, exit status is not 0')

            if name == "Elapsed (wall clock) time (h:mm:ss or m:ss)":
                if '.' in value:
                    value = value.split(":")
                    value[-1] = round(float(value[-1]))
                else:
                    value = value.split(":")

                if len(value) == 2:
                    seconds = int(value[0]) * 60 + int(value[1])
                elif len(value) == 3:
                    seconds = int(value[0]) * 3600 + int(value[1]) * 60 + int(value[2])
                else:
                    raise ValueError(f"Unknown time format {value} in {log_file}")
                value = seconds
                running_time = value

            if name == 'Maximum resident set size (kbytes)':
                memory = int(value)/1024
    return ResourceUsage(running_time, memory)

