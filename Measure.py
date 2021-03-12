from pathlib import Path
import logging


def measure(measure_template, measure_dict):
    """Measure - mashes up Measure_Template and Measure_Dictionary"""
    """mashup between template and dictionary"""
    measure = None
    my_template = Path(measure_template)
    if my_template.is_file():
        measure_temp = open(my_template, "r").read()
        try:
            measure = measure_temp.format(**measure_dict)
            logging.debug("MeasureSQL [{}]".format(measure))
        except Exception as ex:
            logging.exception("formatting Measure, {} with {}".format(measure_temp, measure_dict))
            raise ex
    else:
        logging.exception("Cannot read measure template {}".format(measure_template))
        raise IOError

    return measure
