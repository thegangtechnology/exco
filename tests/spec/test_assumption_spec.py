from exco import AssumptionSpec


def test_assumption_spec():
    assumption = {
        "name": "left",
        "label": "something"
    }

    assumption_spec = AssumptionSpec.from_dict(assumption)
    assert assumption_spec is not None
