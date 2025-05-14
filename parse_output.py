def parse_time_output(log_file):
    with open(log_file) as fh:
        running_time = 0
        memory = 0
        for line in fh:
            if line.strip().startswith("Command exited with non-zero"):
                print('error')
                continue

            name, value = line.strip().split(": ")
            value = value.strip('"')

            if name == "Exit status":
                if int(value) != 0:
                    print('error')

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
                    raise Exception("Unknown time format {}".format(value))
                value = seconds
                running_time = value

            if name == 'Maximum resident set size (kbytes)':
                memory = int(value)/1024
    return running_time, memory


