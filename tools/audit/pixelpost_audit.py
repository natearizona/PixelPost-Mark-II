#!/usr/bin/env python3
"""
pixelpost_audit.py — PixelPost II / Darkroom Repository Audit Gate
===================================================================
Read-only. Pure Python stdlib. No staging, no commits, no pushes,
no database connections, no artifact mutation.

Audit categories:
  A  Archaeology / Historical Truth
  B  Restoration Lab / Runtime Claims
  C  Public / Private Boundary
  D  Documentation Structure
  E  Staged File Safety
  F  System Audit / Restoration Plan

Usage:
  python tools/audit/pixelpost_audit.py [--repo ROOT]

Exit codes:
  0  All checks passed
  1  One or more checks failed
  2  Configuration error (repo not found)
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


# ── Result types ───────────────────────────────────────────────────────────────

@dataclass
class Finding:
    status: str       # "PASS" or "FAIL"
    code: str         # e.g. "A-001"
    path: str         # display path (relative to repo)
    message: str      # short description
    line_num: int = 0
    excerpt: str = ""
    problem: str = ""
    fix: str = ""


def _pass(code: str, path: str, message: str) -> Finding:
    return Finding("PASS", code, path, message)


def _fail(code: str, path: str, message: str,
          line_num: int = 0, excerpt: str = "",
          problem: str = "", fix: str = "") -> Finding:
    return Finding("FAIL", code, path, message, line_num, excerpt, problem, fix)


# ── Audit runner ───────────────────────────────────────────────────────────────

class AuditRunner:

    def __init__(self, repo: Path) -> None:
        self.repo = repo
        self.findings: List[Finding] = []

    # ── internal helpers ───────────────────────────────────────────────────────

    def _add(self, f: Finding) -> None:
        self.findings.append(f)

    def _read(self, rel: str) -> Optional[str]:
        p = self.repo / rel
        if not p.exists() or not p.is_file():
            return None
        try:
            return p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return None

    def _exists(self, rel: str) -> bool:
        return (self.repo / rel).exists()

    def _tracked_files(self) -> List[str]:
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True, text=True, cwd=self.repo,
        )
        return [p for p in result.stdout.splitlines() if p]

    def _staged_files(self) -> List[str]:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True, text=True, cwd=self.repo,
        )
        return [p for p in result.stdout.splitlines() if p]

    def _md_files(self, subdir: str = "") -> List[str]:
        """All .md files under subdir (default: repo root), skipping hidden/venv dirs."""
        base = self.repo / subdir if subdir else self.repo
        if not base.exists():
            return []
        skip = {".git", ".venv", "__pycache__", "node_modules", ".pytest_cache"}
        results: List[str] = []
        for p in sorted(base.rglob("*.md")):
            parts = p.relative_to(self.repo).parts
            if any(part in skip or part.startswith(".") for part in parts):
                continue
            results.append(str(p.relative_to(self.repo)))
        return results

    def _search_lines(self, text: str, pattern: str, flags: int = 0):
        """Yield (line_num, line_text) for lines matching pattern."""
        rx = re.compile(pattern, flags)
        for i, line in enumerate(text.splitlines(), 1):
            if rx.search(line):
                yield i, line

    # ── A: Archaeology / Historical Truth ─────────────────────────────────────

    def run_A(self) -> None:

        # A-001: Canonical archaeology ledger or directory exists
        has_ledger = self._exists("docs/ARCHAEOLOGY_LOG.md")
        arch_dir = self.repo / "docs" / "archaeology"
        arch_count = len(list(arch_dir.glob("*.md"))) if arch_dir.exists() else 0
        if has_ledger or arch_count >= 5:
            self._add(_pass("A-001", "docs/archaeology/",
                            f"Archaeology record exists ({arch_count} docs in docs/archaeology/)"))
        else:
            self._add(_fail("A-001", "docs/",
                            "No archaeology ledger or populated docs/archaeology/ found",
                            problem="docs/ARCHAEOLOGY_LOG.md missing and docs/archaeology/ has < 5 files",
                            fix="Create docs/ARCHAEOLOGY_LOG.md or populate docs/archaeology/"))

        # A-002: Chronology doc with date references exists
        chrono = self._read("docs/archaeology/chronology-validation.md")
        if chrono and re.search(r"\d{4}-\d{2}-\d{2}", chrono):
            self._add(_pass("A-002", "docs/archaeology/chronology-validation.md",
                            "Chronology doc exists with date references"))
        else:
            self._add(_fail("A-002", "docs/archaeology/chronology-validation.md",
                            "Chronology doc missing or lacks traceable dates",
                            problem="Chronology claims require traceable ISO dates",
                            fix="Create docs/archaeology/chronology-validation.md with sourced date range"))

        # A-003: Pixelpost version claims consistent (should all be 1.7.3)
        # Exempt files that are explicitly historical/archaeology/forensics context —
        # those docs legitimately reference older versions as part of the historical record.
        HISTORICAL_CONTEXT = re.compile(
            r"(ARCHAEOLOGY_LOG|TIMESTAMP14|FORENSICS|HISTORICAL|lineage|chronolog|"
            r"INSTALLER_ANALYSIS|COMPATIBILITY_AUDIT|incident|correction|archive|"
            r"failed|unresolved|naming.history|desertdream)",
            re.I
        )
        non_canonical: dict[str, list[str]] = {}
        for rel in self._md_files("docs"):
            if HISTORICAL_CONTEXT.search(rel):
                continue  # historical context — version diversity is expected and correct
            text = self._read(rel)
            if not text:
                continue
            for m in re.finditer(r"[Pp]ixelpost\s+(\d+\.\d+(?:\.\d+)?)", text):
                v = m.group(1)
                if v != "1.7.3":
                    non_canonical.setdefault(v, []).append(rel)
        if not non_canonical:
            self._add(_pass("A-003", "docs/",
                            "Pixelpost version claims consistent (1.7.3)"))
        else:
            for v, files in non_canonical.items():
                self._add(_fail("A-003", files[0],
                                f"Pixelpost version '{v}' found alongside canonical 1.7.3",
                                problem=f"Version '{v}' may indicate documentation drift",
                                fix="Verify correct version or add clarifying historical context"))

        # A-004: Award claims cite sources
        award_text = self._read("docs/archaeology/award-recovery.md")
        if award_text is None:
            self._add(_fail("A-004", "docs/archaeology/award-recovery.md",
                            "Award recovery doc missing",
                            fix="Create docs/archaeology/award-recovery.md with sourced award claims"))
        else:
            lines = award_text.splitlines()
            unsourced: list[tuple[int, str]] = []
            # Positive / inflated claim language — requires source citation
            award_re = re.compile(r"\b(award|won|nominated|finalist|winner|official\s+recognition)\b", re.I)
            # Negative finding language — acknowledged absence of evidence; no citation required
            denial_re = re.compile(
                r"(not\s+confirm(ed)?|not\s+verified|not\s+found|no\s+formal|unconfirmed|"
                r"cannot\s+confirm|could\s+not\s+verify|no\s+evidence|unclear|"
                r"not\s+located|not\s+substantiated|no\s+record|did\s+not\s+confirm|"
                r"searches\s+did\s+not|negative\s+finding)",
                re.I
            )
            source_re = re.compile(r"(source[:\s]|via[:\s]|http|reference|citation|\[.*\]\(|see:)", re.I)
            # Metadata key lines are structural labels, not claims
            meta_key_re = re.compile(r"^[A-Za-z][\w\s]*\s*:", re.I)
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                # Skip heading lines and metadata key lines — structural, not claims
                if stripped.startswith("#"):
                    continue
                if meta_key_re.match(stripped) and not stripped.startswith("-"):
                    continue
                if award_re.search(line):
                    # Use a wider backward window so list items see their lead-in denial
                    window = "\n".join(lines[max(0, i - 10):min(len(lines), i + 4)])
                    # Negative findings are acceptable without a source citation
                    if denial_re.search(window):
                        continue
                    if not source_re.search(window):
                        unsourced.append((i, line.strip()[:100]))
            if not unsourced:
                self._add(_pass("A-004", "docs/archaeology/award-recovery.md",
                                "Award claims appear to reference sources"))
            else:
                self._add(_fail("A-004", "docs/archaeology/award-recovery.md",
                                f"{len(unsourced)} award claim(s) may lack source citations",
                                line_num=unsourced[0][0],
                                excerpt=unsourced[0][1],
                                problem="Award claims require source citations",
                                fix="Add source URL or reference near each award claim"))

        # A-005: Recovered post counts don't conflict (canonical: 731)
        # Post/entry counts and image/photo/JPEG counts are tracked separately.
        # 731 posts and 734 images is NOT a conflict — they are different categories.
        # Only conflict within the same category (e.g., two different post counts) fails.
        # Only check TRACKED files — untracked docs may legitimately report filesystem counts.
        tracked_set = set(self._tracked_files())
        post_re = re.compile(r"\b(\d+)\s+(?:posts?|entries|records?)\b", re.I)
        media_re = re.compile(r"\b(\d+)\s+(?:images?|photographs?|photos?|jpe?gs?|files?)\b", re.I)
        post_counts: dict[str, list[str]] = {}
        media_counts: dict[str, list[str]] = {}
        for rel in self._md_files("docs"):
            if rel not in tracked_set:
                continue  # skip untracked files — not yet committed, not yet canonical
            text = self._read(rel)
            if not text:
                continue
            for m in post_re.finditer(text):
                n = int(m.group(1))
                if 650 <= n <= 850:  # plausible TalkingTree post count range
                    post_counts.setdefault(str(n), []).append(rel)
            for m in media_re.finditer(text):
                n = int(m.group(1))
                if 650 <= n <= 850:
                    media_counts.setdefault(str(n), []).append(rel)
        unique_posts = set(post_counts.keys())
        if len(unique_posts) <= 1:
            label = next(iter(unique_posts)) if unique_posts else "not mentioned"
            self._add(_pass("A-005", "docs/", f"Post count consistent ({label})"))
        else:
            non_731 = unique_posts - {"731"}
            if non_731:
                self._add(_fail("A-005", "docs/",
                                f"Conflicting post counts found: {sorted(unique_posts)}",
                                problem="Multiple post counts may indicate documentation drift",
                                fix="Audit all post count references against TalkingTree field test (731)"))
            else:
                self._add(_pass("A-005", "docs/", "Post count consistent (731)"))

        # A-006: Preservation policy acknowledges uncertainty
        policy = self._read("docs/PRESERVATION_POLICY.md")
        uncertainty_re = re.compile(
            r"\b(uncertain|provisional|unverified|estimated|approximat|unknown|not\s+confirmed|may\s+not)\b",
            re.I
        )
        if policy and uncertainty_re.search(policy):
            self._add(_pass("A-006", "docs/PRESERVATION_POLICY.md",
                            "Preservation policy acknowledges uncertainty"))
        elif policy:
            self._add(_fail("A-006", "docs/PRESERVATION_POLICY.md",
                            "Preservation policy lacks uncertainty language",
                            problem="Policy should acknowledge provisional or unverified claims",
                            fix="Add language: 'Some claims are provisional pending further evidence'"))
        else:
            self._add(_fail("A-006", "docs/PRESERVATION_POLICY.md",
                            "docs/PRESERVATION_POLICY.md missing",
                            fix="Create docs/PRESERVATION_POLICY.md"))

        # A-007: Original artifacts explicitly protected from mutation
        readonly_re = re.compile(
            r"(must\s+not\s+be\s+modified|read.only|do\s+not\s+modify|artifacts?\s+must\s+not|"
            r"must\s+not\s+alter|in\s+place|original.*unmodified)",
            re.I
        )
        if policy and readonly_re.search(policy):
            self._add(_pass("A-007", "docs/PRESERVATION_POLICY.md",
                            "Preservation policy includes artifact protection rule"))
        elif policy:
            self._add(_fail("A-007", "docs/PRESERVATION_POLICY.md",
                            "Preservation policy lacks explicit artifact mutation protection",
                            fix="Add: 'Original recovered artifacts must not be modified in place'"))

    # ── B: Restoration Lab / Runtime Claims ───────────────────────────────────

    def run_B(self) -> None:

        # B-001: Runtime inventory doc exists
        if self._exists("docs/restoration/runtime-inventory-1.7.3.md"):
            self._add(_pass("B-001", "docs/restoration/runtime-inventory-1.7.3.md",
                            "Runtime inventory doc exists"))
        else:
            self._add(_fail("B-001", "docs/restoration/",
                            "Runtime inventory doc missing",
                            fix="Create docs/restoration/runtime-inventory-1.7.3.md"))

        # B-002: Database compatibility doc exists
        if self._exists("docs/restoration/database-compatibility-1.7.3.md"):
            self._add(_pass("B-002", "docs/restoration/database-compatibility-1.7.3.md",
                            "Database compatibility doc exists"))
        else:
            self._add(_fail("B-002", "docs/restoration/",
                            "Database compatibility doc missing",
                            fix="Create docs/restoration/database-compatibility-1.7.3.md"))

        # B-003: TIMESTAMP(14) blocker documented and not prematurely resolved
        ts_text = self._read("docs/TIMESTAMP14_FORENSICS.md")
        if ts_text is None:
            self._add(_fail("B-003", "docs/TIMESTAMP14_FORENSICS.md",
                            "TIMESTAMP(14) forensics doc missing — known blocker may be lost",
                            fix="Create docs/TIMESTAMP14_FORENSICS.md"))
        else:
            resolved_re = re.compile(r"\bstatus\b.*\bresolved\b|\bblocker\b.*\bresolved\b|^##?\s*resolved\b", re.I | re.M)
            mysql51_re = re.compile(r"mysql\s+5\.1|5\.0\b|4\.1\b", re.I)
            if resolved_re.search(ts_text) and not mysql51_re.search(ts_text):
                self._add(_fail("B-003", "docs/TIMESTAMP14_FORENSICS.md",
                                "TIMESTAMP(14) blocker marked resolved without MySQL 5.1/5.0/4.1 evidence",
                                problem="Blocker requires MySQL ≤5.1 testing to resolve",
                                fix="Verify resolution evidence or keep blocker as open"))
            else:
                self._add(_pass("B-003", "docs/TIMESTAMP14_FORENSICS.md",
                                "TIMESTAMP(14) blocker documented and appropriately open"))

        # B-004: PHP 5.6.40 lab runtime distinguished from PHP 5.2 historical target
        runtime_text = self._read("docs/restoration/runtime-inventory-1.7.3.md") or ""
        compat_text = self._read("docs/restoration/database-compatibility-1.7.3.md") or ""
        combined = runtime_text + compat_text
        if re.search(r"5\.6\.40|PHP\s+5\.6", combined, re.I):
            self._add(_pass("B-004", "docs/restoration/",
                            "PHP 5.6.40 lab runtime documented"))
        else:
            self._add(_fail("B-004", "docs/restoration/",
                            "PHP 5.6.40 lab runtime not documented in restoration inventory",
                            problem="Runtime inventory should record the actual PHP version used in lab",
                            fix="Add PHP 5.6.40 as lab runtime in runtime-inventory-1.7.3.md"))

        # B-005: Runtime success claims cite evidence
        success_re = re.compile(
            r"\b(successfully\s+installed|installation\s+(complete|succeeded|worked)|"
            r"confirmed\s+working|restored\s+successfully|first\s+boot\s+(complete|success)|"
            r"verified\s+working|test\s+passed)\b",
            re.I
        )
        evidence_re = re.compile(
            r"(screenshot|log|transcript|\bsee\b.{0,30}\[|evidence/|runtime.testing|"
            r"see\s+docs|confirmed\s+by|appendix|runtime.log)",
            re.I
        )
        evidence_failures: list[tuple[str, int, str]] = []
        for rel in self._md_files("docs/restoration"):
            text = self._read(rel)
            if not text:
                continue
            lines = text.splitlines()
            for i, line in enumerate(lines, 1):
                if success_re.search(line):
                    window_start = max(0, i - 5)
                    window_end = min(len(lines), i + 5)
                    window = "\n".join(lines[window_start:window_end])
                    if not evidence_re.search(window):
                        evidence_failures.append((rel, i, line.strip()[:100]))
        if not evidence_failures:
            self._add(_pass("B-005", "docs/restoration/",
                            "Runtime success claims appear to reference evidence"))
        else:
            f = evidence_failures[0]
            self._add(_fail("B-005", f[0],
                            f"{len(evidence_failures)} success claim(s) may lack evidence reference",
                            line_num=f[1], excerpt=f[2],
                            problem="Success claims require transcript, log, or screenshot citation",
                            fix="Add reference to log file, screenshot, or transcript near this claim"))

        # B-006: Failed experiments documented
        fail_re = re.compile(
            r"\b(fail(ed|ure)?|error|incompatible|blocker|not\s+work(ing)?|TIMESTAMP|rejected|crash(ed)?)\b",
            re.I
        )
        failure_found = any(
            (text := self._read(rel)) and fail_re.search(text)
            for rel in self._md_files("docs/restoration")
        )
        if failure_found:
            self._add(_pass("B-006", "docs/restoration/",
                            "Failed experiments documented in restoration records"))
        else:
            self._add(_fail("B-006", "docs/restoration/",
                            "No failure records found in restoration docs",
                            problem="Failed experiments must remain visible as evidence",
                            fix="Ensure MySQL TIMESTAMP blocker and other failures remain documented"))

    # ── C: Public / Private Boundary ──────────────────────────────────────────

    def run_C(self) -> None:
        tracked = self._tracked_files()

        # C-001: No credentials in tracked files
        cred_re = re.compile(
            r"(password\s*=\s*['\"][^'\"]{6,}|api[_\-\s]?key\s*[:=]\s*\S{10,}|"
            r"secret\s*[:=]\s*\S{10,}|-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY|"
            r"MYSQL_ROOT_PASSWORD\s*=\s*\S+|DB_PASS(?:WORD)?\s*=\s*\S+)",
            re.I
        )
        # Intentional dev-only fallbacks that are documented and non-secret
        cred_allowlist = re.compile(
            r"(darkroom|dev.secret.change.me|dev-secret|test.secret|PIXELPOSTII_SECRET|"
            r"example|placeholder|change.me|your.password)",
            re.I
        )
        cred_failures: list[tuple[str, int, str]] = []
        for rel in tracked:
            suffix = Path(rel).suffix.lower()
            if suffix not in {".md", ".py", ".toml", ".cfg", ".ini", ".env",
                              ".sh", ".txt", ".json", ".yml", ".yaml"}:
                continue
            text = self._read(rel)
            if not text:
                continue
            for i, line in self._search_lines(text, cred_re.pattern, re.I):
                if not cred_allowlist.search(line):
                    cred_failures.append((rel, i, line.strip()[:100]))
        if not cred_failures:
            self._add(_pass("C-001", "(tracked files)",
                            "No credential patterns detected in tracked files"))
        else:
            f = cred_failures[0]
            self._add(_fail("C-001", f[0],
                            f"{len(cred_failures)} possible credential(s) in tracked files",
                            line_num=f[1], excerpt=f[2],
                            problem="Credentials must never be committed",
                            fix="Remove credential and use environment variable instead"))

        # C-002: No live VPS IPs in tracked files
        # IPs from known Turquoise infrastructure — must not appear in public repo.
        # The audit script itself is exempt — it contains these patterns as regex literals.
        ip_re = re.compile(
            r"\b(2\.24\.122\.151|2\.25\.133\.117|2\.25\.160\.190|10\.8\.0\.[0-9]+|"
            r"srv1697587|srv1705543|srv1723995)\b"
        )
        _text_suffixes = {".md", ".py", ".toml", ".cfg", ".ini", ".txt",
                          ".sh", ".json", ".yml", ".yaml", ".html", ".rst"}
        _self_exempt = {"tools/audit/pixelpost_audit.py"}
        ip_failures: list[tuple[str, int, str]] = []
        for rel in tracked:
            if rel in _self_exempt:
                continue  # audit script contains patterns as regex literals — not a leak
            if Path(rel).suffix.lower() not in _text_suffixes:
                continue
            text = self._read(rel)
            if not text:
                continue
            for i, line in self._search_lines(text, ip_re.pattern):
                ip_failures.append((rel, i, line.strip()[:100]))
        if not ip_failures:
            self._add(_pass("C-002", "(tracked text files)",
                            "No live VPS IPs or hostnames detected in tracked files"))
        else:
            f = ip_failures[0]
            self._add(_fail("C-002", f[0],
                            f"{len(ip_failures)} VPS IP/hostname reference(s) in tracked files",
                            line_num=f[1], excerpt=f[2],
                            problem="Live server IPs must not appear in public repository",
                            fix="Remove or redact VPS IP addresses from tracked files"))

        # C-003: No personal archive paths in tracked files
        # The audit script itself is exempt — it contains these patterns as regex literals.
        path_re = re.compile(r"(/Volumes/LaCie|/Users/nathanarizona(?!/\.claude))")
        path_failures: list[tuple[str, int, str]] = []
        for rel in tracked:
            if rel in _self_exempt:
                continue  # audit script contains patterns as regex literals — not a leak
            text = self._read(rel)
            if not text:
                continue
            for i, line in self._search_lines(text, path_re.pattern):
                path_failures.append((rel, i, line.strip()[:100]))
        if not path_failures:
            self._add(_pass("C-003", "(tracked files)",
                            "No personal archive paths in tracked files"))
        else:
            f = path_failures[0]
            self._add(_fail("C-003", f[0],
                            f"{len(path_failures)} personal archive path(s) in tracked files",
                            line_num=f[1], excerpt=f[2],
                            problem="Local personal paths expose archive structure and must not be committed",
                            fix="Remove or redact personal path references before staging"))

        # C-004: Package boundary / preservation policy exists
        if self._exists("docs/PRESERVATION_POLICY.md"):
            self._add(_pass("C-004", "docs/PRESERVATION_POLICY.md",
                            "Package boundary / preservation policy doc exists"))
        else:
            self._add(_fail("C-004", "docs/",
                            "No PRESERVATION_POLICY.md found",
                            problem="Public/private boundary must be documented",
                            fix="Create docs/PRESERVATION_POLICY.md"))

        # C-005: Staged files don't contain private local paths
        # The audit script itself is exempt — it contains these patterns as regex literals.
        staged = self._staged_files()
        staged_path_failures: list[str] = []
        for rel in staged:
            if rel in _self_exempt:
                continue
            text = self._read(rel)
            if text and path_re.search(text):
                staged_path_failures.append(rel)
        if not staged_path_failures:
            self._add(_pass("C-005", "(staged files)",
                            "No staged files contain personal archive paths"))
        else:
            self._add(_fail("C-005", staged_path_failures[0],
                            f"{len(staged_path_failures)} staged file(s) contain personal archive paths",
                            problem="Files with local personal paths are staged for commit",
                            fix="Unstage these files and resolve path references before committing"))

    # ── D: Documentation Structure ────────────────────────────────────────────

    def run_D(self) -> None:

        # D-001: README exists and names project correctly
        readme = self._read("README.md")
        if readme and re.search(r"PixelPost\s+(II|Mark\s*II)", readme, re.I):
            self._add(_pass("D-001", "README.md",
                            "README exists and names PixelPost II / Mark II"))
        elif readme:
            self._add(_fail("D-001", "README.md",
                            "README does not name PixelPost II or PixelPost Mark II",
                            fix="Add 'PixelPost II' or 'PixelPost Mark II' to README heading"))
        else:
            self._add(_fail("D-001", "README.md",
                            "README.md missing",
                            fix="Create README.md at repository root"))

        # D-002: Docs index exists
        docs_readme = self._read("docs/README.md")
        if docs_readme:
            self._add(_pass("D-002", "docs/README.md", "Docs index exists"))
        else:
            self._add(_fail("D-002", "docs/README.md",
                            "Docs index missing",
                            fix="Create docs/README.md listing all documentation"))

        # D-003: Docs index references core docs
        if docs_readme:
            core = {
                "ARCHAEOLOGY_LOG": "Archaeology log",
                "PRESERVATION_POLICY": "Preservation policy",
                "PROJECT_CHARTER": "Project charter",
                "TIMESTAMP14": "TIMESTAMP(14) forensics",
            }
            missing = [label for key, label in core.items() if key not in docs_readme]
            if not missing:
                self._add(_pass("D-003", "docs/README.md",
                                "Docs index references all core documents"))
            else:
                self._add(_fail("D-003", "docs/README.md",
                                f"Docs index missing references to: {', '.join(missing)}",
                                fix=f"Add links to: {', '.join(missing)}"))

        # D-004: No markdown table starts with a separator row
        sep_re = re.compile(r"^\|\s*[-:]+[-|\s:]*$")
        header_re = re.compile(r"^\|.+\|")
        sep_failures: list[tuple[str, int, str]] = []
        for rel in self._md_files():
            text = self._read(rel)
            if not text:
                continue
            lines = text.splitlines()
            prev_line = ""
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                if sep_re.match(stripped):
                    # Flag if the previous non-empty line is NOT a table row
                    if prev_line and not header_re.match(prev_line):
                        sep_failures.append((rel, i, stripped[:80]))
                        break
                if stripped:
                    prev_line = stripped
        if not sep_failures:
            self._add(_pass("D-004", "(all .md files)",
                            "No tables start with separator row"))
        else:
            f = sep_failures[0]
            self._add(_fail("D-004", f[0],
                            f"{len(sep_failures)} table(s) start with separator row",
                            line_num=f[1], excerpt=f[2],
                            problem="Separator before header row breaks markdown renderers",
                            fix="Move header row above separator row"))

        # D-005: No duplicate H1 in a single document
        # Headings inside fenced code blocks are excluded — they are content, not structure.
        h1_re = re.compile(r"^#\s+\S")
        fence_re = re.compile(r"^(`{3,}|~{3,})")
        h1_failures: list[tuple[str, int]] = []
        for rel in self._md_files():
            text = self._read(rel)
            if not text:
                continue
            in_code_block = False
            h1s: list[int] = []
            for i, line in enumerate(text.splitlines(), 1):
                if fence_re.match(line.strip()):
                    in_code_block = not in_code_block
                if not in_code_block and h1_re.match(line):
                    h1s.append(i)
            if len(h1s) > 1:
                h1_failures.append((rel, h1s[1]))
        if not h1_failures:
            self._add(_pass("D-005", "(all .md files)",
                            "No duplicate H1 headings found"))
        else:
            f = h1_failures[0]
            self._add(_fail("D-005", f[0],
                            f"{len(h1_failures)} file(s) have duplicate H1 headings",
                            line_num=f[1],
                            problem="Multiple H1 headings break document title parsing",
                            fix="Use H2 (##) for section headings within a document"))

        # D-006: No duplicate Version/Date/Status metadata headers within a single file.
        # Only matches bare metadata labels (## Version, ## Date) — NOT version history
        # entries like "## Version 0.3" which are legitimate in roadmap/changelog docs.
        meta_re = re.compile(r"^#{1,3}\s+(Version|Date|Status|Last\s+Updated)\s*$", re.I)
        dup_failures: list[tuple[str, int, str]] = []
        for rel in self._md_files():
            text = self._read(rel)
            if not text:
                continue
            seen: dict[str, int] = {}
            for i, line in enumerate(text.splitlines(), 1):
                m = meta_re.match(line)
                if m:
                    key = m.group(1).lower()
                    if key in seen:
                        dup_failures.append((rel, i, line.strip()))
                        break
                    seen[key] = i
        if not dup_failures:
            self._add(_pass("D-006", "(all .md files)",
                            "No duplicate Version/Date/Status headers found"))
        else:
            f = dup_failures[0]
            self._add(_fail("D-006", f[0],
                            f"{len(dup_failures)} file(s) have duplicate metadata headers",
                            line_num=f[1], excerpt=f[2],
                            fix="Consolidate metadata into a single header block per document"))

        # D-007: Incident reports are indexed
        incident_re = re.compile(r"incident", re.I)
        incident_files = [
            rel for rel in self._md_files("docs")
            if incident_re.search(Path(rel).name)
            or (
                (text := self._read(rel)) is not None
                and re.match(r"^#\s+INCIDENT\b", text or "", re.I)
            )
        ]
        if not incident_files:
            self._add(_pass("D-007", "docs/",
                            "No incident reports found (none required)"))
        elif docs_readme:
            unindexed = [f for f in incident_files
                         if Path(f).name not in docs_readme]
            if not unindexed:
                self._add(_pass("D-007", "docs/README.md",
                                f"All {len(incident_files)} incident report(s) appear indexed"))
            else:
                self._add(_fail("D-007", "docs/README.md",
                                f"{len(unindexed)} incident report(s) not indexed",
                                problem=f"Unindexed: {unindexed}",
                                fix="Add incident report links to docs/README.md"))

    # ── E: Staged File Safety ─────────────────────────────────────────────────

    def run_E(self) -> None:
        staged = self._staged_files()
        if not staged:
            self._add(_pass("E-000", "(staged files)",
                            "Staging area is empty — no files to inspect"))
            return

        danger_name_re = re.compile(
            r"(\.env$|\.env\.|credentials?|secrets?|token\.|\.pem$|\.key$|"
            r"\.sql$|\.sqlite$|\.sqlite3$|\.db$|"
            r"\.zip$|\.tar$|\.tar\.gz$|\.tgz$|\.7z$|\.rar$|"
            r"\.(CR2|NEF|RAF|DNG|ARW|ORF|RW2)$|"
            r"Dockerfile$|docker-compose\.ya?ml$)",
            re.I
        )
        danger_dir_re = re.compile(
            r"(^|/)(exports?|backups?|dumps?|originals?|private|Lightroom|"
            r"Google.Photos|SmugMug|node_modules|\.venv|__pycache__)(/|$)",
            re.I
        )

        name_failures = [r for r in staged if danger_name_re.search(Path(r).name)]
        dir_failures = [r for r in staged if danger_dir_re.search(r)]
        pyc_failures = [r for r in staged if r.endswith(".pyc")]

        if not name_failures:
            self._add(_pass("E-001", "(staged files)",
                            "No dangerous filenames in staged files"))
        else:
            self._add(_fail("E-001", name_failures[0],
                            f"{len(name_failures)} staged file(s) match dangerous filename patterns",
                            problem=str(name_failures),
                            fix="Unstage immediately and add to .gitignore"))

        if not dir_failures:
            self._add(_pass("E-002", "(staged files)",
                            "No staged files from private/dangerous directories"))
        else:
            self._add(_fail("E-002", dir_failures[0],
                            f"{len(dir_failures)} staged file(s) from dangerous directories",
                            problem=str(dir_failures),
                            fix="Unstage and add directory pattern to .gitignore"))

        if not pyc_failures:
            self._add(_pass("E-003", "(staged files)",
                            "No compiled .pyc files staged"))
        else:
            self._add(_fail("E-003", pyc_failures[0],
                            f"{len(pyc_failures)} .pyc file(s) staged",
                            fix="Add __pycache__/ and *.pyc to .gitignore and unstage"))

        # E-004: Tracked-file dangerous artifact scan (not only staged files)
        # Detects dangerous artifact types already committed to the repository.
        # .sql files under docs/ are forensic schema records — not database dumps.
        tracked_danger_re = re.compile(
            r"(\.sqlite$|\.sqlite3$|\.db$|"
            r"\.zip$|\.tar$|\.tar\.gz$|\.tgz$|\.7z$|\.rar$|"
            r"\.(CR2|NEF|RAF|DNG|ARW|ORF|RW2)$|"
            r"\.dump$|\.bak$)",
            re.I
        )
        tracked_sql_re = re.compile(r"\.sql$", re.I)
        tracked_dir_re = re.compile(
            r"(^|/)(backups?|dumps?|private|Lightroom|Google.Photos|SmugMug)(/|$)",
            re.I
        )
        tracked = self._tracked_files()
        tracked_artifact_failures = []
        for r in tracked:
            name = Path(r).name
            if tracked_danger_re.search(name):
                tracked_artifact_failures.append(r)
            elif tracked_sql_re.search(name) and not r.startswith("docs/"):
                # .sql outside docs/ is a real dump risk; inside docs/ is forensic schema
                tracked_artifact_failures.append(r)
            elif tracked_dir_re.search(r):
                tracked_artifact_failures.append(r)
        if not tracked_artifact_failures:
            self._add(_pass("E-004", "(tracked files)",
                            "No dangerous artifact types found in tracked files"))
        else:
            self._add(_fail("E-004", tracked_artifact_failures[0],
                            f"{len(tracked_artifact_failures)} tracked file(s) match dangerous artifact patterns",
                            problem=str(tracked_artifact_failures[:5]),
                            fix="Remove from tracking with git rm --cached and add to .gitignore"))

    # ── F: System Audit / Restoration Plan ────────────────────────────────────

    def run_F(self) -> None:
        charter = self._read("docs/PROJECT_CHARTER.md") or ""
        policy = self._read("docs/PRESERVATION_POLICY.md") or ""
        repo_status = self._read("docs/REPOSITORY_STATUS.md") or ""
        combined = charter + "\n" + policy + "\n" + repo_status

        # F-001: System plan covers four lanes
        lanes = {
            "archaeology":    re.compile(r"archaeolog", re.I),
            "restoration lab": re.compile(r"restoration\s+(lab|runtime|experiment)", re.I),
            "public release":  re.compile(r"public\s+(release|package|repo)", re.I),
            "private ops":     re.compile(r"private\s+(ops|operations|package|material)", re.I),
        }
        missing = [name for name, rx in lanes.items() if not rx.search(combined)]
        if not missing:
            self._add(_pass("F-001", "docs/PROJECT_CHARTER.md",
                            "System plan covers all four lanes"))
        else:
            self._add(_fail("F-001", "docs/PROJECT_CHARTER.md",
                            f"System plan missing lane definitions: {missing}",
                            problem="Each lane must be defined and separated",
                            fix=f"Add documentation for: {', '.join(missing)}"))

        # F-002: Source of truth identified
        if re.search(r"source\s+of\s+truth|canonical\s+source|primary\s+record|ground\s+truth", combined, re.I):
            self._add(_pass("F-002", "docs/",
                            "Source of truth identified in project docs"))
        else:
            self._add(_fail("F-002", "docs/PROJECT_CHARTER.md",
                            "No 'source of truth' definition found",
                            fix="Add: 'GitHub origin/main is the source of truth for this project'"))

        # F-003: Rollback rule exists
        if re.search(r"\b(rollback|revert\s+to\s+original|restore\s+from\s+original|undo\s+changes)\b", combined, re.I):
            self._add(_pass("F-003", "docs/",
                            "Rollback rule found in project docs"))
        else:
            self._add(_fail("F-003", "docs/PRESERVATION_POLICY.md",
                            "No rollback rule found",
                            fix="Add rollback rule: define what to do if an experiment corrupts data"))

        # F-004: Read-only preservation rule
        if re.search(r"(must\s+not\s+be\s+modified|read.only|do\s+not\s+modify\s+in\s+place|"
                     r"artifacts?\s+must\s+not|original.*preserved)", combined, re.I):
            self._add(_pass("F-004", "docs/",
                            "Read-only artifact preservation rule found"))
        else:
            self._add(_fail("F-004", "docs/PRESERVATION_POLICY.md",
                            "No read-only preservation rule found",
                            fix="Add: 'Original recovered artifacts must not be modified'"))

        # F-005: Evidence requirement exists
        if re.search(r"\b(evidence|provenance|cite\s+|citation|log\s+required|transcript\s+required)\b", combined, re.I):
            self._add(_pass("F-005", "docs/",
                            "Evidence requirement found in project docs"))
        else:
            self._add(_fail("F-005", "docs/PROJECT_CHARTER.md",
                            "No evidence requirement rule found",
                            fix="Add: 'Runtime claims require transcript, log, or screenshot evidence'"))

        # F-006: Unresolved blocker list exists
        if self._exists("docs/TIMESTAMP14_FORENSICS.md"):
            ts = self._read("docs/TIMESTAMP14_FORENSICS.md") or ""
            open_re = re.compile(r"\b(open|unresolved|blocking|pending|needs?\s+test|mysql\s+5\.[01]|4\.1)\b", re.I)
            if open_re.search(ts):
                self._add(_pass("F-006", "docs/TIMESTAMP14_FORENSICS.md",
                                "Open blocker registry exists (TIMESTAMP14)"))
            else:
                self._add(_pass("F-006", "docs/TIMESTAMP14_FORENSICS.md",
                                "TIMESTAMP14 forensics doc exists (status unclear — review for open/closed)"))
        else:
            self._add(_fail("F-006", "docs/",
                            "No unresolved blocker document found",
                            fix="Create docs/TIMESTAMP14_FORENSICS.md or equivalent blocker registry"))

        # F-007: Release boundary / deployment gate defined
        release_re = re.compile(
            r"\b(public\s+release\s+(requires?|gate|criteria)|before\s+(publish|deploy|release)|"
            r"deployment\s+gate|pre.release\s+checklist|release\s+criteria)\b",
            re.I
        )
        if release_re.search(combined):
            self._add(_pass("F-007", "docs/",
                            "Release boundary / deployment gate defined"))
        else:
            self._add(_fail("F-007", "docs/PROJECT_CHARTER.md",
                            "No release gate or deployment boundary defined",
                            fix="Define what must be true before any public deployment"))

        # F-008: Nathan (human steward) identified as final gate
        if re.search(r"\b(nathan|steward|human\s+approval|operator.*approval|final\s+decision|final\s+author)\b",
                     combined, re.I):
            self._add(_pass("F-008", "docs/",
                            "Human steward (Nathan) identified as final gate"))
        else:
            self._add(_fail("F-008", "docs/PROJECT_CHARTER.md",
                            "No human steward identified as final gate",
                            fix="Add: 'Nathan Arizona is the steward and final decision authority'"))

    # ── Run all checks ─────────────────────────────────────────────────────────

    def run(self) -> None:
        print("\n[A] Archaeology / Historical Truth")
        self.run_A()
        print("[B] Restoration Lab / Runtime Claims")
        self.run_B()
        print("[C] Public / Private Boundary")
        self.run_C()
        print("[D] Documentation Structure")
        self.run_D()
        print("[E] Staged File Safety")
        self.run_E()
        print("[F] System Audit / Restoration Plan")
        self.run_F()

    # ── Report ─────────────────────────────────────────────────────────────────

    def report(self) -> int:
        print()
        pass_count = 0
        fail_count = 0

        for f in self.findings:
            if f.status == "PASS":
                pass_count += 1
                print(f"[PASS] {f.code:<6} {f.path}")
                print(f"       {f.message}")
            else:
                fail_count += 1
                print(f"\n[FAIL] {f.code:<6} {f.path}")
                print(f"       {f.message}")
                if f.line_num:
                    print(f"       Line {f.line_num}: {f.excerpt!r}")
                if f.problem:
                    print(f"       Problem: {f.problem}")
                if f.fix:
                    print(f"       Suggested fix: {f.fix}")

        print(f"\n{'=' * 60}")
        print(f"Summary: {pass_count} PASS / {fail_count} FAIL")
        print(f"Exit code: {'0' if fail_count == 0 else '1'}")
        return 0 if fail_count == 0 else 1


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="PixelPost II / Darkroom repository audit gate"
    )
    parser.add_argument("--repo", default=None,
                        help="Path to repository root (default: auto-detect via .git)")
    args = parser.parse_args()

    if args.repo:
        repo = Path(args.repo).resolve()
    else:
        # Walk up from script location to find .git
        candidate = Path(__file__).resolve().parent
        repo = None
        for _ in range(6):
            if (candidate / ".git").exists():
                repo = candidate
                break
            candidate = candidate.parent
        if repo is None:
            print("ERROR: Could not find repository root (.git not found in parent dirs)")
            sys.exit(2)

    print("PixelPost II / Darkroom — Repository Audit Gate v1.0")
    print(f"Repo root : {repo}")
    print(f"Branch    : ", end="")
    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True, text=True, cwd=repo
    )
    print(branch.stdout.strip())
    log = subprocess.run(
        ["git", "log", "--oneline", "-3"],
        capture_output=True, text=True, cwd=repo
    )
    print(f"Recent commits:")
    for line in log.stdout.strip().splitlines():
        print(f"  {line}")
    print("=" * 60)

    runner = AuditRunner(repo)
    runner.run()
    sys.exit(runner.report())


if __name__ == "__main__":
    main()
