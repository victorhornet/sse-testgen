# Test cases automatically generated by Pynguin (https://www.pynguin.eu).
# Please check them before you use them.
import pytest
import codetiming._timer as module_0

def test_case_0():
    timer_0 = module_0.Timer()
    assert timer_0.text == 'Elapsed time: {:0.4f} seconds'
    assert len(module_0.Timer.timers) == 1
    assert module_0.Timer.text == 'Elapsed time: {:0.4f} seconds'
    timer_1 = timer_0.__enter__()
    assert f'{type(timer_1).__module__}.{type(timer_1).__qualname__}' == 'codetiming._timer.Timer'
    assert timer_1.name is None
    assert timer_1.text == 'Elapsed time: {:0.4f} seconds'
    with pytest.raises(module_0.TimerError):
        timer_0.start()

def test_case_1():
    timer_0 = module_0.Timer()
    assert timer_0.text == 'Elapsed time: {:0.4f} seconds'
    assert len(module_0.Timer.timers) == 1
    assert module_0.Timer.text == 'Elapsed time: {:0.4f} seconds'
    none_type_0 = timer_0.start()

def test_case_2():
    timer_0 = module_0.Timer()
    assert timer_0.text == 'Elapsed time: {:0.4f} seconds'
    assert len(module_0.Timer.timers) == 1
    assert module_0.Timer.text == 'Elapsed time: {:0.4f} seconds'
    timer_1 = timer_0.__enter__()
    assert f'{type(timer_1).__module__}.{type(timer_1).__qualname__}' == 'codetiming._timer.Timer'
    assert timer_1.name is None
    assert timer_1.text == 'Elapsed time: {:0.4f} seconds'
    none_type_0 = timer_0.__exit__()
    assert timer_0.last == pytest.approx(0.00014866599667584524, abs=0.01, rel=0.01)
    assert timer_1.last == pytest.approx(0.00014866599667584524, abs=0.01, rel=0.01)

def test_case_3():
    none_type_0 = None
    timer_0 = module_0.Timer()
    assert timer_0.text == 'Elapsed time: {:0.4f} seconds'
    assert len(module_0.Timer.timers) == 1
    assert module_0.Timer.text == 'Elapsed time: {:0.4f} seconds'
    timer_1 = module_0.Timer(text=none_type_0, logger=none_type_0)
    var_0 = timer_1.__call__(timer_1)
    timer_2 = timer_1.__enter__()
    assert f'{type(timer_2).__module__}.{type(timer_2).__qualname__}' == 'codetiming._timer.Timer'
    assert timer_2.name is None
    assert timer_2.text is None
    assert timer_2.logger is None
    float_0 = timer_2.stop()
    assert float_0 == pytest.approx(0.00019412599795032293, abs=0.01, rel=0.01)
    assert timer_1.last == pytest.approx(0.00019412599795032293, abs=0.01, rel=0.01)
    assert timer_2.last == pytest.approx(0.00019412599795032293, abs=0.01, rel=0.01)
    with pytest.raises(module_0.TimerError):
        timer_2.stop()

@pytest.mark.xfail(strict=True)
def test_case_4():
    str_0 = '7\n5gLUl.u\\"~'
    timer_0 = module_0.Timer(str_0)
    assert timer_0.text == 'Elapsed time: {:0.4f} seconds'
    assert len(module_0.Timer.timers) == 1
    assert module_0.Timer.text == 'Elapsed time: {:0.4f} seconds'
    timer_1 = timer_0.__enter__()
    assert f'{type(timer_1).__module__}.{type(timer_1).__qualname__}' == 'codetiming._timer.Timer'
    assert timer_1.name == '7\n5gLUl.u\\"~'
    assert timer_1.text == 'Elapsed time: {:0.4f} seconds'
    var_0 = timer_0.__eq__(timer_0)
    none_type_0 = timer_0.__exit__()
    assert timer_0.last == pytest.approx(0.00026208299823338166, abs=0.01, rel=0.01)
    assert timer_1.last == pytest.approx(0.00026208299823338166, abs=0.01, rel=0.01)
    var_1 = timer_0.__eq__(timer_0)
    var_1.__getitem__(var_1)

def test_case_5():
    timer_0 = module_0.Timer()
    assert timer_0.text == 'Elapsed time: {:0.4f} seconds'
    assert len(module_0.Timer.timers) == 1
    assert module_0.Timer.text == 'Elapsed time: {:0.4f} seconds'
    with pytest.raises(module_0.TimerError):
        timer_0.stop()

def test_case_6():
    timer_0 = module_0.Timer()
    assert timer_0.text == 'Elapsed time: {:0.4f} seconds'
    assert len(module_0.Timer.timers) == 1
    assert module_0.Timer.text == 'Elapsed time: {:0.4f} seconds'

def test_case_7():
    timer_0 = module_0.Timer()
    assert timer_0.text == 'Elapsed time: {:0.4f} seconds'
    assert len(module_0.Timer.timers) == 1
    assert module_0.Timer.text == 'Elapsed time: {:0.4f} seconds'
    timer_1 = timer_0.__enter__()
    assert f'{type(timer_1).__module__}.{type(timer_1).__qualname__}' == 'codetiming._timer.Timer'
    assert timer_1.name is None
    assert timer_1.text == 'Elapsed time: {:0.4f} seconds'