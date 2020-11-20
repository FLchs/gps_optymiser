import joblib
# Starts process in parallel


def run(n_jobs, func, arr):
    return joblib.Parallel(n_jobs, prefer='threads')(joblib.delayed(func)(tgt) for tgt in arr)


def run_with_args(n_jobs, func, arg, arr):
    return joblib.Parallel(n_jobs, prefer='threads')(joblib.delayed(func)(tgt, arg) for tgt in arr)
