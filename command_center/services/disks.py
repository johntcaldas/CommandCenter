"""
Disks Service

This service exposes information about hard disks in the system.

This is the first service (in order of code creation) requiring 'root' access to run commands on the host machine
(eg. sudo parted -lms). For now, I added:
    jcaldas ALL=(ALL) NOPASSWD: ALL
using 'visudo'. Eventually this application will be run as a web server user and it will probably make sense to
give only access to specific commands.

Info on fine grained command control for sudoers:
http://ubuntuforums.org/showthread.php?p=7118727#post7118727
"""

import os
import re

class DiskService():

    def get_disks(self):
        """
        Use 'sudo parted -lms' to get the list of disks on the system.

        Sample output:
        BYT;
        /dev/sda:128GB:scsi:512:512:msdos:ATA OCZ-VERTEX;
        1:1049kB:119GB:119GB:ext4::boot;
        2:119GB:128GB:8588MB:::;
        5:119GB:128GB:8588MB:linux-swap(v1)::;

        Error: The primary GPT table is corrupt, but the backup appears OK, so that will be used.
        BYT;
        /dev/sdb:3001GB:scsi:512:512:gpt:ATA Hitachi HDS72303;
        1:17.4kB:3001GB:3001GB:ext4::;

        ...

        We want to cluster the line starting with '/dev/' with each following line until we reach a blank line. This
        will represent the information we have about a single disk.

        """

        parted_handle = os.popen('sudo parted -lms')
        disks_by_line = []

        # First, read in all the command output
        for line in parted_handle.readlines():
            disks_by_line.append(line)

        # Gather disk/partition info by disk
        disks = []       # our list of disks
        disk_index = 0   # current 'disk' index (independent of line)
        part_index = 0   # current 'partition' index
        in_disk = False  # are we currently inside a block of disc information
        raid_arrays = 0  # count the number of raid arrays

        for line in disks_by_line:
            if "/dev/" in line and "Error" not in line and "Warning" not in line:
                # This is the first line of a disk's information
                # eg. /dev/sda:128GB:scsi:512:512:msdos:ATA OCZ-VERTEX;

                in_disk = True
                disks.append({})
                split_line = line.split(':')

                disks[disk_index]['device'] = split_line[0]
                disks[disk_index]['size'] = split_line[1]
                disks[disk_index]['bus'] = split_line[2]
                disks[disk_index]['logical_sector_size'] = split_line[3]
                disks[disk_index]['physical_sector_size'] = split_line[4]
                disks[disk_index]['partition_table'] = split_line[5]
                disks[disk_index]['model'] = split_line[6].rstrip(';\n')

                if disks[disk_index]['bus'] == "md":
                    raid_arrays += 1

            elif line == '\n' and in_disk:
                in_disk = False
                disk_index += 1
                part_index = 0

            elif in_disk:
                # This is a line describing a partition of the current disk.
                # eg. 1:1049kB:119GB:119GB:ext4::boot;

                if 'partitions' not in disks[disk_index]:
                    disks[disk_index]['partitions'] = []

                disks[disk_index]['partitions'].append({})
                split_line = line.split(':')

                disks[disk_index]['partitions'][part_index]['number'] = split_line[0]
                disks[disk_index]['partitions'][part_index]['start'] = split_line[1]
                disks[disk_index]['partitions'][part_index]['end'] = split_line[2]
                disks[disk_index]['partitions'][part_index]['size'] =  split_line[3]
                disks[disk_index]['partitions'][part_index]['file_system'] = split_line[4]
                disks[disk_index]['partitions'][part_index]['name'] = split_line[5]
                disks[disk_index]['partitions'][part_index]['flags'] = split_line[6].rstrip(';\n')


                part_index += 1

        get_disks_result = {
            'disk_data': disks,
            'num_disks': disk_index - raid_arrays,
            'num_raid_arrays': raid_arrays
        }

        return get_disks_result
