""" Summary usage statistics for SLURM-managed compute clusters """

import subprocess

DEFAULT_STATS = ["JobName", "Partition", "AllocCPUS", "State", "Elapsed"]


def convert_seconds_to_hms(seconds: int) -> str:
    """ Converts seconds to a string in the format HH:MM:SS """

    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"


def retrieve_stats() -> None:
    """ Retrieves statistics from SLURM and stores in a dictionary """

    # pylint: disable-next=consider-using-with
    process = subprocess.Popen(
        f"sacct -u $(whoami) -n --start=1970-01-01 --format={','.join(DEFAULT_STATS)}",
        shell=True, stdout=subprocess.PIPE)

    stdout, _ = process.communicate()

    stdout = stdout.decode().split('\n')[:-1]

    total_jobs_run = len(stdout)

    stats_dict = {key: [] for key in DEFAULT_STATS}

    for job in stdout:
        line = job.split()
        i = 0
        for key in stats_dict.keys():
            stats_dict[key].append(line[i])
            i += 1

    unique_job_names = len(set(stats_dict["JobName"]))
    unique_partitions = len(set(stats_dict["Partition"]))

    total_compute_seconds = 0
    for time in stats_dict["Elapsed"]:
        h, m, s = [int(t) for t in time.split(':')]
        total_compute_seconds += 3600 * h + 60 * m + s

    print(f"Total jobs run: {total_jobs_run}")
    print(f"Unique job names: {unique_job_names}")
    print(f"Unique partitions: {unique_partitions}")
    print(f"Total compute time: {convert_seconds_to_hms(total_compute_seconds)}")


if __name__ == "__main__":
    retrieve_stats()
