/***
 * A Collection of Utilities to assist in the displaying of disk data.
 * Original intended consumer: disks.js
 *
 * A disk looks like:
 *
    {
      "device_file": "/dev/sdd",
      "partition_count": 1,
      "human_size": "320GB",
      "revision": "01.03E10",
      "interface": "ata",
      "partitions": [
        {
          "device_file": "/dev/sdd1",
          "available": "265G",
          "used": "14G",
          "number": "1",
          "used_percent": "5%",
          "label": "small1",
          "device_name": "sdd1",
          "is_mounted": true,
          "is_read_only": false,
          "mount_paths": "/media/small1",
          "usage": "filesystem",
          "block_size": "512",
          "type": "ext4",
          "size": "294G"
        }
      ],
      "is_raid_member": false,
      "device_name": "sdd",
      "rotational_media": "Yes, unknown rate",
      "can_spindown": "1",
      "native_path": "/sys/devices/pci0000:00/0000:00:05.0/0000:02:00.0/ata6/host5/target5:0:0/5:0:0:0/block/sdd",
      "raid_info": {},
      "usage": "",
      "if_speed": "(unknown)",
      "model": "WDC WD3200AAJS-65M0A0",
      "block_size": "512",
      "type": "",
      "serial": "WD-WMAV2H741194",
      "smart": "Good",
      "size": "320072933376"
    }
 *
 */
"use strict";

function isSSD(disk) {
    if(disk.rotational_media.indexOf('Yes') !== -1) {
        return false;
    }
    return true;
}

function isRaidDevice(disk) {
    if(disk.device_name.indexOf('md') !== -1) {
        return true;
    }
    return false;
}