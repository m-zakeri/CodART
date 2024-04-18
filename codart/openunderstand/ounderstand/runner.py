from multiprocessing import cpu_count, Pool
from openunderstand.ounderstand.parsing_process import process_file, get_files


def runner(path_project: str = ""):
    files = get_files(path_project)
    with Pool(cpu_count()) as pool:
        pool.map_async(process_file, files)
        pool.close()
        pool.join()
