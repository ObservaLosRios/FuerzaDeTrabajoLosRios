"""Export a Jupyter notebook to HTML (executed) into docs/ using nbconvert API.

Usage (from repo root):
  .venv/bin/python -m scripts.export_notebook_html \
      --input notebooks/fuerza_trabajo_los_rios.ipynb \
      --output docs/fuerza_trabajo_los_rios.html \
      --no-input
"""
from __future__ import annotations

import argparse
from pathlib import Path

import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor
import traceback


def export(input_path: Path, output_path: Path, hide_inputs: bool = True, kernel_name: str = "python3", timeout: int = 600) -> None:
    input_path = input_path.resolve()
    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    nb = nbformat.read(str(input_path), as_version=4)

    # Execute the notebook so outputs are captured
    ep = ExecutePreprocessor(timeout=timeout, kernel_name=kernel_name)
    try:
        ep.preprocess(nb, {"metadata": {"path": str(input_path.parent)}})
    except Exception:
        logs_dir = Path("logs").resolve()
        logs_dir.mkdir(parents=True, exist_ok=True)
        log_file = logs_dir / "nbconvert_error.txt"
        log_file.write_text(traceback.format_exc(), encoding="utf-8")
        raise

    # Export to HTML (classic template), optionally excluding inputs
    exporter = HTMLExporter()
    exporter.exclude_input = hide_inputs
    body, _resources = exporter.from_notebook_node(nb)

    output_path.write_text(body, encoding="utf-8")
    print(f"✔ Exported to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--show-inputs", action="store_true", help="Include code cells in the HTML output")
    parser.add_argument("--kernel", type=str, default="python3")
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()

    export(
        input_path=Path(args.input),
        output_path=Path(args.output),
        hide_inputs=not args.show_inputs,
        kernel_name=args.kernel,
        timeout=args.timeout,
    )


if __name__ == "__main__":
    main()
