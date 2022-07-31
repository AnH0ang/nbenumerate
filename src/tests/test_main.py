from pathlib import Path

import nbformat
from click.testing import CliRunner
from nbformat.notebooknode import NotebookNode
from pytest import fixture

from nbenumerate.main import _enumerate_notebook, _enumerate_text, main
from nbenumerate.version import Version


@fixture
def raw_nb(shared_datadir: Path) -> NotebookNode:
    return nbformat.read(shared_datadir / "raw_notebook.ipynb", as_version=4)


def test_text_enumeration(shared_datadir: Path) -> None:
    version = Version()

    # read in templates from data foldre
    input_text = (shared_datadir / "raw_text.txt").read_text()
    enumerated_text = (shared_datadir / "enumerated_text.txt").read_text()

    # enumerate text
    output_text = _enumerate_text(input_text, version)

    assert enumerated_text == output_text


def test_enumerate_notebook(raw_nb: NotebookNode) -> None:
    enumerated_nb = _enumerate_notebook(raw_nb)

    markdown_cells = [c for c in enumerated_nb["cells"] if c["cell_type"] == "markdown"]
    assert "# 1. Header" in markdown_cells[0]["source"]
    assert "### 2.1.1. Sub Sub Sub" in markdown_cells[2]["source"]


def test_cli(shared_datadir: Path) -> None:
    runner = CliRunner()

    # define paths
    path = str(shared_datadir / "raw_notebook.ipynb")

    # run cli twice
    result_one = runner.invoke(main, [path])
    assert result_one.exit_code == 0
    result_two = runner.invoke(main, [path])
    assert result_two.exit_code == 0

    # read in sorted notebook
    sorted_nb = nbformat.read(path, as_version=4)
    test_enumerate_notebook(sorted_nb)
