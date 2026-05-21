import json
from pathlib import Path


def test_pipeline_notebooks_are_valid_json():
    notebook_paths = sorted(Path("examples_pipeline").glob("*.ipynb"))

    assert notebook_paths
    for notebook_path in notebook_paths:
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        assert notebook["nbformat"] == 4
        assert notebook["cells"], f"{notebook_path} has no cells"
