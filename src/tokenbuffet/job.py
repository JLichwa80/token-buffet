"""Windows job object holding every Token Buffet process and whatever those processes spawn.

`tbuffet start` joins the job before launching services, so proxies, router, dashboard and the provider CLIs they run all
belong to it; `tbuffet stop --force` terminates the job by name.
"""
import ctypes
from ctypes import wintypes

NAME = "TokenBuffetServices"
JOB_OBJECT_ALL_ACCESS = 0x1F001F
JOB_OBJECT_LIMIT_BREAKAWAY_OK = 0x800
JobObjectExtendedLimitInformation = 9
CREATE_BREAKAWAY_FROM_JOB = 0x01000000


class _BasicLimits(ctypes.Structure):
    _fields_ = [("PerProcessUserTimeLimit", ctypes.c_int64), ("PerJobUserTimeLimit", ctypes.c_int64),
                ("LimitFlags", wintypes.DWORD), ("MinimumWorkingSetSize", ctypes.c_size_t),
                ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", wintypes.DWORD),
                ("Affinity", ctypes.c_size_t), ("PriorityClass", wintypes.DWORD), ("SchedulingClass", wintypes.DWORD)]


class _IoCounters(ctypes.Structure):
    _fields_ = [(name, ctypes.c_uint64) for name in (
        "ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
        "ReadTransferCount", "WriteTransferCount", "OtherTransferCount")]


class _ExtendedLimits(ctypes.Structure):
    _fields_ = [("BasicLimitInformation", _BasicLimits), ("IoInfo", _IoCounters),
                ("ProcessMemoryLimit", ctypes.c_size_t), ("JobMemoryLimit", ctypes.c_size_t),
                ("PeakProcessMemoryUsed", ctypes.c_size_t), ("PeakJobMemoryUsed", ctypes.c_size_t)]

_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
_kernel32.CreateJobObjectW.argtypes = [wintypes.LPVOID, wintypes.LPCWSTR]
_kernel32.CreateJobObjectW.restype = wintypes.HANDLE
_kernel32.OpenJobObjectW.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR]
_kernel32.OpenJobObjectW.restype = wintypes.HANDLE
_kernel32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
_kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
_kernel32.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
_kernel32.TerminateJobObject.restype = wintypes.BOOL
_kernel32.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD]
_kernel32.SetInformationJobObject.restype = wintypes.BOOL
_kernel32.GetCurrentProcess.restype = wintypes.HANDLE
_kernel32.CloseHandle.argtypes = [wintypes.HANDLE]


def join():
    """Put this process in the named job (created if missing); children it starts afterwards inherit membership."""
    job = _kernel32.CreateJobObjectW(None, NAME)
    if not job:
        raise ctypes.WinError(ctypes.get_last_error())
    limits = _ExtendedLimits()
    limits.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_BREAKAWAY_OK  # lets apps launch outside the job
    if not _kernel32.SetInformationJobObject(job, JobObjectExtendedLimitInformation, ctypes.byref(limits), ctypes.sizeof(limits)):
        raise ctypes.WinError(ctypes.get_last_error())
    if not _kernel32.AssignProcessToJobObject(job, _kernel32.GetCurrentProcess()):
        raise ctypes.WinError(ctypes.get_last_error())
    # The handle stays open until this process exits; the job lives on while any member process runs.


def terminate():
    """Kill every process in the named job; returns False when no such job exists."""
    job = _kernel32.OpenJobObjectW(JOB_OBJECT_ALL_ACCESS, False, NAME)
    if not job:
        return False
    try:
        if not _kernel32.TerminateJobObject(job, 1):
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        _kernel32.CloseHandle(job)
    return True
