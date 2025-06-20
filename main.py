""" Summary usage statistics for SLURM-managed compute clusters """

import subprocess

DEFAULT_STATS = ["JobName", "Partition", "AllocCPUS", "State", "Elapsed"]


def retrieve_stats() -> ():
    """ Retrieves statistics from SLURM and stores in a dictionary """

    process = subprocess.Popen(
        f"sacct -u $(whoami) -n --start=1970-01-01 --format={','.join(DEFAULT_STATS)}",
        shell=True, stdout=subprocess.PIPE)

    stdout, _ = process.communicate()

    stdout = stdout.decode().split('\n')[:-1]

    jobs_run = len(stdout)

    stats_dict = {key: [] for key in DEFAULT_STATS}

    for job in stdout:
        line = job.split()
        i = 0
        for key in stats_dict.keys():
            stats_dict[key].append(line[i])
            i += 1

    print("Total jobs run: " + jobs_run)

if __name__ == "__main__":
    retrieve_stats()
