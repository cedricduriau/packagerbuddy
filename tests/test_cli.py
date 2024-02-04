# third party
import pytest

# package
from packagerbuddy import cli


def test_run():
    with pytest.raises(SystemExit) as exc:
        cli.run(["-h"])

    assert exc.value.code == 0


@pytest.mark.parametrize("args", [([]), (["-!"])])
def test_run_no_action(args: list[str]):
    with pytest.raises(SystemExit) as exc:
        cli.run(args)

    assert exc.value.code == 2
