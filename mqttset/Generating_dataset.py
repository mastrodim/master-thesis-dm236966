from Feature_extraction import Feature_extraction
import time
import warnings
warnings.filterwarnings('ignore')
import os
from tqdm import tqdm
from multiprocessing import Process
import numpy as np
import pandas as pd
from pathlib import Path

if __name__ == '__main__':

    start = time.time()
    print("========== CIC IoT feature extraction ==========")
    
    pcapfiles = [
        "PCAP/bruteforce.pcap",
        "PCAP/capture_1w.pcap",
        "PCAP/capture_flood.pcap",
        "PCAP/capture_malariaDoS.pcap",
        "PCAP/malformed.pcap",
        "PCAP/slowite.pcap",
    ]
    subfiles_size = 10  # MB
    split_directory = 'split_temp/'
    destination_directory = 'output/'
    converted_csv_files_directory = 'csv_files/'
    n_threads = 8
    
    # Ensure directories exist
    Path(split_directory).mkdir(parents=True, exist_ok=True)
    Path(destination_directory).mkdir(parents=True, exist_ok=True)
    Path(converted_csv_files_directory).mkdir(parents=True, exist_ok=True)

    for i in range(len(pcapfiles)):
        lstart = time.time()
        pcap_file = pcapfiles[i]
        print(pcap_file)
        print(">>>> 1. splitting the .pcap file.")
        os.system('tcpdump -r '+ pcap_file +' -w ' + split_directory + 'split_temp -C ' + str(subfiles_size))
        subfiles = os.listdir(split_directory)
        print(">>>> 2. Converting (sub) .pcap files to .csv files.")
        processes = []
        errors = 0
        
        subfiles_threadlist = np.array_split(subfiles, (len(subfiles)/n_threads)+1)
        for f_list in tqdm(subfiles_threadlist):
            n_processes = min(len(f_list), n_threads)
            assert n_threads >= n_processes
            assert n_threads >= len(f_list)
            processes = []
            for i in range(n_processes):
                fe = Feature_extraction()
                f = f_list[i]
                subpcap_file = os.path.join(split_directory, f)
                p = Process(target=fe.pcap_evaluation, args=(subpcap_file, os.path.join(destination_directory, f.split('.')[0])))
                p.start()
                processes.append(p)
            for p in processes:
                p.join()
        print('The length of subfiles : ', len(subfiles))
        print('The length of destination directory : ', len(os.listdir(destination_directory)))
        print(">>>> 3. Removing (sub) .pcap files.")
        for sf in subfiles:
            try:
                os.remove(os.path.join(split_directory, sf))
            except:
                pass

        print(">>>> 4. Merging (sub) .csv files (summary).")
        csv_subfiles = [f for f in os.listdir(destination_directory) if f.lower().endswith('.csv')]
        # Output path inside csv_files/, using the PCAP stem as filename
        pcap_stem = Path(pcap_file).stem  # e.g., 'bruteforce' from 'bruteforce.pcap'
        final_csv_path = os.path.join(converted_csv_files_directory, f"{pcap_stem}.csv")
        
        mode = 'w'
        for f in tqdm(csv_subfiles):
            try:
                d = pd.read_csv(os.path.join(destination_directory, f))
                d.to_csv(final_csv_path, header=(mode=='w'), index=False, mode=mode)
                mode='a'
            except:
                pass

        print(">>>> 5. Removing (sub) .csv files.")
        for cf in tqdm(csv_subfiles):
            try:
                os.remove(os.path.join(destination_directory, cf))
            except:
                pass
        print(f'done! ({pcap_file})(' + str(round(time.time()-lstart, 2))+ 's),  total_errors= '+str(errors))
        
    end = time.time()
    print(f'Elapsed Time = {(end-start)}s')
