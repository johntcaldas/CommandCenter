"""
Procfs Service

This service interfaces with the linux procfs API. More specifically, the library 'procfs' does that for us. This
service-layer module wraps procfs and creates python dictionaries with useful info we're interested in.

Procfs documentation:
http://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/tree/Documentation/filesystems/proc.txt
"""

from procfs import Proc
import datetime

class ProcService():

    def __init__(self):
        self.proc_fs = Proc()

    def get_summary(self):
        ret = {
            'memory_info': self.get_mem_info(),
            'up_time': self.get_uptime()
        }

        return ret

    def get_mem_info(self):
        p_meminfo = self.proc_fs.meminfo

        meminfo = {
            # MemTotal: Total usable ram (i.e. physical ram minus a few reserved bits and the kernel binary code)
            'total_mb': p_meminfo.MemTotal,
            # MemFree: The sum of LowFree+HighFree
            'free_mb': p_meminfo.MemFree,
            # Buffers: Relatively temporary storage for raw disk blocks
            # shouldn't get tremendously large (20MB or so)
            'buffers_mb': p_meminfo.Buffers,
            # Cached: in-memory cache for files read from the disk (the
            # pagecache).  Doesn't include SwapCached
            'cached_mb': p_meminfo.Cached
        }

        # All memory values come to us in kilobytes, we convert to megabytes
        megabyte_multiplier = 0.000976563
        for k, v in meminfo.iteritems():
            meminfo[k] = v * megabyte_multiplier

        # Add in values to report for 'real' used and free (the -/+ buffers/cache line in linux free).
        # Most system monitoring tools report this value.
        meminfo['free_plus_cached_mb'] = meminfo['free_mb'] + meminfo['buffers_mb'] + meminfo['cached_mb']
        meminfo['used_minus_cached_mb'] = meminfo['total_mb'] - meminfo['free_plus_cached_mb']

        return meminfo

    def get_uptime(self):
        """
        Will come to us in the form:
        {'idle': datetime.timedelta(0, 110, 640000),
         'uptime': datetime.timedelta(0, 24264, 850000)}
        """
        p_uptime = self.proc_fs.uptime
        ret = {
            'idle_seconds': p_uptime.idle.total_seconds(),
            'uptime_seconds': p_uptime.uptime.total_seconds()
        }

        return ret