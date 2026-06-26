#!/usr/bin/env python3
"""
Workspace inventory and git-history helpers for the session usage report.
"""
import os
import subprocess
from collections import Counter


def get_recent_commits(repo_path, days):
    """Get categorized commits from git log."""
    try:
        output = subprocess.check_output(
            ["git", "-C", repo_path, "log", f"--since={days} days ago", "--oneline", "--all"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {}

    categories = Counter()
    for line in output.strip().split("\n"):
        if not line:
            continue
        message = line.split(" ", 1)[-1].lower()
        if any(keyword in message for keyword in ["story", "epic"]):
            categories["SDC (Story/Epic)"] += 1
        elif "squad" in message:
            categories["Squad"] += 1
        elif "sinkra" in message:
            categories["SINKRA"] += 1
        elif "synapse" in message:
            categories["Synapse"] += 1
        elif "heuristic" in message:
            categories["Heuristics"] += 1
        elif any(keyword in message for keyword in ["yaml", "ci", "lint", "ci/"]):
            categories["CI/Infra"] += 1
        elif any(keyword in message for keyword in ["mmos", "mind", "an_ke", "pv_pa"]):
            categories["MMOS/Minds"] += 1
        elif "doctor" in message:
            categories["Doctor"] += 1
        else:
            categories["Other"] += 1

    return dict(categories.most_common())


def discover_inventory(project_root):
    """Discover available skills, agents, and skill groups."""
    inventory = {"skills": [], "agents": [], "skill_groups": {}}

    skills_dir = os.path.join(project_root, ".claude", "skills")
    if os.path.isdir(skills_dir):
        for entry in sorted(os.listdir(skills_dir)):
            if os.path.isdir(os.path.join(skills_dir, entry)):
                inventory["skills"].append(entry)
                group = entry.split("-", 1)[0]
                inventory["skill_groups"][group] = inventory["skill_groups"].get(group, 0) + 1

    agents_dir = os.path.join(project_root, ".claude", "agents")
    if os.path.isdir(agents_dir):
        for entry in sorted(os.listdir(agents_dir)):
            if entry.endswith(".md"):
                inventory["agents"].append(entry.replace(".md", ""))

    return inventory
