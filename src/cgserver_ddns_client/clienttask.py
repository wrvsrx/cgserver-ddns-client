from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import distro
import os
import platform
import psutil
import psutil._common
import pynvml
import time

from pprint import pprint


def disk_usage(path):
    try:
        return psutil.disk_usage(path)
    except PermissionError:
        return psutil._common.sdiskusage(0, 0, 0, 0)


def get_utilization_rates(handle):
    try:
        return dict(
            gpu=pynvml.nvmlDeviceGetUtilizationRates(handle).gpu,
            memory=pynvml.nvmlDeviceGetUtilizationRates(handle).memory,
        )
    except pynvml.NVMLError_Unknown:  # type: ignore
        return dict(
            gpu=None,
            memory=None,
        )


def get_fan_speed(handle):
    try:
        return pynvml.nvmlDeviceGetFanSpeed(handle)
    except pynvml.NVMLError_NotSupported:  # type: ignore
        return None


def gputask():
    def get(index):
        try:
            handle = pynvml.nvmlDeviceGetHandleByIndex(index)
        except pynvml.NVMLError_GpuIsLost:  # type: ignore
            return None
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        return dict(
            nvmlDeviceGetName=pynvml.nvmlDeviceGetName(handle),
            nvmlDeviceGetMemoryInfo=dict(
                total=memory_info.total,
                free=memory_info.free,
                used=memory_info.used,
            ),
            nvmlDeviceGetUtilizationRates=get_utilization_rates(handle),
            nvmlDeviceGetFanSpeed=get_fan_speed(handle),
            nvmlDeviceGetTemperature=pynvml.nvmlDeviceGetTemperature(
                handle, pynvml.NVML_TEMPERATURE_GPU
            ),
            nvmlDeviceGetTemperatureThreshold=dict(
                slowdown=pynvml.nvmlDeviceGetTemperatureThreshold(
                    handle, pynvml.NVML_TEMPERATURE_THRESHOLD_SLOWDOWN
                ),
                shutdown=pynvml.nvmlDeviceGetTemperatureThreshold(
                    handle, pynvml.NVML_TEMPERATURE_THRESHOLD_SHUTDOWN
                ),
            ),
            nvmlDeviceGetPowerManagementLimit=pynvml.nvmlDeviceGetPowerManagementLimit(
                handle
            ),
            nvmlDeviceGetPowerUsage=pynvml.nvmlDeviceGetPowerUsage(handle),
        )

    try:
        pynvml.nvmlInit()
        res = dict(
            nvml_version=pynvml.nvmlSystemGetDriverVersion(),
            nvmlDeviceGetCount=pynvml.nvmlDeviceGetCount(),
            nvmlDevices=[get(i) for i in range(pynvml.nvmlDeviceGetCount())],
        )
        pynvml.nvmlShutdown()
    except pynvml.NVMLError as error:
        print(error)
        return dict(
            nvml_version=None,
        )

    return res


def alltasks():
    res = dict(
        version="0.1.3",
        platform=platform.platform(),
        uname=platform.uname(),
        dist=distro.linux_distribution(),
        now=time.time(),
        boot_time=psutil.boot_time(),
        loadavg=hasattr(os, "getloadavg") and os.getloadavg() or None,
        cpu_count_logical=psutil.cpu_count(logical=True),
        cpu_count_physical=psutil.cpu_count(logical=False),
        cpu_freq=psutil.cpu_freq(),
        cpu_percent=psutil.cpu_percent(),
        cpu_stats=psutil.cpu_stats(),
        cpu_times=psutil.cpu_times(),
        cpu_times_percent=psutil.cpu_times_percent(),
        disk_io_counters=psutil.disk_io_counters(),
        disk_partitions=psutil.disk_partitions(),
        disk_usage=[disk_usage(part.mountpoint) for part in psutil.disk_partitions()],
        net_if_addrs=psutil.net_if_addrs(),
        net_if_stats=psutil.net_if_stats(),
        net_io_counters=psutil.net_io_counters(),
        swap_memory=psutil.swap_memory(),
        users=psutil.users(),
        virtual_memory=psutil.virtual_memory(),
    )
    res.update(gputask())
    return res


def dump_info():
    print(alltasks())


if __name__ == "__main__":
    dump_info()
