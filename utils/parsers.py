# utils/parsers.py

import re
from typing import Dict


# ============================================================
# STREAM
# ============================================================
def parse_stream(stdout: str) -> Dict[str, float]:
    metrics = {}
    pattern = r"^(Copy|Scale|Add|Triad)\s+([0-9.]+)\s+([A-Z]+/s)"
    for line in stdout.splitlines():
        m = re.match(pattern, line.strip())
        if m:
            name, value, unit = m.groups()
            value = float(value)
            if unit.startswith("MB"):
                value_gb = value / 1024.0
            elif unit.startswith("GB"):
                value_gb = value
            else:
                continue
            metrics[f"{name.lower()}_gbps"] = value_gb
    return metrics


# ============================================================
# HPL
# ============================================================
def parse_hpl(stdout: str) -> Dict[str, float]:
    metrics = {}
    pattern = r"WR11[^\s]*\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([0-9.]+E[+-]\d+)"
    for line in stdout.splitlines():
        m = re.search(pattern, line)
        if m:
            N, NB, P, Q, gflops = m.groups()
            metrics["N"] = int(N)
            metrics["NB"] = int(NB)
            metrics["P"] = int(P)
            metrics["Q"] = int(Q)
            metrics["gflops"] = float(gflops)
    return metrics


# ============================================================
# HPCG
# ============================================================
def parse_hpcg(stdout: str) -> Dict[str, float]:
    metrics = {}
    pattern = r"Final Summary::HPCG result is\s+([0-9.]+)"
    for line in stdout.splitlines():
        m = re.search(pattern, line)
        if m:
            metrics["gflops"] = float(m.group(1))
    return metrics


# ============================================================
# FIO
# ============================================================
def parse_fio(stdout: str) -> Dict[str, float]:
    metrics = {}
    rw_pattern = r"(READ|WRITE):.*bw=([0-9.]+)([KMG]?)i?B/s.*iops=([0-9.]+)([KMG]?)"
    unit_map = {"": 1, "K": 1e3, "M": 1e6, "G": 1e9}

    for line in stdout.splitlines():
        m = re.search(rw_pattern, line)
        if m:
            kind, bw, bw_unit, iops, iops_unit = m.groups()
            bw = float(bw) * unit_map.get(bw_unit, 1)
            iops_val = float(iops) * unit_map.get(iops_unit, 1)
            metrics[f"{kind.lower()}_bw_bytes_per_s"] = bw
            metrics[f"{kind.lower()}_iops"] = iops_val
    return metrics


# ============================================================
# iperf3
# ============================================================
def parse_iperf3(stdout: str) -> Dict[str, float]:
    """
    Parse iperf3 output and extract the summary bandwidth.
    Works for both single-stream and multi-stream (SUM) output.
    """
    metrics = {}

    # 1) Try SUM line (parallel streams)
    sum_pattern = r"

\[SUM\]

.* ([0-9.]+)\s+([KMG])bits/sec"
    for line in stdout.splitlines():
        m = re.search(sum_pattern, line)
        if m:
            val, unit = m.groups()
            val = float(val)
            if unit == "K":
                val *= 1e3
            elif unit == "M":
                val *= 1e6
            elif unit == "G":
                val *= 1e9
            metrics["bandwidth_bits_per_s"] = val
            return metrics

    # 2) Fallback: single-stream summary line
    single_pattern = r"

\[\s*\d+\]

.* ([0-9.]+)\s+([KMG])bits/sec"
    for line in stdout.splitlines():
        m = re.search(single_pattern, line)
        if m:
            val, unit = m.groups()
            val = float(val)
            if unit == "K":
                val *= 1e3
            elif unit == "M":
                val *= 1e6
            elif unit == "G":
                val *= 1e9
            metrics["bandwidth_bits_per_s"] = val
            return metrics

    return metrics


