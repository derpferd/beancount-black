import pathlib
import shutil
from typing import List

import pytest
from click.testing import CliRunner

from beancount_black.main import create_backup
from beancount_black.main import main


def test_create_backup(tmp_path: pathlib.Path):
    content = "; my book\n; foobar"
    input_file = tmp_path / "input.bean"
    input_file.write_text(content)
    create_backup(input_file, suffix=".backup")
    backup_file = tmp_path / "input.bean.backup"
    assert backup_file.read_text() == content


def test_create_backup_with_conflicts(tmp_path: pathlib.Path):
    for i in range(5):
        input_file = tmp_path / "input.bean"
        input_file.write_text(str(i))
        create_backup(input_file, suffix=".backup")
    backup_file = tmp_path / "input.bean.backup"
    assert backup_file.read_text() == "0"
    for i in range(1, 4):
        backup_file = tmp_path / f"input.bean.backup.{i}"
        assert backup_file.read_text() == str(i)


@pytest.mark.parametrize(
    "input_files, expected_output_files",
    [
        (["oneline.bean"], ["oneline.bean"]),
        (["simple.bean"], ["simple.bean"]),
        (["cost_and_price.bean"], ["cost_and_price.bean"]),
        (["header_comments.bean"], ["header_comments.bean"]),
        (["sections.bean"], ["sections.bean"]),
        (["column_width.bean"], ["column_width.bean"]),
        (["txn.bean"], ["txn.bean"]),
        (["number_expr.bean"], ["number_expr.bean"]),
        (["tailing_comment.bean"], ["tailing_comment.bean"]),
        (["tailing_comments.bean"], ["tailing_comments.bean"]),
        (["metadata_items.bean"], ["metadata_items.bean"]),
        (["metadata_items.bean"], ["metadata_items.bean"]),
        (["balance.bean"], ["balance.bean"]),
        (["oneline.bean", "simple.bean"], ["oneline.bean", "simple.bean"]),
    ],
)
@pytest.mark.parametrize("stdin_mode", [False, True])
def test_main(
    tmp_path: pathlib.Path,
    fixtures_folder: pathlib.Path,
    input_files: List[pathlib.Path],
    expected_output_files: List[pathlib.Path],
    stdin_mode: bool,
):
    if len(input_files) > 1 and stdin_mode:
        pytest.skip("Stdin does not support multiple files")
    input_file_paths = [fixtures_folder / "input" / input_file for input_file in input_files]
    expected_output_file_paths = [fixtures_folder / "expected_output" / expected_output_file for expected_output_file in expected_output_files]
    tmp_input_files = [tmp_path / f"input{i}.bean" for i in range(len(input_files))]
    for input_file_path, tmp_input_file in zip(input_file_paths, tmp_input_files):
        shutil.copy2(input_file_path, tmp_input_file)
    runner = CliRunner()
    if stdin_mode:
        result = runner.invoke(
            main, ["-s", "-"], input=tmp_input_files[0].read_text(), catch_exceptions=False
        )
    else:
        result = runner.invoke(main, [str(tmp_input_file) for tmp_input_file in tmp_input_files], catch_exceptions=False)
    assert result.exit_code == 0
    if stdin_mode:
        updated_input_contents = [result.stdout]
    else:
        updated_input_contents = [tmp_input_file.read_text() for tmp_input_file in tmp_input_files]
    expected_output_contents = [expected_output_file_path.read_text() for expected_output_file_path in expected_output_file_paths]
    assert updated_input_contents == expected_output_contents
