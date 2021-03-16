class MeasureBase(object):
    def __init__(self):
        self.measure_dict = {}
        self.measure_dict['__CLAIMS_TABLE__'] = 'claims'
        self.measure_dict['__METRICS__'] = 'metrics'
        self.measure_dict['__EFFECTIVE_DATE__'] = "'2020-01-01'" # gotta love py strings!

    def add_to_dict(self, key, value):
        self.measure_dict[key] = value

    def get_dict(self):
        return(self.measure_dict)

class Measure1(MeasureBase):
    def __init__(self):
        """constructor of the class"""
        # call base class to do any initialization ...
        super().__init__()
        super().add_to_dict('__BLAH__', 'bar1')
        super().add_to_dict('__MEASURE__', 'measure1')

class Measure2(MeasureBase):
    def __init__(self):
        """constructor of the class"""
        # call base class to do any initialization ...
        super().__init__()
        super().add_to_dict('__BLAH__', 'foo2')
        super().add_to_dict('__MEASURE__', 'measure2')


if __name__ == '__main__':
    m1 = Measure1()
    m2 = Measure2()

    for measure in [ m1, m2 ]:
        d = measure.get_dict()
        keys = d.keys()
        for key in keys:
            print ('key: {}, value: {}'.format(key, d[key]))
