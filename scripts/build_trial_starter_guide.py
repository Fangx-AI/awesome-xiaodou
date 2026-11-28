"""Pin the phone-friendly copy pages to the exact trial and public commits."""
import argparse
import re
import subprocess
from pathlib import Path
from urllib.parse import quote

from build_life_plans import PLAN_COPY_DIR, PLAN_FILES, PLAN_STARTER_FILES, ROOT
from verify_candidate import REPOSITORY, read_candidate


def copied_blocks(markdown):
    blocks = {}
    for plan_id, title, text in re.findall(
        r"^## (P\d{2}) · ([^\n]+)\n\n```text\n(.*?)\n```$",
        markdown, re.MULTILINE | re.DOTALL,
    ):
        if plan_id in blocks:
            raise ValueError(f"Repeated copy block: {plan_id}")
        anchor = quote(f"{plan_id.lower()}--{title.lower().replace(' ', '-')}")
        blocks[plan_id] = (title, anchor, text)
    return blocks


def make_guide(copies, candidate, public, repository):
    candidate_root = f"{repository}/blob/{candidate}"
    public_root = f"{repository}/blob/{public}"
    lines = [
        "## 手机可复制的固定开局", "",
        "选一个目标，点开后复制对应代码块。把整段发到小豆独立 App 的新对话。",
        "右侧链接表示该固定公开版本的代码块内容相同。", "",
        f"[自填目标的通用开局]({candidate_root}/README.md#一句话在小豆里开始)", "",
    ]
    covered = set()
    for chapter in PLAN_FILES:
        category = chapter.read_text(encoding="utf-8").splitlines()[0].removeprefix("# ")
        page = PLAN_COPY_DIR / chapter.name
        name = page.relative_to(ROOT).as_posix()
        candidate_blocks = copied_blocks(page.read_text(encoding="utf-8"))
        public_page = subprocess.run(
            ["git", "show", f"{public}:{name}"], cwd=ROOT, capture_output=True, check=False,
        )
        public_blocks = copied_blocks(public_page.stdout.decode("utf-8")) if not public_page.returncode else {}
        if len(candidate_blocks) != 6:
            raise ValueError(f"Expected six copy blocks: {name}")
        lines.extend([f"### {category}", ""])
        for plan_id, (title, anchor, text) in candidate_blocks.items():
            starter = PLAN_STARTER_FILES[plan_id].relative_to(PLAN_COPY_DIR).name
            if plan_id in covered or text + "\n" != (copies / "life-plans" / starter).read_text(encoding="utf-8"):
                raise ValueError(f"Candidate copy block does not match the checked text: {plan_id}")
            covered.add(plan_id)
            public_match = public_blocks.get(plan_id)
            line = f"- [{plan_id} · {title}]({candidate_root}/{name}#{anchor})"
            if public_match and public_match[2] == text:
                line += f" · [同版公开开局]({public_root}/{name}#{public_match[1]})"
            lines.append(line)
        lines.append("")
    if covered != PLAN_STARTER_FILES.keys():
        raise ValueError("The trial guide must contain each life plan once")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--repository", default=REPOSITORY)
    args = parser.parse_args()
    directory = args.directory.resolve()
    candidate = read_candidate(directory)
    guide = make_guide(directory, candidate["candidate_commit"], candidate["public_readme_commit"],
                       args.repository.rstrip("/"))
    (directory / "STARTERS.md").write_text(guide, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
