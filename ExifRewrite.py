# -*- coding: cp1251 -*-
#
# install PIP, import `PIL` and `piexif first`
#   PIP:
#     https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip
#     python get-pip.py
#   piexif
#     python -m pip install piexif
#   PIL
#     python -m pip install pillow
#

from __future__ import print_function
import sys, os, piexif

################## parameters ##################
path_with_files  = r'E:\iMAGES\2019-08 Turkey, Kemer, Beldibi\2019-08 Kemer 1\Lightroom'
delete_exif_data = True
print_exif_data  = False
################## variables ###################
image_make       = 'Milok Zbrozek'
image_model      = 'by Nikon'
image_software   = 'Milok Zbrozek ImageReady'
image_artist     = 'Photographer: Milok Zbrozek'
image_copyright  = 'Copyright (c) 2019 Milok Zbrozek milokz@gmail.com'
image_comment    = 'Turkey, Kemer, 2019'
################################################


def process_file(file_name):
    # list of tags:    
    #     https://www.exiv2.org/tags.html	
    
    exif_data = {'0th': {}} # empty
    try:
        if not delete_exif_data:
            exif_data = piexif.load(file_name)
    except piexif._exceptions.InvalidImageDataError:    
        print('  Skip', end='')
        return
    except:
        pass
    
    exif_data['0th'][270]   = image_comment   # comment
    exif_data['0th'][271]   = image_make      # make
    exif_data['0th'][272]   = image_model     # model
    exif_data['0th'][305]   = image_software  # software
    exif_data['0th'][315]   = image_artist    # artist
    exif_data['0th'][33432] = image_copyright # copyright
    
    exif_bytes = piexif.dump(exif_data)
    try:
        piexif.insert(exif_bytes, file_name)
    except:
		print('  Error', end='')
    else:
        print('  Done', end='')
    
    if print_exif_data:
        print()
        for ifd in ("0th", "Exif", "GPS", "1st"):
            try:
                exif_data[ifd]
            except:
                pass
            else:                
                for tag in exif_data[ifd]:
                    print('    {0: >4}[{1:0<5}] {2: <28} {3}'.format(ifd, tag, piexif.TAGS[ifd][tag]["name"] + ':', exif_data[ifd][tag]))
    

def main(args = []):
    print('Make        = {0}'.format(image_make))
    print('Model       = {0}'.format(image_model))
    print('Software    = {0}'.format(image_software))
    print('Artist      = {0}'.format(image_artist))
    print('Copyright   = {0}'.format(image_copyright))
    print('Comment     = {0}'.format(image_comment))
    print('Delete Exif = {0}'.format(delete_exif_data))
    print()    
    print('Processing directory', path_with_files)    
    files_in_dir = [f for f in os.listdir(path_with_files) if os.path.isfile(os.path.join(path_with_files, f))]
    print('Total {0} files'.format(len(files_in_dir)))
    for i in range(len(files_in_dir)):
        ext = str(os.path.splitext(files_in_dir[i])[1].upper())
        print('  {0:0>4}/{2:0>4}: {1:<26} ... '.format(i + 1, files_in_dir[i], len(files_in_dir)), end='')
        if ext == '.JPG' or ext == '.JPEG':            
            process_file(os.path.join(path_with_files, files_in_dir[i]))
            print('  ')
        else:
            print('  Skip')
    print('Done')

if __name__ == '__main__':
    print('Milok Zbrozek ImageReady Python Script')
    print('Copyrights (c) 2019 Milok Zbrozek milokz@gmail.com')
    print()
	# print('Cmd line arguments:', sys.argv)
    # print('Current Dir:', os.getcwd())
    main(sys.argv)		