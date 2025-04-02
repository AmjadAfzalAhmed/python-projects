import os # import os module 

# function to rename files
def rename_files():
    i = 0 # counter
    # path to the directory where images / files are stored
    path = "F:/Python Practice/Python Web Apps/python-projects/22-file-renamer/images/"

    # loop through the files in the directory
    for filename in os.listdir(path):
        # create new filename
        my_file = 'img' + str(i) + '.jpg'
        # create full path to the file
        my_source = path + filename
        # create full path to the new filename
        my_dest = path + my_file
        # rename the file
        os.rename(my_source, my_dest)
        # increment the counter
        i += 1


if __name__ == '__main__':
    rename_files()
