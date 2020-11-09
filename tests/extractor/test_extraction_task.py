from exco.extractor.assumption.assumption_result import AssumptionResult
from exco.extractor.extraction_task import ExtractionTaskResult
from exco.extractor.locator.locating_result import LocatingResult


def test_extraction_task_result_failed():
    assert ExtractionTaskResult.fail_locating(key="something",
                                              locating_result=LocatingResult(location=None, is_ok=False)) is not None


def test_extraction_task_assumption_failed():
    assert ExtractionTaskResult.fail_assumptions(key="something",
                                                 locating_result=LocatingResult(location=None, is_ok=False),
                                                 assumption_results={
                                                     "a": AssumptionResult.bad(msg="failed")
                                                 }) is not None