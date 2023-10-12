# FILE DUPLICATE FINDER AND MANAGER
###########################################################################################################

import os, logging, subprocess, time
                                                                                                                    #Importing the required packages and modules
###########################################################################################################
logging.basicConfig(filename="Log_file.log", encoding='utf-8', 
                    format='%(levelname)s (%(asctime)s): %(message)s [%(filename)s]',
                    datefmt='%d/%m/%Y %I:%M:%S %p', level=logging.DEBUG)

###########################################################################################################
def progress_bar(progress, total):                                                                                  #Function to print progress bar I have used num alt 219 for forming the bar
    percentage = 100 * (progress / float(total))
    bar = ('█' * int(percentage)) + ('-' * (100 - int(percentage)))
    # print()
    print(f"\r|{bar}| {percentage:.2f}%", end="\r")

###########################################################################################################
def backup(dstn, src):                                                                                              #Function to backup the duplicates
    progress_bar(0, len(src))
    count = 0
    for i in src:
        cmd = f"cp {i} {dstn}"
        os.system(cmd)
        progress_bar(count+1, len(src))
        count += 1
        logging.info(f"Taking backup for files {i} on {dstn}\Backup_files")

###########################################################################################################
def get_file_size(directory):                                                                                       #Function to get the size of the directory.
    cmd = f'du -s -h {directory}'                                                                                   #Helps to print the freed up space from the directory after moving/deleting the duplicates
    try:
        result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            file_size_str = result.stdout.split()[0]
            if 'K' in file_size_str:
                file_size = int(file_size_str.replace('K', '')) * 1024
            else:
                file_size = int(file_size_str)
            return file_size
        else:
            print("Command failed with error:")
            print(result.stderr)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

###########################################################################################################
l1, l2, l3 = [], [], []                                                                                             #Backbone of the program. It basically sort Original and repetitive files in the folder
def matching(link):                                                                                                 #Sorting done after comparing each files line by line with each other
    logging.info(f"Scanning for the group {link}")
    if len(link) == 0:
        return
    
    for i in range(len(link)):
        with open(link[i]) as compare1:
            file_text1 = compare1.readlines()
            
        for j in range(i, len(link)):
            with open(link[j]) as compare2:
                file_text2 = compare2.readlines()
            if file_text1 == file_text2 and file_text1 not in l1:
                l1.append(file_text1)
                l2.append(link[i])
            
    if open(link[-1]).readlines() not in l1:
        l1.append(open(link[-1]).readlines())
        l2.append(link[-1])
    for k in link:
        if k not in l2:
            l3.append(k)
    
    return l2, l3

###########################################################################################################   
def delete(array1):                                                                                                 #Function to delete the duplicates
    progress_bar(0, len(array1))
    count = 0
    lgt = len(array1)
    print("If you want to delete files which don't have write permissions just press y and hit enter else n")
    for i in array1:
        cmd = f"rm {i}"
        logging.info(f"Deleting {str(i)}")
        progress_bar(count+1, lgt)
        os.system(cmd)
        count += 1

###########################################################################################################
def movee(array1):                                                                                                  #Function to move the duplicates to the entered destination directory
    destination = input("Enter address of a destination directory: ")
    progress_bar(0, len(array1))
    count = 0
    print("If you want to move files which don't have write permissions just press y and hit enter else n")
    for j in array1:
        cmd = f"mv {j} {destination}"
        os.system(cmd)
        logging.info(f"Trying to Move {str(j)} to {str(destination)}")
        progress_bar(count+1, len(array1))
        count += 1

###########################################################################################################    
def rename(array1):                                                                                                 #Renaming function
    progress_bar(0, len(array1))                                                                                    #Used linux cmd to rename/delete/move/copy files inside python through os module.
    count = 0
    for k in range(len(array1)):
        print()
        inp = input(f"Enter a name for the {array1[k]} file:")
        filename = os.path.basename(array1[k])
        source_directory = os.path.dirname(os.path.realpath(array1[k]))
        
        if inp == "":
            progress_bar(count+1, len(array1))
            count += 1
            pass
        else:
            old_path = os.path.join(source_directory, filename)
            new_path = os.path.join(source_directory, inp)
            os.rename(old_path, new_path)
            logging.info(f"Renaming {str(old_path)} to {str(new_path)}")
            progress_bar(count+1, len(array1))
            count += 1

