import sys
import joblib
import pytest
from joblib._compat import PY27
from joblib.testing import check_subprocess_call


def test_version():
    assert hasattr(joblib, '__version__'), (
        "There are no __version__ argument on the joblib module")


@pytest.mark.skipif(PY27, reason="Need python3.3+")
def test_no_start_method_side_effect_on_import():
    # check that importing joblib does not implicitly set the global
    # start_method for multiprocessing.
    code = """if True:
        import joblib
        import multiprocessing as mp
        # The following line would raise RuntimeError if the
        # start_method is already set.
        mp.set_start_method("loky")
    """
    check_subprocess_call([sys.executable, '-c', code])


@pytest.mark.skipif(PY27, reason="Need python3.3+")
def test_no_semaphore_tracker_on_import():
    # check that importing joblib does not implicitly spawn a ressource tracker
    # or a semaphore tracker
    code = """if True:
        import joblib
        from multiprocessing import semaphore_tracker
        # The following line would raise RuntimeError if the
        # start_method is already set.
        msg = "multiprocessing.semaphore_tracker has been spawned on import"
        assert semaphore_tracker._semaphore_tracker._fd is None, msg"""
    check_subprocess_call([sys.executable, '-c', code])


def test_no_ressource_tracker_on_import():
    code = """if True:
        import joblib
        from joblib.externals.loky.backend import resource_tracker
        # The following line would raise RuntimeError if the
        # start_method is already set.
        msg = "loky.resource_tracker has been spawned on import"
        assert resource_tracker._resource_tracker._fd is None, msg
    """
    check_subprocess_call([sys.executable, '-c', code])