"""
Disks Service

This service exposes information about hard disks in the system.

"""
import subprocess

from server.command_center.services import utils


class DiskService():

    def get_disks(self):


        #*********************************************************
        # Part 1: Get the device file and 'name' for each disk   *
        #*********************************************************

        # Read in command output by line.
        ls_command = subprocess.Popen('ls -lahrt /dev', stdout=subprocess.PIPE, shell=True)
        grep_command = subprocess.Popen('grep "[shm]d.$"', stdin=ls_command.stdout, stdout=subprocess.PIPE, shell=True)
        devices_by_line = grep_command.communicate()[0].split('\n')



        disks = []       # our list of disks
        disk_index = 0   # current 'disk' index (independent of line)
        raid_arrays = 0  # number of raid arrays we find
        for line in devices_by_line:
            if line is '':
                continue
            split_line = line.split()
            device_file = split_line[len(split_line) -1]

            disks.append({})
            disks[disk_index]['device_file'] = '/dev/' + device_file
            disks[disk_index]['device_name'] = device_file

            if 'md' in device_file:
                raid_arrays += 1

            disk_index += 1


        #*********************************************************
        # Part 2: Get udisks info for each disk                  *
        #*********************************************************

        for disk in disks:
            udisks_command = 'udisks --show-info ' + disk['device_file']
            udisks_by_line = utils.get_command_output_by_line(self, udisks_command)

            disk['raid_info'] = {}

            # Iterate on the udisks output, grabbing information
            for line in udisks_by_line:
                # Smart data is a the bottom of the output, delimited by lines of equal signs. Ignore that for now,
                # when we reach a line of equal signs, we're done.
                if '====================' in line:
                    break

                # All of the lines we care about are in the form:
                #  name:  value
                # So, we split by colon and discard lines that don't split into 2
                split_line = line.split(':', 1)
                if len(split_line) < 2:
                    continue

                # Strip whitespace from value only, we'd like to keep the indentation before the name.
                name = split_line[0]
                value = split_line[1].strip()

                if 'native-path' in name:
                    disk['native_path'] = value

                elif '  size' == name:
                    disk['size'] = value
                    human_size = int(value) / 1000000000
                    human_size = str(human_size) + "GB"
                    disk['human_size'] = human_size

                elif 'block size' in name:
                    disk['block_size'] = value

                elif 'usage' in name:
                    if value == 'raid':
                        disk['is_raid_member'] = True
                    else:
                        disk['is_raid_member'] = False
                    disk['usage'] = value

                elif 'type' in name:
                    disk['type'] = value

                elif 'RAID level' in name:
                    disk['raid_info']['level'] = value

                elif 'position' in name:
                    disk['raid_info']['position'] = value

                elif 'num components' in name:
                    disk['raid_info']['num_components'] = value

                elif 'version' in name and disk['is_raid_member'] == True:
                    disk['raid_info']['version'] = value

                elif 'holder' in name:
                    split_holder = value.split('/')
                    if len(split_holder) > 2:
                        holder = '/dev/' + split_holder[len(split_holder) - 1]
                        disk['raid_info']['holder'] = holder

                elif 'model' in name:
                    disk['model'] = value

                elif 'revision' in name:
                    disk['revision'] = value

                elif 'serial' in name:
                    disk['serial'] = value

                elif 'can spindown' in name:
                    disk['can_spindown'] = value

                elif 'rotational media' in name:
                    disk['rotational_media'] = value

                elif 'interface' in name:
                    disk['interface'] = value

                elif 'if speed' in name:
                    disk['if_speed'] = value

                elif 'overall assessment' in name:
                    disk['smart'] = value

                elif 'count' in name:
                    disk['partition_count'] = int(value)

            if disk.get('partition_count') is None:
                disk['partition_count'] = 0


        #*********************************************************
        # Part 3: Get partition info for each disk               *
        #*********************************************************

        # Get all info from df
        df_by_line = utils.get_command_output_by_line(self, 'df -h')

        for disk in disks:
            if disk['partition_count'] < 1:
                continue


            ls_command = subprocess.Popen('ls -lahrt /dev', stdout=subprocess.PIPE, shell=True)
            cmd = 'egrep "' + disk['device_name'] + 'p?[0-9]$"'
            grep_command = subprocess.Popen(cmd, stdin=ls_command.stdout, stdout=subprocess.PIPE, shell=True)
            partitions_by_line = grep_command.communicate()[0].split('\n')

            partitions = []       # our list of partitions
            partition_index = 0   # current 'partition' index (independent of line)
            for line in partitions_by_line:
                if line is '':
                    continue
                split_line = line.split()
                device_file = split_line[len(split_line) -1]

                partitions.append({})
                partitions[partition_index]['device_file'] = '/dev/' + device_file
                partitions[partition_index]['device_name'] = device_file
                partition_index += 1

            disk['partitions'] = partitions


            for partition in disk['partitions']:

                udisks_command = 'udisks --show-info ' + partition['device_file']
                udisks_by_line = utils.get_command_output_by_line(self, udisks_command)

                for line in udisks_by_line:
                    # TODO: following 10 lines copied from above, new method candidate.
                    # All of the lines we care about are in the form:
                    #  name:  value
                    # So, we split by colon and discard lines that don't split into 2
                    split_line = line.split(':', 1)
                    if len(split_line) < 2:
                        continue

                    # Strip whitespace from value only, we'd like to keep the indentation before the name.
                    name = split_line[0]
                    value = split_line[1].strip()

                    if 'is read only' in name:
                        is_read_only = False
                        if value == "1":
                            is_read_only = True
                        partition['is_read_only'] = is_read_only

                    elif 'is mounted' in name:
                        is_mounted = False
                        if value == "1":
                            is_mounted = True
                        partition['is_mounted'] = is_mounted

                    elif 'mount paths' in name:
                        partition['mount_paths'] = value

                    elif 'block size' in name:
                        partition['block_size'] = value

                    elif 'usage' in name:
                        partition['usage'] = value

                    elif 'type' in name and name == '  type':
                        partition['type'] = value

                    elif 'label' in name and name == '  label':
                        partition['label'] = value

                    elif 'number' in name:
                        partition['number'] = value

                for line in df_by_line:
                    split_line = line.split()
                    device_file = split_line[0].strip()

                    if device_file == partition['device_file']:
                        size = split_line[1].strip()
                        used = split_line[2].strip()
                        available = split_line[3].strip()
                        used_percent = split_line[4].strip()

                        partition['size'] = size
                        partition['used'] = used
                        partition['available'] = available
                        partition['used_percent'] = used_percent



        get_disks_result = {
            'disk_data': disks,
            'num_disks': disk_index - raid_arrays,
            'num_raid_arrays': raid_arrays
        }

        return get_disks_result
