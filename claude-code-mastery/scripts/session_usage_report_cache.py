#!/usr/bin/env python3
"""
Cache and session-meta helpers for the session usage report.

The main script keeps the public API and injects patchable callbacks from its
own module so tests can continue monkeypatching there.
"""
import hashlib
import json
import os
import sys
from collections import Counter
from datetime import datetime


def ensure_dir(path):
    """Create a directory tree when missing."""
    os.makedirs(path, exist_ok=True)
    return path


def get_cache_paths(cache_root=None, default_usage_data_dir=None):
    """Resolve cache locations used by the report."""
    root = os.path.expanduser(cache_root or default_usage_data_dir or "")
    return {
        "root": root,
        "session_meta": os.path.join(root, "session-meta"),
        "facets": os.path.join(root, "facets"),
    }


def file_fingerprint(session_file):
    """Stable fingerprint for cache invalidation."""
    stat_result = os.stat(session_file)
    return {
        "size": stat_result.st_size,
        "mtime_ns": stat_result.st_mtime_ns,
    }


def cache_key_for_file(session_file):
    """Derive a stable cache key from the absolute session path."""
    absolute_path = os.path.abspath(session_file)
    return hashlib.sha1(absolute_path.encode("utf-8")).hexdigest()


def load_session_entries(session_file):
    """Read a JSONL transcript while tolerating malformed lines."""
    raw_entries = []
    with open(session_file, "r", errors="replace") as file_handle:
        for line in file_handle:
            line = line.strip()
            if not line:
                continue
            try:
                raw_entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return raw_entries


def select_session_branch(raw_entries, select_dominant_session_fn, build_selected_branch_fn):
    """Resolve the dominant session and its strongest branch."""
    dominant_session_id = select_dominant_session_fn(raw_entries)
    selected_branch, branch_count = build_selected_branch_fn(raw_entries, dominant_session_id)
    if not selected_branch:
        if dominant_session_id:
            selected_branch = [
                entry for entry in raw_entries
                if entry.get("sessionId") == dominant_session_id
            ]
        else:
            selected_branch = list(raw_entries)
        if selected_branch and branch_count == 0:
            branch_count = 1
    return dominant_session_id, selected_branch, branch_count


def serialize_session_result(result, counter_fields, set_fields):
    """Convert in-memory session analysis into JSON-safe structures."""
    serialized = {}
    for key, value in result.items():
        if key in counter_fields:
            serialized[key] = dict(value)
        elif key in set_fields:
            serialized[key] = sorted(value)
        else:
            serialized[key] = value
    return serialized


def deserialize_session_result(payload, counter_fields, set_fields):
    """Restore Counters/sets from cached JSON payloads."""
    result = dict(payload)
    for key in counter_fields:
        result[key] = Counter(result.get(key, {}))
    for key in set_fields:
        result[key] = set(result.get(key, []))
    return result


def read_cached_json(cache_file):
    """Load a cache file, returning None on corruption or absence."""
    try:
        with open(cache_file, "r", encoding="utf-8") as file_handle:
            return json.load(file_handle)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def write_cached_json(cache_file, payload, cache_warning_paths=None):
    """Persist a cache file as formatted JSON."""
    try:
        ensure_dir(os.path.dirname(cache_file))
        with open(cache_file, "w", encoding="utf-8") as file_handle:
            json.dump(payload, file_handle, indent=2, ensure_ascii=False)
        return True
    except OSError as exc:
        warning_key = os.path.dirname(cache_file)
        if cache_warning_paths is not None and warning_key not in cache_warning_paths:
            cache_warning_paths.add(warning_key)
            print(f"  Warning: unable to write cache {cache_file}: {exc}", file=sys.stderr)
        return False


def get_session_meta(
    session_file,
    analyze_session_fn,
    default_usage_data_dir,
    counter_fields,
    set_fields,
    cache_warning_paths,
    cache_root=None,
    use_cache=True,
    refresh_cache=False,
):
    """Load session meta from cache or compute it from the transcript."""
    fingerprint = file_fingerprint(session_file)
    cache_paths = get_cache_paths(cache_root, default_usage_data_dir)
    cache_file = os.path.join(cache_paths["session_meta"], f"{cache_key_for_file(session_file)}.json")

    if use_cache and not refresh_cache:
        cached = read_cached_json(cache_file)
        if cached and cached.get("fingerprint") == fingerprint:
            result = deserialize_session_result(cached.get("result", {}), counter_fields, set_fields)
            return result, "hit"

    result = analyze_session_fn(session_file)

    if use_cache:
        write_cached_json(
            cache_file,
            {
                "version": 1,
                "session_file": os.path.abspath(session_file),
                "fingerprint": fingerprint,
                "generated_at": datetime.now().isoformat(),
                "result": serialize_session_result(result, counter_fields, set_fields),
            },
            cache_warning_paths=cache_warning_paths,
        )

    return result, "miss"
