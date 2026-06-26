#!/usr/bin/env python3
"""
Tests for session-usage-report.py

Covers: short_name, analyze_session, get_recent_commits, discover_inventory,
        generate_report, format_markdown, normalize_skill dedup, CLI args.
"""
import json
import os
import sys
import tempfile
import shutil
import subprocess
import textwrap
import unittest
from collections import Counter, defaultdict
from unittest.mock import patch

# ── Import the module under test ──────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
import importlib
report_mod = importlib.import_module("session-usage-report")

short_name = report_mod.short_name
find_projects = report_mod.find_projects
analyze_session = report_mod.analyze_session
get_recent_commits = report_mod.get_recent_commits
discover_inventory = report_mod.discover_inventory
generate_report = report_mod.generate_report
format_markdown = report_mod.format_markdown
format_html = report_mod.format_html
get_session_meta = report_mod.get_session_meta
generate_workflow_recommendations = report_mod.generate_workflow_recommendations
build_transcript_excerpt = report_mod.build_transcript_excerpt
BUILTIN_COMMANDS = report_mod.BUILTIN_COMMANDS


class TestShortName(unittest.TestCase):
    """Unit tests for short_name()."""

    def test_oalanicolas_prefix(self):
        path = "/tmp/.claude/projects/-Users-userA-Code-sinkra-hub"
        self.assertEqual(short_name(path), "sinkra-hub")

    def test_alan_prefix(self):
        path = "/tmp/.claude/projects/-Users-userB-Code-aiox-stage"
        self.assertEqual(short_name(path), "aiox-stage")

    def test_generic_users_prefix(self):
        path = "/tmp/.claude/projects/-Users-john"
        self.assertEqual(short_name(path), "john")

    def test_no_known_prefix(self):
        path = "/tmp/.claude/projects/my-project"
        self.assertEqual(short_name(path), "my-project")

    def test_nested_code_path(self):
        path = "/x/-Users-userA-Code-aiox-stage-apps-site-aiox"
        self.assertEqual(short_name(path), "aiox-stage-apps-site-aiox")