###########################################################################################################

def dir_scan(path):                                                                                                 #Used Recursion Time O(N) to access all the files and directory fom the source folder
    lnk_arr = []
    
    for i in os.scandir(path):
        if i.is_file():
            lnk_arr.append(i.path)
               
        elif i.is_dir():
            (matching(lnk_arr))
            lnk_arr = []
            lnk_arr += dir_scan(i.path)
        
    return lnk_arr

###########################################################################################################
inp = input("Enter a path: ")                                                                                       #Program will start executing from here. Passing the path to dir_scan and further passing inside matching function
if os.path.exists(inp) and os.access(inp, os.W_OK) and os.access(inp, os.R_OK):
    initial_size_of_directory = get_file_size(inp) 
    logging.info(f"Entered path: {inp}")
    
    # total_files = 0
    # for root, dirs, files in os.walk(inp):
    #     total_files += len(files)
    
    print("Scanning folder!!!")
    file_sort = (matching((dir_scan(inp))))

else:
    logging.info(f"Either entered a path which doesn't exist or its not having read/write permissions {inp}")
    print("Please enter a path which exists and have read and write permissions")
    print("Terminating...")
    time.sleep(1)
    exit(0)

###########################################################################################################
if len(file_sort[0]) != 0:
    print("Below is a list of original files path: ")                                                               #Printing list and groups of original and duplicate files
    for i in file_sort[0]:
        logging.info(f"Original {i}")
        print(i)
else:
    logging.info("Empty Directory. Terminating ...")
    print("Empty directory")
    time.sleep(1)
    exit()
print()
if len(file_sort[1]) != 0:
    print("Below is a list of duplicate file path: ")
    for j in file_sort[1]:
        logging.info(f"Duplicate {j}")
        print(j)
else:
    logging.info("No duplicates found!!! Terminating...")
    print("No duplicates found!!! Terminating...") 
    time.sleep(1) 
    exit()
print()

print("Printing different lists of file containg one original file and its duplicate")
for k in file_sort[0]:
    arr2 = []
    txt1 = open(k).readlines()
    arr2.append(k)
    for l in file_sort[1]:
        txt2 = open(l).readlines()
        if txt1 == txt2:
            arr2.append(l)
    print(arr2)
    
############################################################################################################## 
action = input("If you want to manage duplicate files then press 'Y' otherwise hit enter: ")
flag = False
if action == "Y":
    backp_execution = input("Do you want to take backup of the repeated files? if yes type Y else hit enter: ")
    if backp_execution == "Y":
        backp_destination = input("Enter a backup directory path: ")
        logging.info(f"Backup directory path: {backp_destination}")
        try: 
            if os.path.exists(backp_destination) and os.access(backp_destination, os.W_OK):
                backup(backp_destination, file_sort[1])
                print()
            else:
                logging.info(f"Failed to backup on {backp_destination} either it doses not exist or dont have write permissions")
            print("An error occurred while backuping seems like folder is not proper")
        except Exception as e:
            logging.info(f"Failed to backup on {backp_destination} due to exception: {e}")
            print("An error occurred", e)
    cmd_execution = input("Take one action in the given options or hit enter: (Delete) (Move) (Rename): ")
    if cmd_execution == "Delete":
        delete(file_sort[1])
        flag = True
    elif cmd_execution == "Move":
        movee(file_sort[1])
        flag = True
    elif cmd_execution == "Rename":
        rename(file_sort[1])
    else:
        pass
else:
    pass

###########################################################################################################
final_directory_size = get_file_size(inp)                                                                                   #Calculating size of the folder and space freed after moving or deleting
if flag == True:
    print()
    logging.info(f"Freed up space : {initial_size_of_directory-final_directory_size} Bytes from the current working directory")
    print(f"Freed up space : {initial_size_of_directory-final_directory_size} Bytes from the current working directory")
