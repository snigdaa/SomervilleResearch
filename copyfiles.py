shuimport os.path
from shutil import copy
import numpy as np

base = '/home/sss274/Work/cosmo/'
hydrodir = '/projects/somerville/GADGET-3/Fiducial_Models/Fiducial_withAGN_hdf/'

for root, dirs, files in os.walk(base):
    for name in dirs:
        if name[3:5]=='44':
            newbase = os.path.join(base,name)
            #os.remove(newbase+'/parameters_model.py')
            #copy(base+'parentfiles/parameterstest.py', newbase)
            #copy(base+'parentfiles/pd.cmd', newbase)
            #copy(base+'parentfiles/parameters_master.py', newbase)
            for root, dirs, files in os.walk(newbase):
                for each in files:
                    #print each
                    #print newbase
                    #print os.path.join(newbase,each)
                    if each=='parameterstest.py':
            #            print each
                        appending = ''
                        xcent = 0.0
                        ycent = 0.0
                        zcent = 0.0
                        #f is opening the parameters test file
                        f = open(os.path.join(newbase,each), 'r')
                        #fnew creates the needed parameters_model file
                        fnew = open(os.path.join(newbase, 'parameters_model.py'), 'w')
                        for idx, val in enumerate(list(f)):
                        #change all unique values that you have to change in parameters model
                        #by using the 'name' (halo name) from the directory you're looking at
                        #in addition to using info file info (for center coordinates). Idx num
                        #is one less than row actual number

                            #change the hydro dir input file
                            if idx == 11:
                                print val[-8:-3]
                                appending = val[:-8]+name[5:]+val[-3:]
                                fnew.write(appending)
                            #Change gadget_snap_name
                            elif idx == 12:
                                appending = val[:25]+name[5:]+val[30:]
                                fnew.write(appending)
                            #Change PD output directory
                            elif idx == 15:
                                print val[-13:-3]
                                appending = val[:-13]+name+val[-3:]
                                fnew.write(appending)
                            #change input file loc & name
                            elif idx == 24:
                                print val[-28:-24]
                                appending = val[:-28]+name[6:]+val[-24:]
                                fnew.write(appending)
                            #change output file loc & name
                            elif idx == 25:
                                print val[-29:-25]
                                appending = val[:-29]+name[6:]+val[-25:]
                                fnew.write(appending)
                            elif idx == 30:
                            #change the 'center' coordinates for each halo
                                print val[9:]
                                infodir = hydrodir+'/'+name[5:]+'/'
                                for one, subone, subtwo in os.walk(infodir):
                                    for infos in subtwo:
                                        if infos == 'info_044.txt':
                                            print infos
                                            centers=open(os.path.join(infodir,infos))
                                            #open the info file and find the centers
                                            for num,line in enumerate(list(centers)):
                                                if num==6:
                                                    xcent= line[23:37]
                                                    ycent= line[39:53]
                                                    zcent= line[55:68]
                                appending = val[:9]+str(xcent)+'\n'
                                fnew.write(appending)
                            elif idx == 31:
                                print val[9:]
                                appending = val[:9]+str(ycent)+'\n'
                                fnew.write(appending)
                            elif idx == 32:
                                print val[9:]
                                appending = val[:9]+str(zcent)+'\n'
                                fnew.write(appending)
                            else:
                                fnew.write(val)
                        f.close()
                        fnew.close()