class TestAnalyzeSession(unittest.TestCase):
    """Unit tests for analyze_session()."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _write_jsonl(self, filename, entries):
        path = os.path.join(self.tmpdir, filename)
        with open(path, "w") as f:
            for entry in entries:
                f.write(json.dumps(entry) + "\n")
        return path

    def test_empty_file(self):
        path = self._write_jsonl("empty.jsonl", [])
        result = analyze_session(path)
        self.assertFalse(result["is_headless"])
        self.assertEqual(len(result["slash_commands"]), 0)
        self.assertEqual(len(result["skill_invocations"]), 0)
        self.assertEqual(len(result["agent_types"]), 0)
        self.assertEqual(len(result["shell_runners"]), 0)

    def test_detects_headless_session(self):
        entries = [
            {"message": {"type": "queue-operation", "content": "run"}}
        ]
        path = self._write_jsonl("headless.jsonl", entries)
        result = analyze_session(path)
        self.assertTrue(result["is_headless"])

    def test_interactive_session_default(self):
        entries = [
            {"message": {"content": "hello world"}}
        ]
        path = self._write_jsonl("interactive.jsonl", entries)
        result = analyze_session(path)
        self.assertFalse(result["is_headless"])

    def test_extracts_slash_commands(self):
        entries = [
            {"message": {"content": "invoking <command-name>commit</command-name> now"}},
            {"message": {"content": "<command-name>sinkra-squad:sinkra-chief</command-name>"}},
        ]
        path = self._write_jsonl("commands.jsonl", entries)
        result = analyze_session(path)
        self.assertEqual(result["slash_commands"]["/commit"], 1)
        self.assertEqual(result["slash_commands"]["/sinkra-squad:sinkra-chief"], 1)

    def test_ignores_builtin_commands(self):
        entries = [
            {"message": {"content": "<command-name>clear</command-name>"}},
            {"message": {"content": "<command-name>model</command-name>"}},
            {"message": {"content": "<command-name>help</command-name>"}},
        ]
        path = self._write_jsonl("builtins.jsonl", entries)
        result = analyze_session(path)
        self.assertEqual(len(result["slash_commands"]), 0)

    def test_extracts_skill_tool_invocations(self):
        entries = [
            {"message": {"content": [
                {"type": "tool_use", "name": "Skill", "input": {"skill": "handoff"}},
                {"type": "tool_use", "name": "Skill", "input": {"skill": "commit"}},
                {"type": "tool_use", "name": "Skill", "input": {"skill": "commit"}},
            ]}}
        ]
        path = self._write_jsonl("skills.jsonl", entries)
        result = analyze_session(path)
        self.assertEqual(result["skill_invocations"]["handoff"], 1)
        self.assertEqual(result["skill_invocations"]["commit"], 2)

    def test_extracts_agent_types(self):
        entries = [
            {"message": {"content": [
                {"type": "tool_use", "name": "Agent", "input": {"subagent_type": "dev", "prompt": "do stuff"}},
                {"type": "tool_use", "name": "Agent", "input": {"subagent_type": "Explore", "prompt": "find"}},
                {"type": "tool_use", "name": "Agent", "input": {"prompt": "no type specified"}},
            ]}}
        ]
        path = self._write_jsonl("agents.jsonl", entries)
        result = analyze_session(path)
        self.assertEqual(result["agent_types"]["dev"], 1)
        self.assertEqual(result["agent_types"]["Explore"], 1)
        self.assertEqual(result["agent_types"]["general-purpose"], 1)

    def test_extracts_shell_runners(self):
        entries = [
            {"message": {"content": [
                {"type": "tool_use", "name": "Bash", "input": {"command": "bash sinkra-map.sh --all"}},
                {"type": "tool_use", "name": "Bash", "input": {"command": "/path/to/validate-squad.sh config.yaml"}},
                {"type": "tool_use", "name": "Bash", "input": {"command": "npm run build"}},
            ]}}
        ]
        path = self._write_jsonl("runners.jsonl", entries)
        result = analyze_session(path)
        self.assertEqual(result["shell_runners"]["sinkra-map.sh"], 1)
        self.assertEqual(result["shell_runners"]["validate-squad.sh"], 1)
        self.assertNotIn("build", result["shell_runners"])

    def test_extracts_dates_from_summary(self):
        entries = [
            {"type": "summary", "timestamp": "2026-03-28T10:00:00Z"},
        ]
        path = self._write_jsonl("dates.jsonl", entries)
        result = analyze_session(path)
        self.assertIn("2026-03-28", result["dates"])

    def test_handles_malformed_json_lines(self):
        path = os.path.join(self.tmpdir, "bad.jsonl")
        with open(path, "w") as f:
            f.write("not json\n")
            f.write('{"message": {"content": "<command-name>commit</command-name>"}}\n')
            f.write("{broken\n")
        result = analyze_session(path)
        self.assertEqual(result["slash_commands"]["/commit"], 1)

    def test_handles_content_as_list_of_blocks(self):
        entries = [
            {"message": {"content": [
                {"type": "text", "text": "running <command-name>deploy</command-name>"},
                {"type": "text", "text": "also <command-name>review-story</command-name>"},
            ]}}
        ]
        path = self._write_jsonl("blocks.jsonl", entries)
        result = analyze_session(path)
        self.assertEqual(result["slash_commands"]["/deploy"], 1)
        self.assertEqual(result["slash_commands"]["/review-story"], 1)

    def test_handles_content_as_string(self):
        entries = [
            {"message": "plain string message, no tool use"}
        ]
        path = self._write_jsonl("string_msg.jsonl", entries)
        result = analyze_session(path)
        self.assertEqual(len(result["slash_commands"]), 0)

    def test_nonexistent_file_does_not_crash(self):
        result = analyze_session("/nonexistent/path.jsonl")
        self.assertFalse(result["is_headless"])
        self.assertEqual(len(result["skill_invocations"]), 0)

    def test_dedupes_branches_and_extracts_rich_metrics(self):
        entries = [
            {
                "type": "user",
                "uuid": "u1",
                "sessionId": "sess-main",
                "timestamp": "2026-04-01T10:00:00Z",
                "message": {"content": [{"type": "text", "text": "Start"}]},
            },
            {
                "type": "assistant",
                "uuid": "a1",
                "parentUuid": "u1",
                "sessionId": "sess-main",
                "timestamp": "2026-04-01T10:00:05Z",
                "message": {
                    "usage": {"input_tokens": 100, "output_tokens": 50},
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Edit",
                            "input": {
                                "file_path": "/tmp/a.py",
                                "old_string": "old\nline",
                                "new_string": "new\nline\nextra",
                            },
                        },
                        {"type": "tool_use", "name": "WebSearch", "input": {"query": "branch dedupe"}},
                        {"type": "tool_result", "is_error": True, "content": "command failed with exit code 1"},
                    ],
                },
            },
            {
                "type": "user",
                "uuid": "u2",
                "parentUuid": "a1",
                "sessionId": "sess-main",
                "timestamp": "2026-04-01T10:00:20Z",
                "message": {"content": [{"type": "text", "text": "Continue"}]},
            },
            {
                "type": "assistant",
                "uuid": "a2",
                "parentUuid": "u2",
                "sessionId": "sess-main",
                "timestamp": "2026-04-01T10:00:35Z",
                "message": {
                    "usage": {"input_tokens": 70, "output_tokens": 30},
                    "content": [
                        {"type": "tool_use", "name": "Agent", "input": {"subagent_type": "dev", "prompt": "x"}},
                        {"type": "tool_use", "name": "mcp__drive__fetch", "input": {"url": "x"}},
                        {
                            "type": "tool_use",
                            "name": "Write",
                            "input": {"file_path": "/tmp/b.py", "content": "alpha\nbeta\n"},
                        },
                        {"type": "text", "text": "[Request interrupted by user]"},
                    ],
                },
            },
            {
                "type": "user",
                "uuid": "u3",
                "parentUuid": "a2",
                "sessionId": "sess-main",
                "timestamp": "2026-04-01T10:00:40Z",
                "message": {"content": [{"type": "text", "text": "Final ask"}]},
            },
            {
                "type": "user",
                "uuid": "u2b",
                "parentUuid": "a1",
                "sessionId": "sess-main",
                "timestamp": "2026-04-01T10:00:25Z",
                "message": {"content": [{"type": "text", "text": "Short branch"}]},
            },
            {
                "type": "assistant",
                "uuid": "a2b",
                "parentUuid": "u2b",
                "sessionId": "sess-main",
                "timestamp": "2026-04-01T10:00:30Z",
                "message": {
                    "content": [
                        {"type": "tool_use", "name": "Bash", "input": {"command": "bash ignored.sh"}}
                    ]
                },
            },
            {
                "type": "assistant",
                "uuid": "other-1",
                "sessionId": "sess-stray",
                "timestamp": "2026-04-01T10:00:50Z",
                "message": {
                    "content": [
                        {"type": "tool_use", "name": "Skill", "input": {"skill": "deploy"}}
                    ]
                },
            },
        ]
        path = self._write_jsonl("rich-session.jsonl", entries)
        result = analyze_session(path)

        self.assertEqual(result["session_id"], "sess-main")
        self.assertEqual(result["branches_total"], 2)
        self.assertEqual(result["branches_deduped"], 1)
        self.assertEqual(result["user_messages"], 3)
        self.assertEqual(result["assistant_messages"], 2)
        self.assertEqual(result["duration_minutes"], 1)
        self.assertEqual(result["input_tokens"], 170)
        self.assertEqual(result["output_tokens"], 80)
        self.assertEqual(result["tool_errors"], 1)
        self.assertEqual(result["tool_error_categories"]["Command Failed"], 1)
        self.assertEqual(result["user_interruptions"], 1)
        self.assertEqual(result["user_response_times"], [15.0, 5.0])
        self.assertTrue(result["uses_task_agent"])
        self.assertTrue(result["uses_mcp"])
        self.assertTrue(result["uses_web_search"])
        self.assertFalse(result["uses_web_fetch"])
        self.assertEqual(result["tools"]["Edit"], 1)
        self.assertEqual(result["tools"]["Agent"], 1)
        self.assertEqual(result["tools"]["Write"], 1)
        self.assertEqual(result["tools"]["Bash"], 1)
        self.assertNotIn("deploy", result["skill_invocations"])
        self.assertEqual(result["lines_added"], 4)
        self.assertEqual(result["lines_removed"], 1)
        self.assertEqual(result["files_modified"], {"/tmp/a.py", "/tmp/b.py"})

    def test_counts_workflow_usage_from_non_selected_branch(self):
        entries = [
            {
                "type": "user",
                "uuid": "u1",
                "sessionId": "sess-main",
                "timestamp": "2026-04-01T10:00:00Z",
                "message": {"content": [{"type": "text", "text": "Start"}]},
            },
            {
                "type": "assistant",
                "uuid": "a1",
                "parentUuid": "u1",
                "sessionId": "sess-main",
                "timestamp": "2026-04-01T10:00:05Z",
                "message": {"content": [{"type": "text", "text": "Choose a path"}]},
            },
            {
                "type": "user",
                "uuid": "u-long",
                "parentUuid": "a1",
                "sessionId": "sess-main",
                "timestamp": "2026-04-01T10:00:10Z",
                "message": {"content": [{"type": "text", "text": "Long branch"}]},
            },
            {
                "type": "assistant",
                "uuid": "a-long",
                "parentUuid": "u-long",
                "sessionId": "sess-main",
                "timestamp": "2026-04-01T10:00:15Z",
                "message": {"content": [{"type": "text", "text": "Continuing"}]},
            },
            {
                "type": "user",
                "uuid": "u-long-2",
                "parentUuid": "a-long",
                "sessionId": "sess-main",
                "timestamp": "2026-04-01T10:00:20Z",
                "message": {"content": [{"type": "text", "text": "Finish long branch"}]},
            },
            {
                "type": "assistant",
                "uuid": "a-short",
                "parentUuid": "a1",
                "sessionId": "sess-main",
                "timestamp": "2026-04-01T10:00:12Z",
                "message": {
                    "content": [
                        {"type": "text", "text": "<command-name>commit</command-name>"},
                        {"type": "tool_use", "name": "Skill", "input": {"skill": "commit"}},
                    ]
                },
            },
        ]
        path = self._write_jsonl("branch-usage.jsonl", entries)
        result = analyze_session(path)
        self.assertEqual(result["user_messages"], 3)
        self.assertEqual(result["assistant_messages"], 2)
        self.assertEqual(result["slash_commands"]["/commit"], 1)
        self.assertEqual(result["skill_invocations"]["commit"], 1)


class TestGetRecentCommits(unittest.TestCase):
    """Unit tests for get_recent_commits()."""

    def test_nonexistent_repo_returns_empty(self):
        result = get_recent_commits("/nonexistent/repo", 14)
        self.assertEqual(result, {})

    def test_categorizes_story_commits(self):
        fake_output = textwrap.dedent("""\
            abc1234 feat: implement feature [Story 71.1]
            def5678 docs(epic-71): add stories
            ghi9012 fix: correct RLS policy
            jkl3456 chore: squad validation
            mno7890 fix(sinkra): add tokens
            pqr1234 feat(synapse): scanner
            stu5678 fix(yaml): duplicate keys
            vwx9012 feat: migrate AN_KE_115 to structure
        """)
        with patch("subprocess.check_output", return_value=fake_output):
            result = get_recent_commits("/fake/repo", 14)
        self.assertEqual(result["SDC (Story/Epic)"], 2)
        self.assertEqual(result["Squad"], 1)
        self.assertEqual(result["SINKRA"], 1)
        self.assertEqual(result["Synapse"], 1)
        self.assertEqual(result["CI/Infra"], 1)
        self.assertEqual(result["MMOS/Minds"], 1)
        self.assertEqual(result["Other"], 1)


class TestDiscoverInventory(unittest.TestCase):
    """Unit tests for discover_inventory()."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.claude_dir = os.path.join(self.tmpdir, ".claude")

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _make_dirs(self, *paths):
        for p in paths:
            os.makedirs(os.path.join(self.tmpdir, p), exist_ok=True)

    def _make_files(self, *paths):
        for p in paths:
            full = os.path.join(self.tmpdir, p)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w") as f:
                f.write("# placeholder")

    def test_discovers_skills(self):
        self._make_dirs(".claude/skills/commit", ".claude/skills/handoff", ".claude/skills/deploy")
        inv = discover_inventory(self.tmpdir)
        self.assertEqual(sorted(inv["skills"]), ["commit", "deploy", "handoff"])

    def test_discovers_agents(self):
        self._make_files(".claude/agents/dev.md", ".claude/agents/qa.md")
        inv = discover_inventory(self.tmpdir)
        self.assertEqual(sorted(inv["agents"]), ["dev", "qa"])

    def test_discovers_skill_groups(self):
        self._make_files(
            ".claude/skills/copy-copy-chief/SKILL.md",
            ".claude/skills/copy-gary-halbert/SKILL.md",
            ".claude/skills/hormozi-hormozi-chief/SKILL.md",
        )
        inv = discover_inventory(self.tmpdir)
        self.assertEqual(inv["skill_groups"]["copy"], 2)
        self.assertEqual(inv["skill_groups"]["hormozi"], 1)

    def test_empty_project(self):
        inv = discover_inventory(self.tmpdir)
        self.assertEqual(inv["skills"], [])
        self.assertEqual(inv["agents"], [])
        self.assertEqual(inv["skill_groups"], {})

    def test_ignores_non_md_agent_files(self):
        self._make_files(".claude/agents/dev.md", ".claude/agents/readme.txt")
        inv = discover_inventory(self.tmpdir)
        self.assertEqual(inv["agents"], ["dev"])

    def test_ignores_files_in_skills_dir(self):
        self._make_files(".claude/skills/registry.yaml")
        self._make_dirs(".claude/skills/commit")
        inv = discover_inventory(self.tmpdir)
        self.assertEqual(inv["skills"], ["commit"])