# ============================================================
# OSU Microbenchmarks (Bandwidth)
# ============================================================
def parse_osu_bw(stdout: str) -> Dict[str, float]:
    metrics = {}
    lines = [
        l for l in stdout.splitlines()
        if l.strip() and not l.startswith("#") and not l.lower().startswith("osu")
    ]
    if not lines:
        return metrics
    last = lines[-1].split()
    if len(last) >= 2:
        try:
            size = int(last[0])
            bw = float(last[-1])
            metrics["msg_size_bytes"] = size
            metrics["bandwidth_mb_per_s"] = bw
        except ValueError:
            pass
    return metrics


# ============================================================
# IOR
# ============================================================
def parse_ior(stdout: str) -> Dict[str, float]:
    metrics = {}
    pattern = r"(write|read).* ([0-9.]+)\s+MiB/s"
    for line in stdout.splitlines():
        m = re.search(pattern, line)
        if m:
            kind, bw = m.groups()
            metrics[f"{kind.lower()}_bw_mib_per_s"] = float(bw)
    return metrics


# ============================================================
# mdtest
# ============================================================
def parse_mdtest(stdout: str) -> Dict[str, float]:
    metrics = {}
    pattern = r"^(.*?):\s*([0-9.]+)\s+ops/sec"
    for line in stdout.splitlines():
        m = re.match(pattern, line.strip())
        if m:
            name, val = m.groups()
            key = name.lower().strip().replace(" ", "_")
            metrics[f"{key}_ops_per_s"] = float(val)
    return metrics


# ============================================================
# HPCC
# ============================================================
def parse_hpcc(stdout: str) -> Dict[str, float]:
    metrics = {}

    hpl_pattern = r"HPL.*Gflops\s*=\s*([0-9.]+)"
    m = re.search(hpl_pattern, stdout)
    if m:
        metrics["hpl_gflops"] = float(m.group(1))

    ptrans_pattern = r"PTRANS.*GBytes\s*/\s*s\s*=\s*([0-9.]+)"
    m = re.search(ptrans_pattern, stdout)
    if m:
        metrics["ptrans_gbytes_per_s"] = float(m.group(1))

    ra_pattern = r"RandomAccess.*GUPS\s*=\s*([0-9.]+)"
    m = re.search(ra_pattern, stdout)
    if m:
        metrics["randomaccess_gups"] = float(m.group(1))

    return metrics


# ============================================================
# IMB (PingPong)
# ============================================================
def parse_imb(stdout: str) -> Dict[str, float]:
    metrics = {}
    lines = [
        l for l in stdout.splitlines()
        if l.strip() and not l.strip().startswith("#") and not l.lower().startswith("imb")
    ]
    if not lines:
        return metrics

    last = lines[-1].split()
    if len(last) >= 4:
        try:
            size = int(last[0])
            t_usec = float(last[2])
            mbps = float(last[3])
            metrics["msg_size_bytes"] = size
            metrics["latency_usec"] = t_usec
            metrics["bandwidth_mbytes_per_s"] = mbps
        except ValueError:
            pass
    return metrics


# ============================================================
# NetPIPE
# ============================================================
def parse_netpipe(stdout: str) -> Dict[str, float]:
    metrics = {}
    max_bw = 0.0
    max_size = None

    for line in stdout.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 3:
            continue
        try:
            size = float(parts[0])
            bw = float(parts[-1])  # assume last column is Mb/s
        except ValueError:
            continue
        if bw > max_bw:
            max_bw = bw
            max_size = size

    if max_bw > 0:
        metrics["max_bandwidth_mbit_per_s"] = max_bw
        if max_size is not None:
            metrics["max_bandwidth_msg_size_bytes"] = max_size

    return metrics


# ============================================================
# lmbench (lat_mem_rd)
# ============================================================
def parse_lmbench(stdout: str) -> Dict[str, float]:
    metrics = {}
    last_latency = None

    for line in stdout.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        try:
            lat = float(parts[-1])
            last_latency = lat
        except ValueError:
            continue

    if last_latency is not None:
        metrics["latency_ns"] = last_latency

    return metrics


# ============================================================
# Graph500
# ============================================================
def parse_graph500(stdout: str) -> Dict[str, float]:
    metrics = {}
    pattern = r"TEPS[:\s]+([0-9.eE+-]+)"
    m = re.search(pattern, stdout)
    if m:
        metrics["teps"] = float(m.group(1))
    return metrics
