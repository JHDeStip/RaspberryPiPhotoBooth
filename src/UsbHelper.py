import os
import subprocess
import ctypes

class UsbHelper(object):
    # Take sda1 or sdb1 as partition to mount
    _PARTITION_FILES = ["/dev/sda1", "/dev/sdb1"]

    _mountDirectory = None
    _subDirectories = None

    def __init__(self, mountDirectory, subDirectories):
        self._mountDirectory = mountDirectory
        self._subDirectories = subDirectories


    def isMounted(self):
        try:
            if not os.path.ismount(self._mountDirectory):
                return False

            for subdirectory in self._subDirectories:
                if not os.path.isdir(os.path.join(self._mountDirectory, subdirectory)):
                    return False
            
            return True
                    
        except:
            return False


    def mount(self):
        try:
            if os.path.ismount(self._mountDirectory):
                self.createDirectoriesIfNeeded()
                return True
            
            if not os.path.isdir(self._mountDirectory):
                os.makedirs(self._mountDirectory, 644)

            if not (os.access(self._mountDirectory, os.R_OK) and os.access(self._mountDirectory, os.W_OK)):
                return False
            
            partitionToMount = None
            
            for partitionFile in self._PARTITION_FILES:
                if os.path.exists(partitionFile):
                    partitionToMount = partitionFile
                    break
            
            # If no drive is found we cannot mount
            if partitionToMount == None:
                return False
            
            subprocess.check_call(["mount", partitionToMount, self._mountDirectory])
            self.createDirectoriesIfNeeded()
            
            return True
        except:
            return False


    def unmount(self):
        try:
            if os.path.ismount(self._mountDirectory):
                subprocess.check_call(["umount", self._mountDirectory])

            return True
        except:
            return False

    def createDirectoriesIfNeeded(self):
        for subdirectory in self._subDirectories:
            fullPath = os.path.join(self._mountDirectory, subdirectory)
            if not os.path.isdir(fullPath):
                os.makedirs(fullPath, 644)