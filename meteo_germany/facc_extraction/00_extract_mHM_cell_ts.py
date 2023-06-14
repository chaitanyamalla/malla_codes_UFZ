'''

Purpose: Extract timeseries from netcdf-data (mHM Output or gridded input data)
Written by Friedrich Boeing, Nov 2019

'''
#!/usr/bin/env python
import numpy as np
import ufz   as ufz
from ufz.netcdf4 import NcDataset
import pandas as pd
import optparse
import datetime
from cftime import num2date, date2num
import os

parser = optparse.OptionParser(
    usage='%prog -i [infile] -o [outfile] ] ..',
    description="Plotting of SMI for drought monitor."
)
parser.add_option(
    '-i', '--infile', action='store', dest='infile', type=str,
    help='NetCDF file name.'
)

parser.add_option(
    '-o', '--outfile', action='store', dest='outfile', type=str,
    help='Name of the outputfile.'
)

parser.add_option(
    '-c', '--COORDs', action='store', dest='COORDs', type=str,
    help='Lat Lon Coordinates "51.2, 10.5".'
)

parser.add_option(
    '-w', '--write_data', action='store', dest='write', type=str,
    help='write data or only search for grid cells.'
)

parser.add_option(
    '-v', '--VARs', action='store', dest='VARs', type=str,
    help='Variables to extract. if '' all variables in file are extracted.'
)
parser.add_option(
    '-l', '--latlon', action='store', dest='latlon', type=str,
    help='latlon file.'
)






def latlon_extractor(lat,lon,lats,lons):
    print("Searching for right cell ..")
    for i in np.arange(1,lons.shape[0]-1): # range(ymin, ymax):
        for j in np.arange(1,lons.shape[1]-1): # range(xmin, xmax):

            #lat lon value of grid cells defined as middlepoint
            # !! because of irregular grid the loop starts at 1 and engs n -1, but indexes are starting at 0
            term1=(lons[i+1,j+1]-lons[i,j])/2
            term2=(lons[i-1,j+1]-lons[i,j])/2
            term3=(lons[i-1,j-1]-lons[i,j])/2
            term4=(lons[i+1,j-1]-lons[i,j])/2
            # print(str(term1),str(term2),str(term3),str(term4))
            coord_lons=np.array([lons[i,j]+term1,lons[i,j]+term2,lons[i,j]+term3,lons[i,j]+term4])
            term1=(lats[i+1,j+1]-lats[i,j])/2
            term2=(lats[i-1,j+1]-lats[i,j])/2
            term3=(lats[i-1,j-1]-lats[i,j])/2
            term4=(lats[i+1,j-1]-lats[i,j])/2

            coord_lats=np.array([lats[i,j]+term1,lats[i,j]+term2,lats[i,j]+term3,lats[i,j]+term4])

            value = ufz.in_poly([lon, lat], coord_lons, coord_lats)
            #print(str(i) + ' ' + str(j) + ' ' + str(value))
            if value == 1:
                print('found the right cell: y ' + str(i) + ' and x ' + str(j))
                print("lat: " + str(lat) + " lon:" + str(lon))
                print(str(coord_lons))
                print(str(coord_lats))
                x_val=j
                y_val=i
                break
    return x_val,y_val
def write_data(y_val,x_val,VARs,round_dig=4):
    print(VARs)
    if VARs == '':
        VARs     = ufz.readnetcdf(nc_infile,variables=True)
        var_list=["time","time_bnds","northing","easting","lat","lon"]
        for var_rm in var_list:
            if var_rm in VARs:
                VARs.remove(var_rm)
    else:
        VARs     = list(VARs.split(', ')) 

    timeunit  = ufz.readnetcdf(nc_infile, var='time', attributes=True)['units']
    times     = ufz.readnetcdf(nc_infile, var='time')
    datetimes = num2date(times,units=timeunit,only_use_cftime_datetimes=False)
    years     = np.array([d.year for d in datetimes.data])
    months    = np.array([d.month for d in datetimes.data])
    days      = np.array([d.day for d in datetimes.data])
    dates     = ["{:}-{:}-{:}".format(years[i],str(months[i]).zfill(2),str(days[i]).zfill(2)) for i in range(len(times))]

    data_all=np.empty([times.shape[0],len(VARs)])
    data_all[:]=-9999

    ncin = NcDataset(nc_infile, 'r')
    # read netcdf files:
    x=0
    for var in VARs:
        print('extract data from variable: {:}'.format(var))
        data_all[:,x] = ncin.variables[var][:,y_val,x_val]
        x=x+1

    data_all=np.round(data_all,round_dig)
    res = pd.DataFrame(data_all,index=dates,columns=VARs)
    res.rename_axis('time')
    return res

