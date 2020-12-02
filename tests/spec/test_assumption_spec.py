import openpyxl
from exco import AssumptionSpec, CellLocation
from exco.dereferator import Dereferator


def test_assumption_spec():
    assumption = {
        "name": "left",
        "label": "something"
    }

    assumption_spec = AssumptionSpec.from_dict(assumption)
    assert assumption_spec is not None


def test_assumption_spec_deref():
    assumption = {
        "name": "<<A1>>",
        "label": "something"
    }
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet['A1'] = 'hello'
    dereferator = Dereferator.template_to_spec(workbook=workbook,
                                               anchor=CellLocation(sheet.title, 'A2'))
    assumption_spec = AssumptionSpec.from_dict(assumption).deref(dereferator)
    assert assumption_spec.name == 'hello'
