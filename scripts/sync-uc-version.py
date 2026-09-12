#!/usr/bin/env python3

"""Bump the Unity Catalog version pinned in mkdocs.yml (extra.uc.version) and, when
given a local unitycatalog/unitycatalog checkout, sync the dependency versions in
extra.* from that checkout's build.sbt / project/spark-versions.json.

Usage:
  scripts/sync-uc-version.py NEW_VERSION [SRC_DIR] [--dry-run]
  scripts/sync-uc-version.py --latest

  NEW_VERSION  Unity Catalog version to pin, e.g. 0.6.0 (a leading 'v' is stripped)
  SRC_DIR      Optional path to a local unitycatalog/unitycatalog git checkout. When
               given, the script runs `git fetch --tags` + `git checkout vNEW_VERSION`
               there, then reads build.sbt and project/spark-versions.json to sync
               extra.{armeria,delta,hadoop,hibernate,iceberg,java,jcasbin,log4j,scala,
               vertx} (version + any URL derived from it) and check extra.spark.version
               against the highest version listed in project/spark-versions.json's
               "versions" array. A dependency whose version can't be found in build.sbt
               is skipped (left unchanged), not fatal; see the status summary printed at
               the end.
               When omitted, only extra.uc.version and every other "vOLD_VERSION"
               occurrence in the file (extra.uc.github, and the build.sbt /
               spark-versions.json source-link comments) are updated.
  --latest     Fetch the latest unitycatalog/unitycatalog GitHub release and use it as
               NEW_VERSION, asking for confirmation first (in a terminal); pass it
               instead of NEW_VERSION.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

LATEST_RELEASE_URL = "https://api.github.com/repos/unitycatalog/unitycatalog/releases/latest"

REPO_ROOT = Path(__file__).resolve().parent.parent
MKDOCS_YML = REPO_ROOT / "mkdocs.yml"

# extra.<key> -> regex (one capture group) to pull that dependency's version out of build.sbt
BUILD_SBT_PATTERNS = {
    "armeria": r'"com\.linecorp\.armeria"\s*%\s*"armeria"\s*%\s*"([^"]+)"',
    "delta": r'lazy val deltaVersion\s*=\s*sys\.props\.getOrElse\("deltaVersion",\s*"([^"]+)"\)',
    "hadoop": r'lazy val hadoopVersion\s*=\s*sys\.props\.getOrElse\("hadoopVersion",\s*"([^"]+)"\)',
    "hibernate": r'"org\.hibernate\.orm"\s*%\s*"hibernate-core"\s*%\s*"([^"]+)"',
    "iceberg": r'lazy val icebergVersion\s*=\s*"([^"]+)"',
    "java": r'lazy val javacRelease17\s*=\s*Seq\("--release",\s*"(\d+)"\)',
    "jcasbin": r'"org\.casbin"\s*%\s*"jcasbin"\s*%\s*"([^"]+)"',
    "log4j": r'lazy val log4jVersion\s*=\s*"([^"]+)"',
    "scala": r'lazy val scala213\s*=\s*"([^"]+)"',
    "vertx": r'"io\.vertx"\s*%\s*"vertx-core"\s*%\s*"([^"]+)"',
}

# extra.<key> -> function(new_version) -> [(field, new_value), ...] for URLs derived from
# that dependency's version. Keys with no version-derived URL (delta, iceberg, scala) map
# to an empty list.
DERIVED_FIELDS = {
    "armeria": lambda v: [
        ("api", f"https://javadoc.io/doc/com.linecorp.armeria/armeria-javadoc/{v}"),
    ],
    "delta": lambda v: [],
    "hadoop": lambda v: [
        ("api", f"https://hadoop.apache.org/docs/r{v}/api/index.html"),
    ],
    "hibernate": lambda v: [
        ("api", f"https://docs.hibernate.org/orm/{'.'.join(v.split('.')[:2])}/javadocs"),
    ],
    "iceberg": lambda v: [],
    "java": lambda v: [
        ("api", f"https://docs.oracle.com/en/java/javase/{v}/docs/api/java.base"),
        ("spec", f"https://docs.oracle.com/javase/specs/jls/se{v}/html"),
    ],
    "jcasbin": lambda v: [
        ("api", f"https://www.javadoc.io/static/org.casbin/jcasbin/{v}"),
    ],
    "log4j": lambda v: [
        ("manual", f"https://logging.apache.org/log4j/{v.split('.')[0]}.x/manual"),
    ],
    "scala": lambda v: [],
    "vertx": lambda v: [
        ("api", f"https://vertx.io/docs/{v}/apidocs/"),
    ],
}


def die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def warn(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)


def parse_version_tuple(v: str) -> tuple[int, ...]:
    try:
        return tuple(int(p) for p in v.split("."))
    except ValueError:
        die(f"could not parse version '{v}' from spark-versions.json")


def run(cmd, cwd=None) -> str:
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        die(f"`{' '.join(cmd)}` failed:\n{result.stderr.strip()}")
    return result.stdout


def find_version(pattern: str, text: str, what: str) -> tuple[str, int] | tuple[None, None]:
    """Returns (value, 1-based line number) of the first match, or (None, None)."""
    m = re.search(pattern, text)
    if not m:
        warn(f"could not find {what} in build.sbt")
        return None, None
    line_no = text.count("\n", 0, m.start()) + 1
    return m.group(1), line_no


# Matches the "#Lxxx" source-line reference in a block's leading comment, e.g.
#   # https://github.com/unitycatalog/unitycatalog/blob/v0.6.0/build.sbt#L362
#   # https://github.com/unitycatalog/unitycatalog/blob/v0.6.0/project/spark-versions.json#L2
COMMENT_LINE_RE = re.compile(
    r"(# https://github\.com/unitycatalog/unitycatalog/blob/v\S+?#L)(\d+)"
)


def update_comment_line(text: str, block_key: str, new_line_no: int) -> tuple[str, str]:
    """Verify/update the '#Lxxx' source-line reference in extra.<block_key>'s leading
    comment against new_line_no. Returns (new_text, status_message)."""
    m = _block_re(block_key).search(text)
    if not m:
        die(f"could not find 'extra.{block_key}' block in mkdocs.yml")
    block = m.group(0)
    lm = COMMENT_LINE_RE.search(block)
    if not lm:
        return text, "no source-line comment to verify"
    old_line_no = int(lm.group(2))
    if old_line_no == new_line_no:
        return text, f"L{old_line_no} (unchanged)"
    new_block = block[: lm.start()] + f"{lm.group(1)}{new_line_no}" + block[lm.end():]
    new_text = text[: m.start()] + new_block + text[m.end():]
    return new_text, f"L{old_line_no} -> L{new_line_no}"


def fetch_latest_release() -> dict:
    req = urllib.request.Request(
        LATEST_RELEASE_URL,
        headers={"User-Agent": "sync-uc-version.py", "Accept": "application/vnd.github+json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        die(f"GitHub API request for the latest release failed: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        die(f"could not reach the GitHub API: {e.reason}")


def resolve_latest_version() -> str:
    release = fetch_latest_release()
    latest_version = release["tag_name"].lstrip("v")
    current_version = get_block_field(MKDOCS_YML.read_text(), "uc", "version")

    print(f"latest unitycatalog/unitycatalog release: {release['tag_name']} ({release.get('name', '')})")
    print(f"published: {release.get('published_at', '?')}")
    print(f"url: {release.get('html_url', '')}")
    if latest_version == current_version:
        print(f"mkdocs.yml is already pinned to {current_version}")

    if sys.stdin.isatty():
        try:
            answer = input(
                f"Use v{latest_version} as the version to sync mkdocs.yml to? [y/N] "
            ).strip().lower()
        except EOFError:
            answer = ""
        if answer not in ("y", "yes"):
            print("aborted: no changes made")
            sys.exit(0)
    else:
        print(f"non-interactive: proceeding with v{latest_version}")

    return latest_version


def _block_re(block_key: str) -> re.Pattern:
    # A block is the "  <key>:" line plus every following line indented >= 4 spaces
    # (its fields/comments) or blank; it stops at the next 2-space-indented key.
    return re.compile(r"^  " + re.escape(block_key) + r":\n(?:[ \t]{4,}.*\n|\n)*", re.MULTILINE)


def get_block_field(text: str, block_key: str, field: str) -> str:
    m = _block_re(block_key).search(text)
    if not m:
        die(f"could not find 'extra.{block_key}' block in mkdocs.yml")
    fm = re.search(r"    " + re.escape(field) + r":\s*(\S+)", m.group(0))
    if not fm:
        die(f"could not find 'extra.{block_key}.{field}' in mkdocs.yml")
    return fm.group(1)


def print_table(headers: list[str], rows: list[tuple[str, ...]]) -> None:
    widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def fmt_row(cells: tuple[str, ...]) -> str:
        return "  ".join(cell.ljust(widths[i]) for i, cell in enumerate(cells)).rstrip()

    print(fmt_row(tuple(headers)))
    print(fmt_row(tuple("-" * w for w in widths)))
    for row in rows:
        print(fmt_row(row))


def replace_block_field(text: str, block_key: str, field: str, new_value: str) -> str:
    m = _block_re(block_key).search(text)
    if not m:
        die(f"could not find 'extra.{block_key}' block in mkdocs.yml")
    block = m.group(0)
    field_re = re.compile(r"(    " + re.escape(field) + r":).*\n")
    fm = field_re.search(block)
    if not fm:
        die(f"could not find 'extra.{block_key}.{field}' in mkdocs.yml")
    new_block = block[: fm.start()] + f"{fm.group(1)} {new_value}\n" + block[fm.end():]
    return text[: m.start()] + new_block + text[m.end():]


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("new_version", nargs="?", help="Unity Catalog version to pin, e.g. 0.6.0")
    parser.add_argument("src_dir", nargs="?", help="path to a unitycatalog/unitycatalog checkout")
    parser.add_argument("--dry-run", action="store_true", help="print changes without writing mkdocs.yml")
    parser.add_argument(
        "--latest", action="store_true",
        help="fetch the latest unitycatalog/unitycatalog release and use it as NEW_VERSION",
    )
    args = parser.parse_args()

    if args.latest:
        # NEW_VERSION is supplied by --latest, so a lone leftover positional
        # (`--latest /path/to/src`) is SRC_DIR, not an explicit version.
        if args.new_version and args.src_dir:
            parser.error("pass either NEW_VERSION or --latest, not both")
        src_dir_arg = args.new_version
        new_version = resolve_latest_version()
    else:
        if not args.new_version:
            parser.error("new_version is required unless --latest is given")
        new_version = args.new_version.lstrip("v")
        if not re.fullmatch(r"\d+\.\d+\.\d+", new_version):
            die(f"'{args.new_version}' doesn't look like a version (expected X.Y.Z)")
        src_dir_arg = args.src_dir

    original_text = MKDOCS_YML.read_text()
    text = original_text
    old_version = get_block_field(original_text, "uc", "version")

    dep_versions: dict[str, str] = {}
    dep_lines: dict[str, int] = {}
    upstream_spark_version = None
    spark_line_no = None

    if src_dir_arg:
        src_dir = Path(src_dir_arg).expanduser().resolve()
        if not (src_dir / ".git").exists():
            die(f"{src_dir} is not a git checkout")

        print(f"checking out v{new_version} in {src_dir} ...")
        run(["git", "fetch", "--tags", "--quiet"], cwd=src_dir)
        run(["git", "checkout", f"v{new_version}", "--quiet"], cwd=src_dir)

        build_sbt = src_dir / "build.sbt"
        if not build_sbt.exists():
            die(f"{build_sbt} not found")
        sbt_text = build_sbt.read_text()
        for key, pattern in BUILD_SBT_PATTERNS.items():
            version, line_no = find_version(pattern, sbt_text, f"extra.{key}.version")
            if version is not None:
                dep_versions[key] = version
                dep_lines[key] = line_no

        spark_versions_json = src_dir / "project" / "spark-versions.json"
        if not spark_versions_json.exists():
            die(f"{spark_versions_json} not found")
        spark_json_text = spark_versions_json.read_text()
        version_entries = json.loads(spark_json_text).get("versions", [])
        if not version_entries:
            die(f"no 'versions' entries found in {spark_versions_json}")
        upstream_spark_version = max(
            (entry["version"] for entry in version_entries), key=parse_version_tuple
        )
        sm = re.search(r'"version"\s*:\s*"' + re.escape(upstream_spark_version) + r'"', spark_json_text)
        spark_line_no = spark_json_text.count("\n", 0, sm.start()) + 1 if sm else None
    else:
        print("no source checkout given: only bumping extra.uc.version and v-tag references")

    # 1. Bump extra.uc.version, then rewrite every other "vOLD_VERSION" occurrence in the
    #    file: extra.uc.github, and every build.sbt / spark-versions.json source-link
    #    comment under extra.{armeria,delta,hadoop,hibernate,iceberg,java,jcasbin,log4j,scala,spark}.
    text = replace_block_field(text, "uc", "version", new_version)
    old_tag, new_tag = f"v{old_version}", f"v{new_version}"
    tag_occurrences = text.count(old_tag)
    text = text.replace(old_tag, new_tag)

    rows: list[tuple[str, str, str]] = [
        (
            "uc.version",
            "unchanged" if old_version == new_version else f"{old_version} -> {new_version}",
            f"{tag_occurrences} v-tag(s) rewritten",
        )
    ]

    # 2. Sync dependency versions + the URLs derived from them, from build.sbt. A
    #    dependency is skipped (left as-is) when no source checkout was given, or when
    #    its version couldn't be found there.
    for key in BUILD_SBT_PATTERNS:
        if not src_dir_arg:
            rows.append((f"{key}.version", "skipped", "no source checkout given"))
            continue
        new_dep_version = dep_versions.get(key)
        if new_dep_version is None:
            rows.append((f"{key}.version", "skipped", "not found in build.sbt"))
            continue
        old_dep_version = get_block_field(original_text, key, "version")
        text = replace_block_field(text, key, "version", new_dep_version)
        for field, value in DERIVED_FIELDS[key](new_dep_version):
            text = replace_block_field(text, key, field, value)
        text, line_col = update_comment_line(text, key, dep_lines[key])
        if old_dep_version == new_dep_version:
            version_col = f"unchanged ({new_dep_version})"
        else:
            version_col = f"{old_dep_version} -> {new_dep_version}"
        rows.append((f"{key}.version", version_col, line_col))

    # 3. extra.spark.version is a deliberate override above upstream (see the comment in
    #    mkdocs.yml). Always keep the commented-out "# version: X" upstream reference
    #    accurate, but only touch the active pin after asking.
    if upstream_spark_version:
        text = re.sub(
            r"(  spark:\n(?:.*\n)*?    # version:\s*)\S+",
            lambda m: m.group(1) + upstream_spark_version,
            text,
            count=1,
        )
        if spark_line_no is not None:
            text, spark_line_col = update_comment_line(text, "spark", spark_line_no)
        else:
            spark_line_col = "no source-line comment"
        current_pin = get_block_field(text, "spark", "version")
        if current_pin == upstream_spark_version:
            spark_version_col = f"unchanged ({current_pin})"
        else:
            print(
                f"extra.spark.version is pinned to {current_pin}; "
                f"upstream v{new_version} default is {upstream_spark_version}."
            )
            answer = ""
            if sys.stdin.isatty():
                try:
                    answer = input(
                        f"Override extra.spark.version to {upstream_spark_version}? [y/N] "
                    ).strip().lower()
                except EOFError:
                    answer = ""
            if answer in ("y", "yes"):
                text = replace_block_field(text, "spark", "version", upstream_spark_version)
                spark_version_col = f"{current_pin} -> {upstream_spark_version}"
            else:
                spark_version_col = f"kept at {current_pin} (upstream {upstream_spark_version})"
    else:
        spark_version_col = "skipped"
        spark_line_col = "no source checkout given"

    rows.append(("spark.version", spark_version_col, spark_line_col))

    print()
    print("=== update status ===")
    print_table(["FIELD", "VERSION", "NOTES"], rows)

    if args.dry_run:
        print()
        print("--- dry run: mkdocs.yml not written ---")
        return

    MKDOCS_YML.write_text(text)
    print()
    print(f"updated {MKDOCS_YML}")


if __name__ == "__main__":
    main()
