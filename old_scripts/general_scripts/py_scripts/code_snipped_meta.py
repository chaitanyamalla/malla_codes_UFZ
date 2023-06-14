import pandas as pd

if __name__ == '__main__':
  #  meta                    = pd.read_csv("/data/hicam/data/processed/meteo/germany/climproj/euro-cordex/88realizations_mhm/88_main_LUT.txt",sep=" ")
     meta                    = pd.read_csv("MET_list.txt",sep=" ")
    met_ids                 = np.sort(pd.unique(meta["met_id"]))
    if len(met_ids) < 88: # if not all simulations are in the directory
        met_ids                 = np.sort(os.listdir("/work/malla/ww_leipzig/output_periods/"))
    # met_ids                 = ["met_001", "met_002"]

    # list of names of the rcps climate models
    gcms                    = np.sort(pd.unique(meta["gcm"]))
    # list of names of the regional climate models
    rcms            = np.sort(pd.unique(meta["inst.rcm"]))
    # list of names of the hydrological models
    hms                     = ['mHM']
    # list of names of the rcps
    # rcps                    = ['rcp2p6', 'rcp6p0', 'rcp8p5']
    rcps                    = np.sort(pd.unique(meta["rcp"]))

