# -*- coding: cp1251 -*-
#
# Milok Zbrozek File Rename With Exif Python Script
# Copyrights (c) 2019 Milok Zbrozek milokz@gmail.com
# Tested on Python 2.7.16 Windows XP with piexif and PIP
#
# install PIP, import `piexif first`
#   PIP:
#     https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip
#     python get-pip.py
#   piexif
#     python -m pip install piexif
#

from __future__ import print_function
import sys, os, piexif

################################################
################## parameters ##################
################################################

                     # {fileType} {origin} {fileNo} {exifDT}
filename_mask        = r'[1908TRK_{fileType}{fileNo:0<4}] {exifDT}';    
              
				     # in lower case ['*.*'] ['*.jpg'] ['.jpg'] ['.jpg','*.mp4']
file_to_search       = ['*.jpg','*.mp4']                  

dir_to_search        = r'E:\iMAGES\2019-08 Turkey, Kemer, Beldibi'
subdirectories       = True
start_index          = 1

#################### EXIF ######################

exif_rewrite         = False
exif_delete_existing = False
exif_print_data      = False

image_make           = 'Milok Zbrozek'
image_model          = 'by Nikon'
image_software       = 'Milok Zbrozek ImageReady'
image_artist         = 'Photographer: Milok Zbrozek'
image_copyright      = 'Copyright (c) 2019 Milok Zbrozek milokz@gmail.com'
image_comment        = 'Turkey, Kemer, 2019'

################################################
################################################
################################################

def rewite_exif(file_path):
    # list of tags:   https://www.exiv2.org/tags.html	   
    exif_data = {'0th': {}} # empty
    try:
        if not exif_delete_existing:
            exif_data = piexif.load(file_path)
    except piexif._exceptions.InvalidImageDataError:    
        print('Wrong Type', end='')
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
        piexif.insert(exif_bytes, file_path)
    except:
		print('Exif Fail', end='')
    else:
        print('Exif RW', end='')
    
    if exif_print_data:
        print()
        for ifd in ("0th", "Exif", "GPS", "1st"):
            try:
                exif_data[ifd]
            except:
                pass
            else:                
                for tag in exif_data[ifd]:
                    print('{0: >4}[{1:0<5}] {2: <28} {3}'.format(ifd, tag, piexif.TAGS[ifd][tag]["name"] + ':', exif_data[ifd][tag]))


def get_exif_dt(file_path):
    try:
        return str(piexif.load(file_path)['0th'][306]).replace(':','')
    except:    
       return ''    

def process_file(folder, file_path, file_name, file_index):    
    fnwo, ext = os.path.splitext(file_name)
    
    isjpeg    = False
    file_type = 'U' # unknown
    exif_dt   = ''    
    extu      = ext.upper()	
    
    if extu == '.JPG' or extu == '.JPEG':
        file_type = 'I'
        isjpeg = True
        if filename_mask.count('{exifDT}') > 0:
            exif_dt = get_exif_dt(file_path)
    elif extu == '.PNG' or extu == '.BMP':
        file_type = 'I'
    elif extu == '.GIF':
        file_type = 'G'
    elif extu == '.MP4' or  extu == '.MPG' or extu == '.MPEG' or extu == '.MPEG2' or extu == '.AVI' or extu == '.WMV' or extu == '.MKV' or extu == '.MOV':
        file_type = 'V'
    
    new_file_path = filename_mask.format(fileNo=file_index,fileType=file_type,origin=fnwo,exifDT=exif_dt).strip() + ext
    full_newfn = os.path.join(folder, new_file_path)
    
    try:
        os.rename(file_path, full_newfn)
    except:
        print('Error', end='')
    else:
        print(new_file_path, end='')
    
    if exif_rewrite and isjpeg:
        print(' ... ', end='')
        rewite_exif(full_newfn)
    

def main(args = []):
    folders = [dir_to_search]
    if subdirectories:
        for r, d, f in os.walk(dir_to_search):
            for folder in d:
                folders.append(os.path.join(r, folder))
    
    processed_file_index  = start_index
    processed_files_count = 0
    
    if exif_rewrite:
        print('Make           = {0}'.format(image_make))
        print('Model          = {0}'.format(image_model))
        print('Software       = {0}'.format(image_software))
        print('Artist         = {0}'.format(image_artist))
        print('Copyright      = {0}'.format(image_copyright))
        print('Comment        = {0}'.format(image_comment))
        print('Delete Exif    = {0}'.format(exif_delete_existing))        
        print()
        print('File Name Mask  =', filename_mask)		
        print('Dir To Search   =', dir_to_search)		
        print('Files To Search =', file_to_search)		
        print('Processing Rename Files and Rewrite JPG Exif Data...')
    else:
        print()
        print('File Name Mask  =', filename_mask)		
        print('Dir To Search   =', dir_to_search)		
        print('Files To Search =', file_to_search)		
        print('Processing Rename Files...')       
    total_files_found = 0
    total_files_index = 0
    for folder in folders:        
        files_in_dir = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        total_files_found += len(files_in_dir)
    print('Found {0} files in {1} folders'.format(total_files_found,len(folders)))
    
    if args.count('/silent') == 0:
        raw_input("Press Enter to continue... ")
    
    for folder in folders:        
        files_in_dir = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        if len(files_in_dir) > 0:
            print('{0} files in {1}'.format(len(files_in_dir), folder))        
        for i in range(len(files_in_dir)):
            skip = False
            if not file_to_search[0] == '*.*':
                skip = True
                for fce in file_to_search:
                    if files_in_dir[i].lower().endswith(fce.replace('*','')):
                        skip = False
            if not skip:                
                print('  {5:0>6.2%}/{3:0>5}/{4:0>5} - {0:0>4}/{2:0>4} : {1:<12} > '.format(i + 1, files_in_dir[i], len(files_in_dir), total_files_index, total_files_found, 1.0 * total_files_index /  total_files_found), end='')
                process_file(folder, os.path.join(folder, files_in_dir[i]), files_in_dir[i], '{:0>4}'.format(processed_file_index))
                processed_file_index += 1
                processed_files_count += 1
                print('  ')
            total_files_index += 1
    print('Processed 100% - {0} of {2} ({4} ignored) files in {1} folders with {3} filter'.format(processed_files_count,len(folders), total_files_found, file_to_search, total_files_found - processed_files_count))
    print('DONE')
    if args.count('/silent') == 0:
        raw_input("Press Enter to Exit... ")

if __name__ == '__main__':
    print('Milok Zbrozek File Rename With Exif Python Script')
    print('Copyrights (c) 2019 Milok Zbrozek milokz@gmail.com')
    print('  arguments: /silent')
    print()
	# print('Cmd line arguments:', sys.argv)
    # print('Current Dir:', os.getcwd())
    main(sys.argv)		