def write_dem(y_val,x_val,round_dig=4):
    ncin = NcDataset(nc_infile, 'r')
    val=np.round(ncin.variables["dem"][y_val,x_val],round_dig)
    print(val)
    return val

if __name__ == '__main__':
    (opts, args)   = parser.parse_args()
    nc_infile      = opts.infile
    outfile        = opts.outfile
    loc_infile     = opts.COORDs
    # COORDs       = list(COORDs.split(',')) 
    VARs           = opts.VARs
    write          = opts.write
    nc_latlon_file = opts.latlon
    #  -- set netcdf file names ------------------------

    nc_lons          = ufz.readnc(nc_latlon_file, var='lon') 
    nc_lats          = ufz.readnc(nc_latlon_file, var='lat')


    #  -- set locations file names ---------------------

    loc_lat_name,loc_lon_name = "Breite","Lange"#"POINT_Y","POINT_X"  # !!! set to point column names for Y(lat, breite) and X (lon, Länge)
    delimiter=","  # !!! define delimiter of the csv file
    loc_outpath="./" # define outpath 


    print(loc_infile)
    loc_file          = pd.read_csv(loc_infile,delimiter=delimiter)
    loc_filename      = loc_infile.split('/')[-1]
    loc_lats,loc_lons = loc_file[loc_lat_name], loc_file[loc_lon_name]
    #  --  loop through list of locations --------------
    dem_dat=pd.DataFrame(columns=["ID","DEM"])
    round_dig=4
    nn=1
    for loc_lat, loc_lon in zip(loc_lats,loc_lons):
        xyFilename='xy_lon{:}_lat{:}.txt'.format(loc_lon,loc_lat)
        if os.path.exists(xyFilename):
            print("xy File already exists..")
            xyFile=pd.read_csv(xyFilename)
            x_val, y_val=xyFile["x"].values[0],xyFile["y"].values[0]
            print("x: ",x_val,"y: ",y_val)
        else:
            x_val,y_val=latlon_extractor(loc_lat,loc_lon,nc_lats,nc_lons)
            print("x: ",x_val,"y: ",y_val)
            xyFile=open(xyFilename,'w')
            # write grid cells
            xyFile.writelines(["x,y\n"])
            xyFile.writelines([str(x_val),",",str(y_val)])
            xyFile.close()

        point_name="{:}-{:}".format(loc_filename.split('.')[0],nn)
        if write == "T":
            if VARs == "dem" or "dem" in ufz.readnetcdf(nc_infile,variables=True):
                print("extract dem.. for location {:}".format(nn))
                dem_dat=dem_dat.append({'ID'  :                              nn,
                                        'DEM' : write_dem(y_val,x_val,round_dig)},ignore_index=True)
            else:
                if outfile == "":
                    outfile_w ="{:}/{:}.txt".format(loc_outpath,point_name)   # plt.show()
                else:
                    outfile_w =outfile
                print('writing file: {:}'.format(outfile_w))
                res=write_data(y_val,x_val,VARs)
                res.to_csv(outfile_w, index = True,index_label="Time")
                # plt.plot(data_all)
        nn = nn + 1
    if VARs == "dem" or "dem" in ufz.readnetcdf(nc_infile,variables=True):
        if outfile == "":
            outfile_w ="{:}/{:}_dem.txt".format(loc_outpath,loc_filename)   # plt.show()
        else:
            outfile_w =outfile
        dem_dat.to_csv(outfile_w, index = False)


