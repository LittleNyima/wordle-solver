from .display import underline


def brief(rdict, quiet=False):
    count = [0 for _ in range(rdict["meta"]["max_attempts"] + 2)]
    success, total = 0, len(rdict["words"])
    total_tries = 0
    for _, tries in rdict["words"].items():
        count[tries] += 1
        if tries <= rdict["meta"]["max_attempts"]:
            success += 1
    for idx, tries in enumerate(count):
        total_tries += idx * tries
    average = total_tries / total
    success_rate = success / total
    if not quiet:
        underline("TRIES STATS")
        for idx, cnt in enumerate(count):
            if idx == 0: continue
            if idx <= rdict["meta"]["max_attempts"]:
                print("%16d  %d" % (idx, cnt))
            else:
                print("(FAILURE) %6d  %d" % (idx, cnt))
        print("%16s  %.4f" % ("AVERAGE", average))
        underline("SUCCESS STATS")
        print("%16s  %d" % ("SUCCESS", success))
        print("%16s  %.4f" % ("SUCCESS RATE", success_rate))
        underline("TIME COST")
        print("%16s  %.4f" % ("CPU TIME", rdict["time_cost"]))
    return {
        "tries": count,
        "success": success,
        "total": total,
        "average": average,
        "success_rate": success_rate,
        "time_cost": rdict["time_cost"]
    }
