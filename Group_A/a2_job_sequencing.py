def schedule_jobs(jobs):
    # A job is (name, deadline, profit).
    valid = [job for job in jobs if job[1] > 0 and job[2] > 0]
    if not valid:
        return [], 0

    horizon = min(len(valid), max(job[1] for job in valid))
    slots = [None] * horizon
    profit = 0
    for job in sorted(valid, key=lambda j: j[2], reverse=True):
        name, deadline, value = job
        for slot in range(min(deadline, horizon) - 1, -1, -1):
            if slots[slot] is None:
                slots[slot] = job
                profit += value
                break
    return slots, profit


if __name__ == "__main__":
    n = int(input("Number of jobs: "))
    jobs = []
    for i in range(n):
        entry = input(f"Job {i + 1} (ID Deadline Profit): ").strip().split()
        if len(entry) >= 3:
            name, deadline, profit = entry[0], int(entry[1]), int(entry[2])
        elif len(entry) == 2:
            name, deadline, profit = f"J{i + 1}", int(entry[0]), int(entry[1])
        elif len(entry) == 1:
            name = entry[0]
            deadline = int(input(f"  Deadline for {name}: "))
            profit = int(input(f"  Profit for {name}: "))
        else:
            name = f"J{i + 1}"
            deadline = int(input(f"  Deadline for Job {i + 1}: "))
            profit = int(input(f"  Profit for Job {i + 1}: "))
        jobs.append((name, deadline, profit))

    slots, profit = schedule_jobs(jobs)
    for time, job in enumerate(slots, start=1):
        print("Slot", time, ":", job[0] if job else "Idle")
    print("Maximum profit:", profit)
