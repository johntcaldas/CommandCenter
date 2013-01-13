"""
Disks Service

This service exposes information about hard disks in the system.

Note on permissions:
--------------------------
This is the first service (in order of code creation) requiring 'root' access to run commands on the host machine
(eg. sudo parted -lms). For now, I added:
    jcaldas ALL=(ALL) NOPASSWD: ALL
using 'visudo'. Eventually this application will be run as a web server user and it will probably make sense to
give only access to specific commands.

Info on fine grained command control for sudoers:
http://ubuntuforums.org/showthread.php?p=7118727#post7118727


Note on methods:
--------------------------
There are certainly way better ways to get this information that what we are doing here (using dbus for example). A good
exercise would be to come back here and rip out the brute force and brittle shelling out + looping. This message is an
acknowledgment of the inelegance contained in this class.
"""
import utils
import re

class DiskService():

    def get_disks(self):
        """
        Use 'sudo parted -lms' to get the list of disks on the system. Expand this information with 'sudo udisks --dump'
        to give a fuller picture of the disk situation.

        Sample parted output:
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

        Sample udisks --dump output (single device):
        ========================================================================
        Showing information for /org/freedesktop/UDisks/devices/sdd
          native-path:                 /sys/devices/pci0000:00/0000:00:05.0/0000:02:00.0/ata6/host5/target5:0:0/5:0:0:0/block/sdd
          device:                      8:48
          device-file:                 /dev/sdd
            presentation:              /dev/sdd
            by-id:                     /dev/disk/by-id/ata-WDC_WD3200AAJS-65M0A0_WD-WMAV2H741194
            by-id:                     /dev/disk/by-id/scsi-SATA_WDC_WD3200AAJS-_WD-WMAV2H741194
            by-id:                     /dev/disk/by-id/wwn-0x50014ee0019f4d48
            by-path:                   /dev/disk/by-path/pci-0000:02:00.0-scsi-0:0:0:0
          detected at:                 Thu 27 Dec 2012 08:19:19 PM EST
          system internal:             1
          removable:                   0
          has media:                   1 (detected at Thu 27 Dec 2012 08:19:19 PM EST)
            detects change:            0
            detection by polling:      0
            detection inhibitable:     0
            detection inhibited:       0
          is read only:                0
          is mounted:                  0
          mount paths:
          mounted by uid:              0
          presentation hide:           0
          presentation nopolicy:       0
          presentation name:
          presentation icon:
          automount hint:
          size:                        320072933376
          block size:                  512
          job underway:                no
          usage:
          type:
          version:
          uuid:
          label:
          partition table:
            scheme:                    gpt
            count:                     1
          drive:
            vendor:                    ATA
            model:                     WDC WD3200AAJS-65M0A0
            revision:                  01.03E10
            serial:                    WD-WMAV2H741194
            WWN:                       50014ee0019f4d48
            detachable:                0
            can spindown:              1
            rotational media:          Yes, unknown rate
            write-cache:               enabled
            ejectable:                 0
            adapter:                   Unknown
            ports:
            similar devices:
            media:
              compat:
            interface:                 ata
            if speed:                  (unknown)
            ATA SMART:                 Updated at Sat 29 Dec 2012 09:19:19 PM EST
              overall assessment:      Good
        ===============================================================================
         Attribute       Current|Worst|Threshold  Status   Value       Type     Updates
        ===============================================================================
         raw-read-error-rate         200|200| 51   good    0           Pre-fail Online
         spin-up-time                171|139| 21   good    2.4 secs    Pre-fail Online
         start-stop-count            100|100|  0    n/a    906         Old-age  Online
         reallocated-sector-count    200|200|140   good    0 sectors   Pre-fail Online
         seek-error-rate             200|200|  0    n/a    0           Old-age  Online
         power-on-hours               81| 81|  0    n/a    578.0 days  Old-age  Online
         spin-retry-count            100|100|  0    n/a    0           Old-age  Online
         calibration-retry-count     100|100|  0    n/a    0           Old-age  Online
         power-cycle-count           100|100|  0    n/a    499         Old-age  Online
         power-off-retract-count     200|200|  0    n/a    281         Old-age  Online
         load-cycle-count            200|200|  0    n/a    906         Old-age  Online
         temperature-celsius-2       115| 91|  0    n/a    28C / 82.4F Old-age  Online
         reallocated-event-count     200|200|  0    n/a    0           Old-age  Online
         current-pending-sector      200|200|  0    n/a    0 sectors   Old-age  Online
         offline-uncorrectable       200|200|  0    n/a    0 sectors   Old-age  Offline
         udma-crc-error-count        200|200|  0    n/a    1           Old-age  Online
         multi-zone-error-rate       200|200|  0    n/a    0           Old-age  Offline

        ========================================================================
        Showing information for /org/freedesktop/UDisks/devices/sdd1
          native-path:                 /sys/devices/pci0000:00/0000:00:05.0/0000:02:00.0/ata6/host5/target5:0:0/5:0:0:0/block/sdd/sdd1
          device:                      8:49
          device-file:                 /dev/sdd1
            presentation:              /dev/sdd1
            by-id:                     /dev/disk/by-id/ata-WDC_WD3200AAJS-65M0A0_WD-WMAV2H741194-part1
            by-id:                     /dev/disk/by-id/scsi-SATA_WDC_WD3200AAJS-_WD-WMAV2H741194-part1
            by-id:                     /dev/disk/by-id/wwn-0x50014ee0019f4d48-part1
            by-id:                     /dev/disk/by-uuid/316ef770-9976-476c-b282-f16aea0afbbd
            by-path:                   /dev/disk/by-path/pci-0000:02:00.0-scsi-0:0:0:0-part1
          detected at:                 Thu 27 Dec 2012 08:19:19 PM EST
          system internal:             1
          removable:                   0
          has media:                   1 (detected at Thu 27 Dec 2012 08:19:19 PM EST)
            detects change:            0
            detection by polling:      0
            detection inhibitable:     0
            detection inhibited:       0
          is read only:                0
          is mounted:                  1
          mount paths:             /media/small1
          mounted by uid:              0
          presentation hide:           0
          presentation nopolicy:       0
          presentation name:
          presentation icon:
          automount hint:
          size:                        320071532544
          block size:                  512
          job underway:                no
          usage:                       filesystem
          type:                        ext4
          version:                     1.0
          uuid:                        316ef770-9976-476c-b282-f16aea0afbbd
          label:                       small1
          partition:
            part of:                   /org/freedesktop/UDisks/devices/sdd
            scheme:                    gpt
            number:                    1
            type:                      EBD0A0A2-B9E5-4433-87C0-68B6B72699C7
            flags:
            offset:                    1048576
            alignment offset:          0
            size:                      320071532544
            label:
            uuid:                      C1666775-3F78-4EB4-8A52-1742733417D5

        ========================================================================


        We want to cluster the line starting with '/dev/' with each following line until we reach a blank line. This
        will represent the information we have about a single disk.


        """

        #*********************************************************
        # Part 1: get disk information from parted               *
        #*********************************************************

        # Read in command output by line.
        disks_by_line = utils.get_command_output_by_line(self,'sudo parted -lms')


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



        #*********************************************************
        # Part 2: Augment the parted info with info from udisks. *
        #*********************************************************
        udisks_by_line = utils.get_command_output_by_line(self, 'sudo udisks --dump')


        udisks_by_disk = []
        udisks_index = -1
        first = False
        in_smart = False
        in_smart_separator_count = 0
        line_index = -1
        for line in udisks_by_line:
            line_index += 1
            if "===========================" in line:
                # For now, skip smart data blocks. We identify these because of a header delimited by lines of '='
                if in_smart:
                    in_smart_separator_count += 1
                    if in_smart_separator_count == 2:
                        in_smart_separator_count = 0
                        in_smart = False
                        first = True
                elif len(udisks_by_line) > line_index + 2 and \
                     "===========================" in udisks_by_line[line_index + 2]:
                    in_smart = True
                    continue
                else:
                    matching_disk_index = None
                    first = True
                continue
            elif in_smart:
                continue
            elif line == '':
                continue
            elif first is True:
                first = False
                udisks_index += 1
                udisks_by_disk.append({})



            # show example resulting string after this block.                     !!!!!!!!!!!!!!! LOOK FOOL
            name_value = line.split(':', 1)

            # For now, ignore all lines that don't have a colon
            if len(name_value) < 2:
                continue

            name_value[0] = name_value[0].strip()
            name_value[1] = name_value[1].strip()

            udisks_by_disk[udisks_index][name_value[0]] = name_value[1]

        for udisk in udisks_by_disk:
            # Figure out if this is a partition (patch that device-file ends with p followed by a digit.
            # Also get disk id, and partition # if it is a partition
            is_partition = False
            disk_dev_file = ""
            partition_num = None
            match_obj = re.search("p\d$", udisk['device-file'])
            if match_obj:
                is_partition = True
                split_device_file = udisk['device-file'].split('p')
                disk_dev_file = split_device_file[0]
                partition_num = split_device_file[1]
            else:
                disk_dev_file = udisk['device-file']

            # Figure out matching disk and partition indices in the disks[] structure created above (parted section)
            disk_index = 0
            found = False
            for disk in disks:
                if disk["device"] == disk_dev_file:
                    found = True
                    break
                disk_index += 1
            if not found:
                continue

            if is_partition:
                pass
            else:
                # Copy information into disks[] structure
                disks[disk_index]['native_path'] = udisk['native-path']
                disks[disk_index]['is_mounted'] = udisk['is mounted']
                disks[disk_index]['mount_paths'] = udisk['mount paths']
                disks[disk_index]['mounted_by_uid'] = udisk['mounted by uid']
                disks[disk_index]['usage'] = udisk['usage']
                disks[disk_index]['type'] = udisk['type']
                disks[disk_index]['label'] = udisk['label']










        get_disks_result = {
            'disk_data': disks,
            'num_disks': disk_index - raid_arrays,
            'num_raid_arrays': raid_arrays
        }

        return get_disks_result
