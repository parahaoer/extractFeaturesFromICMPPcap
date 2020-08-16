import os


def get_filelist(dir):

    if os.path.isfile(dir):
        if dir.find('negative') == 9:
            print('negative')
        elif dir.find('positive') == 9:
            print('positive')
        print(dir)

    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            get_filelist(newDir)


get_filelist('pcap_dir')