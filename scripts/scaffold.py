#!/usr/bin/env python3
"""scaffold.py — 非破坏性生成项目规划文件集。

把 skill 的 assets/ 模板复制到目标项目根，已存在的文件一律跳过，绝不覆盖。
这是「创建模式」的确定性实现：避免 agent 手写时误覆盖用户已有档案（历史 bug F3）。

按项目性质裁剪文件集：
  --type delivery  （默认）生成四件套：AGENTS.md(根) + .plan/{PRD,PLAN,progress}.md
  --type operation        仅生成：AGENTS.md(根) + .plan/progress.md（不生成 PRD/PLAN）

用法:
    python scaffold.py <项目根目录> [--type delivery|operation] [--force-root-agents]
依赖: 本脚本须与 assets/ 同处 skill 目录（scripts/scaffold.py + ../assets/*.md）。
"""
import argparse
import shutil
import sys
from pathlib import Path

# 每种类型在 .plan/ 下生成的文件（AGENTS.md 始终落项目根，单独处理）
PLAN_FILES_BY_TYPE = {
    "delivery": ["PRD.md", "PLAN.md", "progress.md"],
    "operation": ["progress.md"],
}


def main() -> int:
    ap = argparse.ArgumentParser(description="非破坏性生成项目规划文件集")
    ap.add_argument("project_root", help="目标项目根目录（文件落点）")
    ap.add_argument("--type", choices=["delivery", "operation"], default="delivery",
                    help="项目性质：delivery=四件套(默认)，operation=仅 AGENTS+progress")
    ap.add_argument("--force-root-agents", action="store_true",
                    help="即使根已存在 AGENTS.md 也覆盖（默认跳过，绝不静默覆盖）")
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    if not root.is_dir():
        print(f"❌ 项目根不存在或不是目录: {root}")
        return 1

    # assets 目录 = 本脚本上级的 assets/
    assets = (Path(__file__).resolve().parent.parent / "assets")
    if not assets.is_dir():
        print(f"❌ 找不到模板目录: {assets}")
        return 1

    created, skipped = [], []

    # 1) AGENTS.md 放项目根，非破坏性（所有类型都要）
    agents_dst = root / "AGENTS.md"
    agents_src = assets / "AGENTS.md"
    if agents_dst.exists() and not args.force_root_agents:
        skipped.append(str(agents_dst))
    elif agents_src.exists():
        shutil.copyfile(agents_src, agents_dst)
        created.append(str(agents_dst))
    else:
        print(f"⚠️ 模板缺失: {agents_src}")

    # 2) .plan/ 文件集（按类型裁剪）
    plan_files = PLAN_FILES_BY_TYPE[args.type]
    plan_dir = root / ".plan"
    for fn in plan_files:
        src = assets / fn
        dst = plan_dir / fn
        if not src.exists():
            print(f"⚠️ 模板缺失: {src}")
            continue
        if dst.exists():
            skipped.append(str(dst))
            continue
        plan_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        created.append(str(dst))

    # 3) 报告
    print(f"✅ 脚手架完成（type={args.type}）")
    for c in created:
        print(f"   已生成: {c}")
    for s in skipped:
        print(f"   已跳过(存在): {s}")
    if not created:
        print("（无任何新文件生成——目标位置档案已齐全）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