class TestGenerateReport(unittest.TestCase):
    """Integration tests for generate_report()."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.projects_dir = os.path.join(self.tmpdir, "projects")
        os.makedirs(self.projects_dir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _create_project_session(self, project_name, filename, entries):
        proj_dir = os.path.join(self.projects_dir, project_name)
        os.makedirs(proj_dir, exist_ok=True)
        path = os.path.join(proj_dir, filename)
        with open(path, "w") as f:
            for entry in entries:
                f.write(json.dumps(entry) + "\n")
        return path

    def test_empty_projects_dir(self):
        data = generate_report(self.projects_dir, 14)
        self.assertEqual(data["projects"], {})

    def test_single_interactive_session(self):
        self._create_project_session(
            "test-proj", "session1.jsonl",
            [
                {"message": {"content": [
                    {"type": "tool_use", "name": "Skill", "input": {"skill": "commit"}},
                    {"type": "tool_use", "name": "Agent", "input": {"subagent_type": "dev", "prompt": "x"}},
                ]}}
            ]
        )
        data = generate_report(self.projects_dir, 14)
        self.assertIn("test-proj", data["projects"])
        self.assertEqual(data["projects"]["test-proj"]["interactive"], 1)
        self.assertEqual(data["projects"]["test-proj"]["headless"], 0)
        self.assertEqual(data["skills"]["commit"], 1)
        self.assertEqual(data["agents"]["dev"], 1)

    def test_headless_session_separated(self):
        self._create_project_session(
            "test-proj", "session_hl.jsonl",
            [
                {"message": {"type": "queue-operation", "content": "run"}},
                {"message": {"content": [
                    {"type": "tool_use", "name": "Skill", "input": {"skill": "deploy"}},
                ]}}
            ]
        )
        data = generate_report(self.projects_dir, 14)
        self.assertEqual(data["projects"]["test-proj"]["headless"], 1)
        self.assertEqual(data["projects"]["test-proj"]["interactive"], 0)
        self.assertEqual(data["headless_skills"]["deploy"], 1)
        self.assertNotIn("deploy", data["skills"])

    def test_multiple_projects(self):
        self._create_project_session(
            "proj-a", "s1.jsonl",
            [{"message": {"content": [
                {"type": "tool_use", "name": "Agent", "input": {"subagent_type": "dev", "prompt": "x"}},
            ]}}]
        )
        self._create_project_session(
            "proj-b", "s1.jsonl",
            [{"message": {"content": [
                {"type": "tool_use", "name": "Agent", "input": {"subagent_type": "dev", "prompt": "y"}},
            ]}}]
        )
        data = generate_report(self.projects_dir, 14)
        self.assertEqual(len(data["projects"]), 2)
        self.assertEqual(data["agents"]["dev"], 2)
        self.assertEqual(data["agent_projects"]["dev"], {"proj-a", "proj-b"})

    def test_subagent_sessions_counted(self):
        proj_dir = os.path.join(self.projects_dir, "test-proj")
        os.makedirs(proj_dir, exist_ok=True)
        # Main session
        main_path = os.path.join(proj_dir, "main.jsonl")
        with open(main_path, "w") as f:
            f.write(json.dumps({"message": {"content": "hello"}}) + "\n")
        # Subagent session
        sub_dir = os.path.join(proj_dir, "main-id", "subagents")
        os.makedirs(sub_dir, exist_ok=True)
        sub_path = os.path.join(sub_dir, "agent-abc.jsonl")
        with open(sub_path, "w") as f:
            f.write(json.dumps({"message": {"content": [
                {"type": "tool_use", "name": "Agent", "input": {"subagent_type": "Explore", "prompt": "x"}},
            ]}}) + "\n")

        data = generate_report(self.projects_dir, 14)
        self.assertEqual(data["projects"]["test-proj"]["subagents"], 1)
        self.assertEqual(data["agents"]["Explore"], 1)

    def test_aggregates_rich_metrics_and_top_tools(self):
        self._create_project_session(
            "test-proj",
            "session-rich.jsonl",
            [
                {
                    "type": "user",
                    "uuid": "u1",
                    "sessionId": "sess-main",
                    "timestamp": "2026-04-01T10:00:00Z",
                    "message": {"content": [{"type": "text", "text": "Start"}]},
                },
                {
                    "type": "assistant",
                    "uuid": "a1",
                    "parentUuid": "u1",
                    "sessionId": "sess-main",
                    "timestamp": "2026-04-01T10:00:05Z",
                    "message": {
                        "usage": {"input_tokens": 100, "output_tokens": 50},
                        "content": [
                            {
                                "type": "tool_use",
                                "name": "Edit",
                                "input": {
                                    "file_path": "/tmp/a.py",
                                    "old_string": "old\nline",
                                    "new_string": "new\nline\nextra",
                                },
                            },
                            {"type": "tool_use", "name": "WebSearch", "input": {"query": "branch dedupe"}},
                            {"type": "tool_result", "is_error": True, "content": "command failed with exit code 1"},
                        ],
                    },
                },
                {
                    "type": "user",
                    "uuid": "u2",
                    "parentUuid": "a1",
                    "sessionId": "sess-main",
                    "timestamp": "2026-04-01T10:00:20Z",
                    "message": {"content": [{"type": "text", "text": "Continue"}]},
                },
                {
                    "type": "assistant",
                    "uuid": "a2",
                    "parentUuid": "u2",
                    "sessionId": "sess-main",
                    "timestamp": "2026-04-01T10:00:35Z",
                    "message": {
                        "usage": {"input_tokens": 70, "output_tokens": 30},
                        "content": [
                            {"type": "tool_use", "name": "Agent", "input": {"subagent_type": "dev", "prompt": "x"}},
                            {"type": "tool_use", "name": "mcp__drive__fetch", "input": {"url": "x"}},
                            {
                                "type": "tool_use",
                                "name": "Write",
                                "input": {"file_path": "/tmp/b.py", "content": "alpha\nbeta\n"},
                            },
                            {"type": "text", "text": "[Request interrupted by user]"},
                        ],
                    },
                },
                {
                    "type": "user",
                    "uuid": "u3",
                    "parentUuid": "a2",
                    "sessionId": "sess-main",
                    "timestamp": "2026-04-01T10:00:40Z",
                    "message": {"content": [{"type": "text", "text": "Final ask"}]},
                },
                {
                    "type": "user",
                    "uuid": "u2b",
                    "parentUuid": "a1",
                    "sessionId": "sess-main",
                    "timestamp": "2026-04-01T10:00:25Z",
                    "message": {"content": [{"type": "text", "text": "Short branch"}]},
                },
                {
                    "type": "assistant",
                    "uuid": "a2b",
                    "parentUuid": "u2b",
                    "sessionId": "sess-main",
                    "timestamp": "2026-04-01T10:00:30Z",
                    "message": {
                        "content": [
                            {"type": "tool_use", "name": "Bash", "input": {"command": "bash ignored.sh"}}
                        ]
                    },
                },
            ],
        )
        self._create_project_session(
            "test-proj",
            "session-headless.jsonl",
            [
                {"message": {"type": "queue-operation", "content": "run"}},
                {"message": {"content": [
                    {"type": "tool_use", "name": "WebFetch", "input": {"url": "https://example.com"}}
                ]}},
            ],
        )

        data = generate_report(self.projects_dir, 14)

        self.assertEqual(data["summary"]["total_interactive"], 1)
        self.assertEqual(data["summary"]["total_headless"], 1)
        self.assertEqual(data["summary"]["total_branches_deduped"], 1)
        self.assertEqual(data["summary"]["total_tool_errors"], 1)
        self.assertEqual(data["summary"]["sessions_with_task_agent"], 1)
        self.assertEqual(data["summary"]["sessions_with_mcp"], 1)
        self.assertEqual(data["summary"]["sessions_with_web_search"], 1)
        self.assertEqual(data["summary"]["sessions_with_web_fetch"], 1)
        self.assertEqual(data["summary"]["total_lines_added"], 4)
        self.assertEqual(data["summary"]["total_lines_removed"], 1)
        self.assertEqual(data["summary"]["total_unique_files_modified"], 2)
        self.assertEqual(data["summary"]["tool_error_categories"]["Command Failed"], 1)
        self.assertEqual(data["tools"]["Edit"], 1)
        self.assertEqual(data["tools"]["WebFetch"], 1)
        self.assertEqual(data["tool_projects"]["Edit"], {"test-proj"})
        self.assertEqual(data["projects"]["test-proj"]["avg_user_response_seconds"], 10.0)
        self.assertEqual(data["projects"]["test-proj"]["unique_files_modified"], 2)

    def test_filters_meta_sessions_and_counts_exclusions(self):
        self._create_project_session(
            "test-proj",
            "meta-session.jsonl",
            [
                {
                    "type": "user",
                    "message": {"content": [{"type": "text", "text": "RESPOND WITH ONLY A VALID JSON OBJECT"}]},
                },
                {
                    "type": "assistant",
                    "message": {"content": [{"type": "tool_use", "name": "Skill", "input": {"skill": "commit"}}]},
                },
            ],
        )

        data = generate_report(self.projects_dir, 14)

        self.assertEqual(data["projects"], {})
        self.assertEqual(data["summary"]["total_sessions"], 0)
        self.assertEqual(data["summary"]["total_sessions_scanned"], 1)
        self.assertEqual(data["summary"]["excluded_meta_sessions"], 1)

    def test_filters_non_substantive_sessions_but_keeps_meaningful_short_ones(self):
        self._create_project_session(
            "test-proj",
            "non-substantive.jsonl",
            [
                {
                    "type": "user",
                    "message": {"content": [{"type": "text", "text": "oi"}]},
                },
            ],
        )
        self._create_project_session(
            "test-proj",
            "meaningful-short.jsonl",
            [
                {
                    "type": "user",
                    "message": {"content": [{"type": "text", "text": "rodar skill"}]},
                },
                {
                    "type": "assistant",
                    "message": {
                        "content": [
                            {"type": "tool_use", "name": "Skill", "input": {"skill": "commit"}},
                        ]
                    },
                },
            ],
        )

        data = generate_report(self.projects_dir, 14)

        self.assertIn("test-proj", data["projects"])
        self.assertEqual(data["summary"]["total_sessions_scanned"], 2)
        self.assertEqual(data["summary"]["excluded_non_substantive_sessions"], 1)
        self.assertEqual(data["summary"]["total_sessions"], 1)
        self.assertEqual(data["skills"]["commit"], 1)

    def test_builds_usage_inventory_without_changing_original_rankings(self):
        self._create_project_session(
            "test-proj",
            "inventory-rich.jsonl",
            [
                {
                    "type": "user",
                    "uuid": "u1",
                    "sessionId": "sess-inventory",
                    "timestamp": "2026-04-01T10:00:00Z",
                    "message": {"content": [{"type": "text", "text": "Rodar commit"}]},
                },
                {
                    "type": "assistant",
                    "uuid": "a1",
                    "parentUuid": "u1",
                    "sessionId": "sess-inventory",
                    "timestamp": "2026-04-01T10:00:05Z",
                    "message": {
                        "usage": {"input_tokens": 80, "output_tokens": 40},
                        "content": [
                            {"type": "text", "text": "<command-name>commit</command-name>"},
                            {"type": "tool_use", "name": "Skill", "input": {"skill": "commit"}},
                            {"type": "tool_use", "name": "Agent", "input": {"subagent_type": "dev", "prompt": "x"}},
                            {
                                "type": "tool_use",
                                "name": "Edit",
                                "input": {
                                    "file_path": "/tmp/app.py",
                                    "old_string": "old",
                                    "new_string": "new\nextra",
                                },
                            },
                            {"type": "tool_use", "name": "Bash", "input": {"command": "bash validate-squad.sh"}},
                            {"type": "tool_result", "is_error": True, "content": "command failed with exit code 1"},
                        ],
                    },
                },
                {
                    "type": "user",
                    "uuid": "u2",
                    "parentUuid": "a1",
                    "sessionId": "sess-inventory",
                    "timestamp": "2026-04-01T10:00:15Z",
                    "message": {"content": [{"type": "text", "text": "Continuar"}]},
                },
            ],
        )

        data = generate_report(self.projects_dir, 14)

        self.assertEqual(data["skills"]["commit"], 1)
        self.assertEqual(data["tools"]["Edit"], 1)
        self.assertEqual(data["runners"]["validate-squad.sh"], 1)
        self.assertEqual(data["usage_inventory"]["summary"]["normalized_skills"], 1)
        self.assertEqual(data["usage_inventory"]["summary"]["slash_commands"], 1)
        self.assertEqual(data["usage_inventory"]["summary"]["skill_tools"], 1)
        self.assertEqual(data["usage_inventory"]["normalized_skills"]["top_by_usage"][0]["name"], "commit")
        self.assertEqual(data["usage_inventory"]["slash_commands"]["top_by_usage"][0]["name"], "/commit")
        self.assertEqual(data["usage_inventory"]["skill_tools"]["top_by_usage"][0]["name"], "commit")
        self.assertEqual(data["usage_inventory"]["agents"]["top_by_usage"][0]["name"], "dev")
        self.assertEqual(data["usage_inventory"]["tools"]["top_by_usage"][0]["name"], "Agent")


class TestCacheAndInsights(unittest.TestCase):
    """Tests cache invalidation and optional insights enrichment."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.projects_dir = os.path.join(self.tmpdir, "projects")
        self.cache_dir = os.path.join(self.tmpdir, "cache")
        os.makedirs(self.projects_dir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _write_session(self, project_name, filename, entries):
        proj_dir = os.path.join(self.projects_dir, project_name)
        os.makedirs(proj_dir, exist_ok=True)
        session_path = os.path.join(proj_dir, filename)
        with open(session_path, "w") as f:
            for entry in entries:
                f.write(json.dumps(entry) + "\n")
        return session_path

    def test_session_meta_cache_hit_and_invalidation(self):
        session_path = self._write_session(
            "test-proj",
            "s1.jsonl",
            [
                {"message": {"content": "<command-name>commit</command-name>"}},
            ],
        )

        result1, cache_state1 = get_session_meta(session_path, cache_root=self.cache_dir)
        self.assertEqual(cache_state1, "miss")
        self.assertEqual(result1["slash_commands"]["/commit"], 1)

        with patch.object(report_mod, "analyze_session", side_effect=AssertionError("cache should be used")):
            result2, cache_state2 = get_session_meta(session_path, cache_root=self.cache_dir)
        self.assertEqual(cache_state2, "hit")
        self.assertEqual(result2["slash_commands"]["/commit"], 1)

        with open(session_path, "a") as f:
            f.write(json.dumps({"message": {"content": "<command-name>deploy</command-name>"}}) + "\n")

        original_analyze = report_mod.analyze_session
        with patch.object(report_mod, "analyze_session", wraps=original_analyze) as mocked:
            result3, cache_state3 = get_session_meta(session_path, cache_root=self.cache_dir)
        self.assertEqual(cache_state3, "miss")
        self.assertTrue(mocked.called)
        self.assertEqual(result3["slash_commands"]["/deploy"], 1)

    def test_generate_report_uses_llm_enrichment_when_configured(self):
        self._write_session(
            "test-proj",
            "s1.jsonl",
            [
                {
                    "type": "user",
                    "uuid": "u1",
                    "sessionId": "sess-main",
                    "timestamp": "2026-04-01T10:00:00Z",
                    "message": {"content": [{"type": "text", "text": "Investigar workflow"}]},
                },
                {
                    "type": "assistant",
                    "uuid": "a1",
                    "parentUuid": "u1",
                    "sessionId": "sess-main",
                    "timestamp": "2026-04-01T10:00:05Z",
                    "message": {
                        "content": [
                            {"type": "tool_use", "name": "WebSearch", "input": {"query": "workflow"}},
                            {"type": "tool_use", "name": "Agent", "input": {"subagent_type": "dev", "prompt": "x"}},
                        ]
                    },
                },
            ],
        )

        def fake_run_insights_command(command, payload, timeout_seconds=60):
            self.assertEqual(command, "dummy-insights")
            if payload["mode"] == "facet":
                self.assertIn("Investigar workflow", payload["transcript"])
                return {
                    "underlying_goal": "Compreender e refinar o workflow",
                    "goal_categories": ["workflow-analysis", "research"],
                    "outcome": "partial",
                    "satisfaction": "medium",
                    "friction_points": ["handoff ambiguity"],
                    "primary_success": "Mapeou o fluxo principal",
                    "brief_summary": "Sessão de análise de workflow.",
                }
            if payload["mode"] == "insight_sections":
                self.assertIn("facet_summary", payload)
                return {
                    "at_a_glance": "Narrativa LLM.",
                    "at_a_glance_sections": {
                        "whats_working": "Narrativa LLM.",
                        "whats_hindering": "Alguma fricção.",
                        "quick_wins": "Padronizar handoffs.",
                        "ambitious_workflows": "Usar agents em loops maiores.",
                    },
                    "project_area_items": [
                        {
                            "name": "Workflow analysis",
                            "session_count": 1,
                            "description": "Compreender e refinar o workflow principal.",
                        }
                    ],
                    "interaction_style": "Direto e iterativo.",
                    "what_works_items": [
                        {"title": "Bom uso de pesquisa e agentes", "description": "Explorou e refinou o fluxo principal."}
                    ],
                    "friction_categories": [
                        {
                            "category": "Ambiguidade de handoff",
                            "description": "Houve ambiguidade na passagem de contexto.",
                            "examples": ["handoff ambiguity"],
                        }
                    ],
                    "claude_md_additions": [],
                    "features_to_try": [],
                    "usage_patterns": [],
                    "on_the_horizon": "Expandir o uso de agents.",
                    "horizon_opportunities": [],
                    "feedback": {"cc_team_improvements": [], "model_behavior_improvements": []},
                    "fun_ending_card": {"headline": "Fechamento LLM.", "detail": "Sessão útil."},
                }
            raise AssertionError(f"Modo inesperado: {payload['mode']}")

        with patch.object(report_mod, "run_insights_command", side_effect=fake_run_insights_command):
            data = generate_report(
                self.projects_dir,
                14,
                cache_dir=self.cache_dir,
                use_cache=False,
                insights_command="dummy-insights",
            )

        self.assertEqual(data["facet_summary"]["sources"]["llm"], 1)
        self.assertEqual(data["facet_summary"]["goal_categories"]["workflow-analysis"], 1)
        self.assertEqual(data["facet_summary"]["friction_points"]["handoff ambiguity"], 1)
        self.assertEqual(data["narrative"]["source"], "llm")
        self.assertEqual(data["narrative"]["at_a_glance"], "Narrativa LLM.")
        self.assertEqual(data["summary"]["facets_cache_misses"], 1)

    def test_build_transcript_excerpt_summarizes_long_transcript_in_chunks(self):
        session_path = self._write_session(
            "test-proj",
            "long-session.jsonl",
            [
                {
                    "type": "user",
                    "uuid": "u1",
                    "sessionId": "sess-long",
                    "timestamp": "2026-04-01T10:00:00Z",
                    "message": {"content": [{"type": "text", "text": "A" * 20000}]},
                },
                {
                    "type": "assistant",
                    "uuid": "a1",
                    "parentUuid": "u1",
                    "sessionId": "sess-long",
                    "timestamp": "2026-04-01T10:00:05Z",
                    "message": {
                        "content": [
                            {"type": "text", "text": "B" * 20000},
                            {"type": "tool_use", "name": "Edit", "input": {"file_path": "/tmp/a.py"}},
                        ]
                    },
                },
            ],
        )

        def fake_run_insights_command(command, payload, timeout_seconds=60):
            self.assertEqual(command, "dummy-insights")
            self.assertEqual(payload["mode"], "summarize_chunk")
            return {"summary": f"chunk-size={len(payload['transcript_chunk'])}"}

        with patch.object(report_mod, "run_insights_command", side_effect=fake_run_insights_command) as mocked:
            excerpt = build_transcript_excerpt(session_path, insights_command="dummy-insights")

        self.assertTrue(mocked.called)
        self.assertIn("[long transcript summarized in", excerpt)
        self.assertIn("chunk-size=", excerpt)


class TestRecommendations(unittest.TestCase):
    """Tests deterministic workflow recommendations."""

    def test_generates_global_and_project_recommendations(self):
        data = {
            "projects": {
                "proj-a": {
                    "interactive": 4,
                    "headless": 0,
                    "subagents": 0,
                    "tool_errors": 3,
                    "branches_deduped": 3,
                    "lines_added": 140,
                    "lines_removed": 30,
                    "sessions_with_task_agent": 0,
                    "sessions_with_mcp": 0,
                    "sessions_with_web_search": 3,
                    "sessions_with_web_fetch": 1,
                    "avg_user_response_seconds": 52,
                    "user_interruptions": 2,
                },
            },
            "summary": {
                "total_sessions": 12,
                "total_tool_errors": 5,
                "total_branches_deduped": 5,
                "total_lines_added": 500,
                "total_lines_removed": 100,
                "sessions_with_task_agent": 1,
                "sessions_with_web_search": 6,
                "sessions_with_web_fetch": 2,
                "sessions_with_mcp": 1,
            },
            "facet_summary": {
                "friction_points": Counter({"user interruptions": 3}),
            },
        }

        recommendations = generate_workflow_recommendations(data)

        self.assertGreaterEqual(recommendations["summary"]["total_recommendations"], 5)
        self.assertGreaterEqual(recommendations["summary"]["high_impact"], 1)
        self.assertIn("proj-a", recommendations["by_project"])
        self.assertTrue(any(
            rec["category"] == "permissions"
            for rec in recommendations["by_project"]["proj-a"]
        ))
        self.assertTrue(any(
            rec["scope"] == "global" and rec["category"] == "context"
            for rec in recommendations["top_recommendations"]
        ))


class TestFormatMarkdown(unittest.TestCase):
    """Tests for format_markdown()."""

    def _make_data(self, **overrides):
        base = {
            "projects": {"my-proj": {
                "interactive": 10,
                "headless": 2,
                "subagents": 5,
                "date_range": "2026-03-20 to 2026-03-31",
                "input_tokens": 1200,
                "output_tokens": 640,
                "tool_errors": 3,
                "branches_deduped": 4,
                "lines_added": 120,
                "lines_removed": 45,
                "unique_files_modified": 12,
                "avg_user_response_seconds": 18.5,
            }},
            "summary": {
                "total_sessions": 12,
                "total_interactive": 10,
                "total_headless": 2,
                "total_subagents": 5,
                "total_session_files": 17,
                "total_branches": 14,
                "total_branches_deduped": 4,
                "total_user_messages": 88,
                "total_assistant_messages": 74,
                "total_input_tokens": 1200,
                "total_output_tokens": 640,
                "total_tool_errors": 3,
                "tool_error_categories": Counter({"Command Failed": 2, "Edit Failed": 1}),
                "total_user_interruptions": 2,
                "avg_user_response_seconds": 18.5,
                "sessions_with_task_agent": 6,
                "sessions_with_mcp": 3,
                "sessions_with_web_search": 4,
                "sessions_with_web_fetch": 1,
                "total_lines_added": 120,
                "total_lines_removed": 45,
                "total_unique_files_modified": 12,
                "session_meta_cache_hits": 9,
                "session_meta_cache_misses": 8,
                "facets_cache_hits": 7,
                "facets_cache_misses": 10,
            },
            "facet_summary": {
                "sessions_with_facets": 17,
                "sources": Counter({"heuristic": 10, "llm": 7}),
                "goal_categories": Counter({"coding": 9, "research": 5, "orchestration": 3}),
                "outcomes": Counter({"implemented": 8, "partial": 6, "blocked": 3}),
                "satisfaction": Counter({"high": 7, "medium": 6, "low": 4}),
                "friction_points": Counter({"command failed": 2, "user interruptions": 1}),
            },
            "narrative": {
                "source": "llm",
                "at_a_glance": "Visão geral sintética.",
                "project_areas": "Áreas mais frequentes: coding e research.",
                "interaction_style": "Interações objetivas.",
                "what_works": "Boa taxa de implementação.",
                "friction_analysis": "Erros de comando aparecem no topo.",
                "suggestions": "Consolidar prompts e skills recorrentes.",
                "on_the_horizon": "Escalar workflows paralelos mais ambiciosos.",
                "fun_ending": "Muito trabalho real concentrado em poucos fluxos.",
            },
            "recommendations": {
                "summary": {
                    "total_recommendations": 4,
                    "high_impact": 2,
                    "medium_impact": 2,
                    "low_impact": 0,
                    "quick_wins": 2,
                    "estimated_minutes_saved_per_week": 91,
                },
                "global": [
                    {
                        "id": "global-context-discipline",
                        "scope": "global",
                        "project": None,
                        "title": "Adotar disciplina operacional de compaction e checkpoints de plano",
                        "description": "Muitas branches deduplicadas.",
                        "impact": "HIGH",
                        "effort": "Quick",
                        "category": "context",
                        "phase": "Phase 2: Identify Bottlenecks",
                        "rationale": "4 branches deduplicadas.",
                        "implementation_steps": ["Compactar", "Resumir", "Extrair"],
                        "estimated_minutes_saved_per_week": 38,
                        "priority_score": 33,
                    }
                ],
                "by_project": {
                    "my-proj": [
                        {
                            "id": "my-proj-permission-friction",
                            "scope": "project",
                            "project": "my-proj",
                            "title": "Revisar estratégia de permissões para reduzir falhas recorrentes",
                            "description": "Há erros suficientes para revisão.",
                            "impact": "HIGH",
                            "effort": "Quick",
                            "category": "permissions",
                            "phase": "Phase 3: Optimize Permission Strategy",
                            "rationale": "3 erros em 12 sessões.",
                            "implementation_steps": ["Mapear erros", "Adicionar allows", "Promover padrões"],
                            "estimated_minutes_saved_per_week": 35,
                            "priority_score": 33,
                        }
                    ]
                },
                "top_recommendations": [
                    {
                        "id": "global-context-discipline",
                        "scope": "global",
                        "project": None,
                        "title": "Adotar disciplina operacional de compaction e checkpoints de plano",
                        "description": "Muitas branches deduplicadas.",
                        "impact": "HIGH",
                        "effort": "Quick",
                        "category": "context",
                        "phase": "Phase 2: Identify Bottlenecks",
                        "rationale": "4 branches deduplicadas.",
                        "implementation_steps": ["Compactar", "Resumir", "Extrair"],
                        "estimated_minutes_saved_per_week": 38,
                        "priority_score": 33,
                    },
                    {
                        "id": "my-proj-permission-friction",
                        "scope": "project",
                        "project": "my-proj",
                        "title": "Revisar estratégia de permissões para reduzir falhas recorrentes",
                        "description": "Há erros suficientes para revisão.",
                        "impact": "HIGH",
                        "effort": "Quick",
                        "category": "permissions",
                        "phase": "Phase 3: Optimize Permission Strategy",
                        "rationale": "3 erros em 12 sessões.",
                        "implementation_steps": ["Mapear erros", "Adicionar allows", "Promover padrões"],
                        "estimated_minutes_saved_per_week": 35,
                        "priority_score": 33,
                    }
                ],
            },
            "skills": Counter({"/commit": 8, "handoff": 3}),
            "headless_skills": Counter({"/deploy": 2}),
            "agents": Counter({"dev": 15, "Explore": 10}),
            "runners": Counter({"validate-squad.sh": 20}),
            "tools": Counter({"Edit": 11, "Read": 8, "Bash": 6}),
            "skill_projects": defaultdict(set, {
                "/commit": {"my-proj"}, "handoff": {"my-proj"}, "/deploy": {"my-proj"}
            }),
            "agent_projects": defaultdict(set, {"dev": {"my-proj"}, "Explore": {"my-proj"}}),
            "tool_projects": defaultdict(set, {"Edit": {"my-proj"}, "Read": {"my-proj"}, "Bash": {"my-proj"}}),
            "usage_inventory": {
                "summary": {
                    "normalized_skills": 2,
                    "slash_commands": 2,
                    "skill_tools": 2,
                    "agents": 2,
                    "tools": 3,
                    "runners": 1,
                },
                "normalized_skills": {
                    "entries": [],
                    "top_by_usage": [
                        {
                            "name": "commit",
                            "invocations": 8,
                            "sessions": 5,
                            "projects_count": 1,
                            "interactive_invocations": 8,
                            "headless_invocations": 0,
                            "subagent_invocations": 0,
                            "associated_lines_changed": 90,
                            "associated_tokens": 560,
                            "associated_files_modified": 7,
                            "sessions_with_errors": 1,
                            "error_session_rate": 0.2,
                            "avg_associated_tokens_per_session": 112.0,
                        }
                    ],
                    "top_by_impact": [],
                    "top_by_context_cost": [
                        {
                            "name": "commit",
                            "associated_tokens": 560,
                            "avg_associated_tokens_per_session": 112.0,
                            "sessions": 5,
                            "associated_lines_changed": 90,
                        }
                    ],
                    "top_by_friction": [
                        {
                            "name": "commit",
                            "sessions_with_errors": 1,
                            "error_session_rate": 0.2,
                            "sessions": 5,
                            "associated_tokens": 560,
                        }
                    ],
                },
                "slash_commands": {
                    "entries": [],
                    "top_by_usage": [
                        {
                            "name": "/commit",
                            "invocations": 8,
                            "sessions": 5,
                            "interactive_invocations": 8,
                            "headless_invocations": 0,
                            "subagent_invocations": 0,
                        }
                    ],
                },
                "skill_tools": {
                    "entries": [],
                    "top_by_usage": [
                        {
                            "name": "handoff",
                            "invocations": 3,
                            "sessions": 2,
                            "interactive_invocations": 3,
                            "headless_invocations": 0,
                            "subagent_invocations": 0,
                        }
                    ],
                },
                "agents": {
                    "entries": [],
                    "top_by_usage": [],
                    "top_by_impact": [
                        {
                            "name": "dev",
                            "invocations": 15,
                            "sessions": 9,
                            "associated_lines_changed": 120,
                            "associated_files_modified": 12,
                            "error_session_rate": 0.2,
                        }
                    ],
                    "top_by_context_cost": [
                        {
                            "name": "dev",
                            "associated_tokens": 720,
                            "avg_associated_tokens_per_session": 80.0,
                            "sessions": 9,
                            "associated_lines_changed": 120,
                        }
                    ],
                    "top_by_friction": [],
                },
                "tools": {
                    "entries": [],
                    "top_by_usage": [],
                    "top_by_impact": [],
                    "top_by_context_cost": [
                        {
                            "name": "Edit",
                            "associated_tokens": 840,
                            "avg_associated_tokens_per_session": 105.0,
                            "sessions": 8,
                            "invocations": 11,
                        }
                    ],
                    "top_by_friction": [
                        {
                            "name": "Edit",
                            "sessions_with_errors": 2,
                            "error_session_rate": 0.25,
                            "invocations": 11,
                            "sessions": 8,
                            "associated_tokens": 840,
                        }
                    ],
                },
                "runners": {
                    "entries": [],
                    "top_by_usage": [],
                },
            },
        }
        base.update(overrides)
        return base

    def test_contains_header(self):
        md = format_markdown(self._make_data(), 14)
        self.assertIn("# Claude Code Session Usage Report", md)

    def test_contains_summary_table(self):
        md = format_markdown(self._make_data(), 14)
        self.assertIn("| **my-proj** | 10 | 2 | 5 |", md)
        self.assertIn("| **TOTAL** | **10** | **2** | **5** |", md)

    def test_skills_normalized(self):
        md = format_markdown(self._make_data(), 14)
        # "/commit" should appear as "commit" (normalized)
        self.assertIn("| `commit` |", md)
        # The legacy Top Skills/Commands table should still expose a single normalized row.
        top_skill_rows = [l for l in md.split("\n") if l == "| `commit` | 8 | 0 | my-proj |"]
        self.assertEqual(len(top_skill_rows), 1, f"Expected 1 top-skill row, got: {top_skill_rows}")

    def test_agents_table(self):
        md = format_markdown(self._make_data(), 14)
        self.assertIn("| `dev` | 15 |", md)
        self.assertIn("| `Explore` | 10 |", md)

    def test_runners_table(self):
        md = format_markdown(self._make_data(), 14)
        self.assertIn("| `validate-squad.sh` | 20 |", md)

    def test_unused_skills_section(self):
        tmpdir = tempfile.mkdtemp()
        try:
            os.makedirs(os.path.join(tmpdir, ".claude/skills/commit"), exist_ok=True)
            os.makedirs(os.path.join(tmpdir, ".claude/skills/roundtable"), exist_ok=True)
            os.makedirs(os.path.join(tmpdir, ".claude/skills/tribunal"), exist_ok=True)
            md = format_markdown(self._make_data(), 14, {"test": tmpdir})
            self.assertIn("## Skills NUNCA Usados (test)", md)
            self.assertIn("- `roundtable`", md)
            self.assertIn("- `tribunal`", md)
            # commit is used, should NOT appear
            self.assertNotIn("- `commit`", md)
        finally:
            shutil.rmtree(tmpdir)

    def test_unused_agents_section(self):
        tmpdir = tempfile.mkdtemp()
        try:
            agents_dir = os.path.join(tmpdir, ".claude/agents")
            os.makedirs(agents_dir, exist_ok=True)
            for a in ["dev.md", "qa.md", "ux-design-expert.md"]:
                with open(os.path.join(agents_dir, a), "w") as f:
                    f.write("# agent")
            md = format_markdown(self._make_data(), 14, {"test": tmpdir})
            self.assertIn("## Agents NUNCA Usados", md)
            self.assertIn("- `qa`", md)
            self.assertIn("- `ux-design-expert`", md)
            # dev is used, should NOT appear
            unused_lines = [l for l in md.split("\n") if l.strip() == "- `dev`"]
            self.assertEqual(len(unused_lines), 0)
        finally:
            shutil.rmtree(tmpdir)

    def test_empty_projects(self):
        data = self._make_data(projects={})
        data["summary"] = {
            "total_interactive": 0,
            "total_headless": 0,
            "total_subagents": 0,
            "total_session_files": 0,
            "total_branches": 0,
            "total_branches_deduped": 0,
            "total_user_messages": 0,
            "total_assistant_messages": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_tool_errors": 0,
            "tool_error_categories": Counter(),
            "total_user_interruptions": 0,
            "avg_user_response_seconds": 0,
            "sessions_with_task_agent": 0,
            "sessions_with_mcp": 0,
            "sessions_with_web_search": 0,
            "sessions_with_web_fetch": 0,
            "total_lines_added": 0,
            "total_lines_removed": 0,
            "total_unique_files_modified": 0,
            "session_meta_cache_hits": 0,
            "session_meta_cache_misses": 0,
            "facets_cache_hits": 0,
            "facets_cache_misses": 0,
        }
        data["facet_summary"] = {
            "sessions_with_facets": 0,
            "sources": Counter(),
            "goal_categories": Counter(),
            "outcomes": Counter(),
            "satisfaction": Counter(),
            "friction_points": Counter(),
        }
        data["narrative"] = {}
        data["skills"] = Counter()
        data["headless_skills"] = Counter()
        data["agents"] = Counter()
        data["runners"] = Counter()
        data["tools"] = Counter()
        data["skill_projects"] = defaultdict(set)
        data["agent_projects"] = defaultdict(set)
        data["tool_projects"] = defaultdict(set)
        md = format_markdown(data, 14)
        self.assertIn("| **TOTAL** | **0** | **0** | **0** |", md)

    def test_days_param_reflected(self):
        md = format_markdown(self._make_data(), 30)
        self.assertIn("últimos 30 dias", md)

    def test_contains_session_metrics_and_top_tools(self):
        md = format_markdown(self._make_data(), 14)
        self.assertIn("## Métricas de Sessão", md)
        self.assertIn("| Input tokens | 1.200 |", md)
        self.assertIn("| Cache session-meta (hit/miss) | 9/8 |", md)
        self.assertIn("## Top Tools", md)
        self.assertIn("| `Edit` | 11 | my-proj |", md)
        self.assertIn("## Inventário Operacional", md)
        self.assertIn("### Skills Normalizadas por Uso", md)
        self.assertIn("| `commit` | 8 | 5 | 1 | 90 | 20,0 |", md)
        self.assertIn("### Slash Commands Cruos", md)
        self.assertIn("| `/commit` | 8 | 5 | 8 | 0 | 0 |", md)
        self.assertIn("## Custo de Contexto", md)
        self.assertIn("| `commit` | 560 | 112,0 | 5 | 90 |", md)
        self.assertIn("## Fricção Operacional", md)
        self.assertIn("| `Edit` | 2 | 25,0 | 11 | 8 | 840 |", md)
        self.assertIn("## Facets de Sessão", md)
        self.assertIn("coding (9)", md)
        self.assertIn("## Insights Narrativos", md)
        self.assertIn("### O Que Está Funcionando", md)
        self.assertIn("### No Horizonte", md)
        self.assertIn("### Fechamento", md)
        self.assertIn("Visão geral sintética.", md)
        self.assertIn("## Categorias de Erro de Tool", md)
        self.assertIn("| Command Failed | 2 |", md)


class TestFormatHTML(unittest.TestCase):
    """Tests for format_html()."""

    def _make_data(self):
        return TestFormatMarkdown()._make_data()

    def test_contains_html_shell_and_sections(self):
        html_report = format_html(self._make_data(), 14)
        self.assertIn("<!DOCTYPE html>", html_report)
        self.assertIn("<html lang=\"pt-BR\">", html_report)
        self.assertIn("Session Usage Report", html_report)
        self.assertIn("Top Tools", html_report)
        self.assertIn("Inventário Operacional", html_report)
        self.assertIn("Custo de Contexto", html_report)
        self.assertIn("Fricção Operacional", html_report)
        self.assertIn("Insights Narrativos", html_report)
        self.assertIn("O Que Está Funcionando", html_report)
        self.assertIn("No Horizonte", html_report)
        self.assertIn("Fechamento", html_report)
        self.assertIn("Visão geral sintética.", html_report)

    def test_contains_project_and_metric_values(self):
        html_report = format_html(self._make_data(), 14)
        self.assertIn("my-proj", html_report)
        self.assertIn("1.200", html_report)
        self.assertIn("Cache meta hit/miss", html_report)
        self.assertIn("9/8", html_report)
        self.assertIn("coding (9)", html_report)


class TestNormalizeSkillDedup(unittest.TestCase):
    """Verifies that /commit and commit are merged correctly."""

    def test_slash_and_no_slash_merged(self):
        data = {
            "projects": {"p": {"interactive": 5, "headless": 0, "subagents": 0, "date_range": "x"}},
            "skills": Counter({"/commit": 10, "commit": 5, "/tech-research": 3}),
            "headless_skills": Counter({"commit": 2}),
            "agents": Counter(),
            "runners": Counter(),
            "skill_projects": defaultdict(set, {
                "/commit": {"p"}, "commit": {"p"}, "/tech-research": {"p"}
            }),
            "agent_projects": defaultdict(set),
        }
        md = format_markdown(data, 14)
        # "commit" should appear once with interactive=15 (10+5), headless=2
        lines = [l for l in md.split("\n") if l.startswith("| `commit`")]
        self.assertEqual(len(lines), 1)
        self.assertIn("| 15 |", lines[0])
        self.assertIn("| 2 |", lines[0])

    def test_tech_research_merged(self):
        data = {
            "projects": {"p": {"interactive": 1, "headless": 0, "subagents": 0, "date_range": "x"}},
            "skills": Counter({"/tech-research": 6, "tech-research": 5}),
            "headless_skills": Counter(),
            "agents": Counter(),
            "runners": Counter(),
            "skill_projects": defaultdict(set, {
                "/tech-research": {"a"}, "tech-research": {"b"}
            }),
            "agent_projects": defaultdict(set),
        }
        md = format_markdown(data, 14)
        lines = [l for l in md.split("\n") if l.startswith("| `tech-research`")]
        self.assertEqual(len(lines), 1)
        self.assertIn("11", lines[0])
        self.assertIn("a, b", lines[0])


class TestCLI(unittest.TestCase):
    """End-to-end tests for CLI invocation."""

    def test_help_flag(self):
        script = os.path.join(os.path.dirname(__file__), "session-usage-report.py")
        result = subprocess.run(
            [sys.executable, script, "--help"],
            capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("--days", result.stdout)
        self.assertIn("--output", result.stdout)
        self.assertIn("--repo", result.stdout)
        self.assertIn("--cache-dir", result.stdout)
        self.assertIn("--insights-command", result.stdout)
        self.assertIn("--html-file", result.stdout)

    def test_empty_dir_produces_report(self):
        tmpdir = tempfile.mkdtemp()
        try:
            script = os.path.join(os.path.dirname(__file__), "session-usage-report.py")
            result = subprocess.run(
                [sys.executable, script, "--days", "1", "--projects-dir", tmpdir],
                capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("# Claude Code Session Usage Report", result.stdout)
            self.assertIn("| **TOTAL** | **0** | **0** | **0** |", result.stdout)
        finally:
            shutil.rmtree(tmpdir)

    def test_json_output_valid(self):
        tmpdir = tempfile.mkdtemp()
        try:
            script = os.path.join(os.path.dirname(__file__), "session-usage-report.py")
            result = subprocess.run(
                [sys.executable, script, "--days", "1", "--projects-dir", tmpdir, "--output", "json"],
                capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0)
            parsed = json.loads(result.stdout)
            self.assertIn("report", parsed)
            self.assertIn("summary", parsed)
            self.assertIn("facets", parsed)
            self.assertIn("narrative", parsed)
            self.assertEqual(parsed["summary"]["total_interactive"], 0)
        finally:
            shutil.rmtree(tmpdir)

    def test_with_synthetic_session(self):
        tmpdir = tempfile.mkdtemp()
        try:
            proj_dir = os.path.join(tmpdir, "test-project")
            os.makedirs(proj_dir)
            session_path = os.path.join(proj_dir, "abc123.jsonl")
            with open(session_path, "w") as f:
                f.write(json.dumps({"message": {"content": [
                    {"type": "tool_use", "name": "Skill", "input": {"skill": "commit"}},
                    {"type": "tool_use", "name": "Agent", "input": {"subagent_type": "dev", "prompt": "x"}},
                    {"type": "tool_use", "name": "Bash", "input": {"command": "bash validate-squad.sh"}},
                ]}}) + "\n")

            script = os.path.join(os.path.dirname(__file__), "session-usage-report.py")
            result = subprocess.run(
                [sys.executable, script, "--days", "1", "--projects-dir", tmpdir],
                capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("commit", result.stdout)
            self.assertIn("dev", result.stdout)
            self.assertIn("validate-squad.sh", result.stdout)
        finally:
            shutil.rmtree(tmpdir)

    def test_html_output_written_to_file(self):
        tmpdir = tempfile.mkdtemp()
        try:
            proj_dir = os.path.join(tmpdir, "test-project")
            os.makedirs(proj_dir)
            session_path = os.path.join(proj_dir, "abc123.jsonl")
            with open(session_path, "w") as f:
                f.write(json.dumps({"message": {"content": [
                    {"type": "tool_use", "name": "Skill", "input": {"skill": "commit"}},
                ]}}) + "\n")

            html_path = os.path.join(tmpdir, "report.html")
            script = os.path.join(os.path.dirname(__file__), "session-usage-report.py")
            result = subprocess.run(
                [
                    sys.executable,
                    script,
                    "--days", "1",
                    "--projects-dir", tmpdir,
                    "--output", "html",
                    "--html-file", html_path,
                    "--cache-dir", os.path.join(tmpdir, "cache"),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.strip(), html_path)
            self.assertTrue(os.path.exists(html_path))
            with open(html_path, "r", encoding="utf-8") as f:
                html_report = f.read()
            self.assertIn("<!DOCTYPE html>", html_report)
            self.assertIn("Session Usage Report", html_report)
        finally:
            shutil.rmtree(tmpdir)


class TestBuiltinCommandFilter(unittest.TestCase):
    """Verifies builtin commands are correctly filtered."""

    def test_all_builtins_start_with_slash(self):
        for cmd in BUILTIN_COMMANDS:
            self.assertTrue(cmd.startswith("/"), f"Builtin '{cmd}' missing / prefix")

    def test_common_builtins_present(self):
        for cmd in ["/clear", "/model", "/compact", "/help", "/config"]:
            self.assertIn(cmd, BUILTIN_COMMANDS)


class TestEdgeCases(unittest.TestCase):
    """Edge cases and robustness tests."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_nested_command_name_in_tool_content(self):
        """command-name inside tool_use content blocks should still be found."""
        entries = [
            {"message": {"content": [
                {"type": "text", "text": "Loading <command-name>execute-story</command-name>"},
                {"type": "tool_use", "name": "Read", "input": {"file_path": "/some/file"}},
            ]}}
        ]
        path = os.path.join(self.tmpdir, "nested.jsonl")
        with open(path, "w") as f:
            for e in entries:
                f.write(json.dumps(e) + "\n")
        result = analyze_session(path)
        self.assertEqual(result["slash_commands"]["/execute-story"], 1)

    def test_multiple_commands_in_one_line(self):
        entries = [
            {"message": {"content":
                "<command-name>commit</command-name> and <command-name>deploy</command-name>"
            }}
        ]
        path = os.path.join(self.tmpdir, "multi.jsonl")
        with open(path, "w") as f:
            for e in entries:
                f.write(json.dumps(e) + "\n")
        result = analyze_session(path)
        self.assertEqual(result["slash_commands"]["/commit"], 1)
        self.assertEqual(result["slash_commands"]["/deploy"], 1)

    def test_shell_runner_with_path_prefix(self):
        entries = [
            {"message": {"content": [
                {"type": "tool_use", "name": "Bash", "input": {
                    "command": "squads/sinkra-squad/scripts/sinkra-map.sh --verbose"
                }},
            ]}}
        ]
        path = os.path.join(self.tmpdir, "paths.jsonl")
        with open(path, "w") as f:
            for e in entries:
                f.write(json.dumps(e) + "\n")
        result = analyze_session(path)
        self.assertEqual(result["shell_runners"]["sinkra-map.sh"], 1)

    def test_skill_with_missing_skill_field(self):
        entries = [
            {"message": {"content": [
                {"type": "tool_use", "name": "Skill", "input": {}},
            ]}}
        ]
        path = os.path.join(self.tmpdir, "no_skill.jsonl")
        with open(path, "w") as f:
            for e in entries:
                f.write(json.dumps(e) + "\n")
        result = analyze_session(path)
        self.assertEqual(result["skill_invocations"]["unknown"], 1)


class TestFindProjects(unittest.TestCase):
    """Unit tests for find_projects()."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_discovers_project_dirs(self):
        os.makedirs(os.path.join(self.tmpdir, "proj-a"))
        os.makedirs(os.path.join(self.tmpdir, "proj-b"))
        projects = find_projects(self.tmpdir)
        self.assertIn("proj-a", projects)
        self.assertIn("proj-b", projects)

    def test_empty_dir(self):
        projects = find_projects(self.tmpdir)
        self.assertEqual(projects, {})

    def test_ignores_files(self):
        with open(os.path.join(self.tmpdir, "not-a-project.txt"), "w") as f:
            f.write("x")
        os.makedirs(os.path.join(self.tmpdir, "real-project"))
        projects = find_projects(self.tmpdir)
        self.assertEqual(len(projects), 1)
        self.assertIn("real-project", projects)


class TestJSONOutputNormalization(unittest.TestCase):
    """Verifies JSON output normalizes skills (no /prefix dupes)."""

    def test_json_output_merges_slash_variants(self):
        tmpdir = tempfile.mkdtemp()
        try:
            proj_dir = os.path.join(tmpdir, "test-project")
            os.makedirs(proj_dir)
            session_path = os.path.join(proj_dir, "s1.jsonl")
            with open(session_path, "w") as f:
                # Skill tool invocation (no slash)
                f.write(json.dumps({"message": {"content": [
                    {"type": "tool_use", "name": "Skill", "input": {"skill": "commit"}},
                    {"type": "tool_use", "name": "Skill", "input": {"skill": "commit"}},
                ]}}) + "\n")
                # Slash command invocation (with slash via command-name tag)
                f.write(json.dumps({"message": {"content":
                    "<command-name>commit</command-name>"
                }}) + "\n")

            script = os.path.join(os.path.dirname(__file__), "session-usage-report.py")
            result = subprocess.run(
                [sys.executable, script, "--days", "1", "--projects-dir", tmpdir, "--output", "json"],
                capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0)
            parsed = json.loads(result.stdout)
            skills = parsed["top_skills"]
            # Should have "commit" (normalized), not "/commit"
            self.assertIn("commit", skills)
            self.assertNotIn("/commit", skills)
            # Combined count: 2 (Skill tool) + 1 (slash command) = 3
            self.assertEqual(skills["commit"], 3)
        finally:
            shutil.rmtree(tmpdir)

    def test_json_output_includes_rich_session_metrics(self):
        tmpdir = tempfile.mkdtemp()
        try:
            proj_dir = os.path.join(tmpdir, "test-project")
            os.makedirs(proj_dir)
            session_path = os.path.join(proj_dir, "s1.jsonl")
            with open(session_path, "w") as f:
                f.write(json.dumps({
                    "type": "user",
                    "uuid": "u1",
                    "sessionId": "sess-main",
                    "timestamp": "2026-04-01T10:00:00Z",
                    "message": {"content": [{"type": "text", "text": "Start"}]},
                }) + "\n")
                f.write(json.dumps({
                    "type": "assistant",
                    "uuid": "a1",
                    "parentUuid": "u1",
                    "sessionId": "sess-main",
                    "timestamp": "2026-04-01T10:00:05Z",
                    "message": {
                        "usage": {"input_tokens": 100, "output_tokens": 50},
                        "content": [
                            {
                                "type": "tool_use",
                                "name": "Edit",
                                "input": {
                                    "file_path": "/tmp/a.py",
                                    "old_string": "old",
                                    "new_string": "new\nextra",
                                },
                            },
                            {"type": "tool_result", "is_error": True, "content": "command failed with exit code 1"},
                        ],
                    },
                }) + "\n")
                f.write(json.dumps({
                    "type": "user",
                    "uuid": "u2",
                    "parentUuid": "a1",
                    "sessionId": "sess-main",
                    "timestamp": "2026-04-01T10:00:20Z",
                    "message": {"content": [{"type": "text", "text": "Continue"}]},
                }) + "\n")

            script = os.path.join(os.path.dirname(__file__), "session-usage-report.py")
            result = subprocess.run(
                [sys.executable, script, "--days", "1", "--projects-dir", tmpdir, "--output", "json"],
                capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0)
            parsed = json.loads(result.stdout)
            self.assertEqual(parsed["summary"]["total_tool_errors"], 1)
            self.assertEqual(parsed["summary"]["total_branches"], 1)
            self.assertEqual(parsed["summary"]["projects"]["test-project"]["input_tokens"], 100)
            self.assertEqual(parsed["summary"]["projects"]["test-project"]["unique_files_modified"], 1)
            self.assertIn("goal_categories", parsed["facets"])
            self.assertIn("at_a_glance", parsed["narrative"])
            self.assertEqual(parsed["top_tools"]["Edit"], 1)
            self.assertIn("usage_inventory", parsed)
            self.assertEqual(parsed["usage_inventory"]["summary"]["tools"], 1)
        finally:
            shutil.rmtree(tmpdir)


class TestCLIWithRepo(unittest.TestCase):
    """Tests for --repo flag with inventory analysis."""

    def test_repo_flag_shows_unused_skills(self):
        tmpdir = tempfile.mkdtemp()
        try:
            # Create a fake project dir (no sessions)
            proj_dir = os.path.join(tmpdir, "projects")
            os.makedirs(proj_dir)
            # Create a fake repo with skills
            repo_dir = os.path.join(tmpdir, "repo")
            os.makedirs(os.path.join(repo_dir, ".claude/skills/commit"), exist_ok=True)
            os.makedirs(os.path.join(repo_dir, ".claude/skills/unused-skill"), exist_ok=True)

            script = os.path.join(os.path.dirname(__file__), "session-usage-report.py")
            result = subprocess.run(
                [sys.executable, script, "--days", "1", "--projects-dir", proj_dir,
                 "--repo", repo_dir],
                capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("Skills NUNCA Usados", result.stdout)
            self.assertIn("unused-skill", result.stdout)
        finally:
            shutil.rmtree(tmpdir)


if __name__ == "__main__":
    unittest.main()
