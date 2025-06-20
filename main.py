import os
import subprocess


stats_dict = {
    "JobName" : [],
    "Parition": [],
    "AllocCPUs": [],
    "State": [],
    "Elapsed": []
}

def retrieve_stats() -> ():
    process = subprocess.Popen("sacct -u $(whoami) -n --start=1970-01-01 --format=JobName,Partition,AllocCPUS,State,Elapsed", shell=True, stdout=subprocess.PIPE)
    stdout, _ = process.communicate()

    stdout = stdout.decode().split('\n')[:-1]

    jobs_run = len(stdout)

    for job in stdout:
        line = job.split()
        i = 0
        for key in stats_dict.keys():
            stats_dict[key].append(line[i])
            i += 1


if __name__ == "__main__":
    retrieve_stats()