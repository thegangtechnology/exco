import exco
from os.path import join, dirname


def test_dynamic_locator():
    processor = exco.from_excel(
        join(dirname(__file__), '../../sample/test/dynamic_location/dynamic_location_template.xlsx'))
    datafile = join(dirname(
        __file__), '../../sample/test/dynamic_location/dynamic_location_data.xlsx')

    result = processor.process_excel(datafile)
    assert result.to_dict() == {'marker_value': 2, 'below_marker_value': 'below_marker'}
