"""Capture aggregate GitHub traffic and distribution data for the project."""
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile


REPOSITORY = "Fangx-AI/awesome-xiaodou"


def github(path="", *, paginate=False):
    endpoint = f"repos/{REPOSITORY}{path}"
    command = ["gh", "api"]
    if paginate:
        command.extend(("--paginate", "--slurp"))
    result = subprocess.run(
        [*command, endpoint], capture_output=True, text=True, encoding="utf-8", timeout=30, check=True,
    )
    return json.loads(result.stdout)


def capture():
    repo = github()
    views = github("/traffic/views")
    clones = github("/traffic/clones")
    release = github("/releases/latest")
    release_pages = github("/releases?per_page=100", paginate=True)
    published_releases = {
        item["tag_name"]: {
            "id": item["id"],
            "published_at_utc": item["published_at"],
            "prerelease": item["prerelease"],
            "assets": {
                asset["name"]: {"id": asset["id"], "download_count": asset["download_count"]}
                for asset in item["assets"]
            },
        }
        for page in release_pages for item in page if not item["draft"]
    }
    return {
        "observed_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "stars": repo["stargazers_count"],
        "forks": repo["forks_count"],
        "traffic": {
            "views": views,
            "clones": clones,
            "popular_paths": github("/traffic/popular/paths"),
            "popular_referrers": github("/traffic/popular/referrers"),
        },
        "latest_release": {
            "tag": release["tag_name"],
            "asset_downloads": {asset["name"]: asset["download_count"] for asset in release["assets"]},
        },
        "published_releases": published_releases,
    }


def save(path, observation):
    history = {"repository": REPOSITORY, "snapshots": {}}
    if path.exists():
        history = json.loads(path.read_text(encoding="utf-8"))
        if history["repository"] != REPOSITORY or not isinstance(history["snapshots"], dict):
            raise ValueError("Output does not contain this repository's metrics history")

    day = observation["observed_at_utc"][:10]
    history["snapshots"][day] = observation
    path.parent.mkdir(parents=True, exist_ok=True)
    out = NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False)
    partial = Path(out.name)
    try:
        with out:
            json.dump(history, out, ensure_ascii=False, indent=2, sort_keys=True)
            out.write("\n")
        partial.replace(path)
    finally:
        partial.unlink(missing_ok=True)
    return day


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("history", type=Path, help="History file, normally kept outside the public checkout")
    args = parser.parse_args()
    try:
        observation = capture()
        day = save(args.history, observation)
    except subprocess.CalledProcessError as exc:
        parser.exit(2, f"GitHub API request failed for {exc.cmd[-1]} (exit {exc.returncode}). History unchanged.\n")
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as exc:
        parser.exit(2, f"Metrics could not be saved ({type(exc).__name__}).\n")

    print(f"{day} UTC | {observation['stars']} stars | "
          f"{observation['traffic']['views']['uniques']} unique repository visitors in the traffic window")


if __name__ == "__main__":
    main()
