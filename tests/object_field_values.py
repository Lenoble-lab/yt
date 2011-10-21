import hashlib
import numpy as na

from yt.utilities.answer_testing.output_tests import \
    YTStaticOutputTest, RegressionTestException, create_test
from yt.funcs import ensure_list
from fields_to_test import field_list, particle_field_list

class FieldHashesDontMatch(RegressionTestException):
    pass

known_objects = {}

def register_object(func):
    known_objects[func.func_name] = func
    return func

@register_object
def centered_sphere(self):
    center = 0.5*(self.pf.domain_right_edge + self.pf.domain_left_edge)
    width = (self.pf.domain_right_edge - self.pf.domain_left_edge).max()
    self.data_object = self.pf.h.sphere(center, width/0.25)

@register_object
def off_centered_sphere(self):
    center = 0.5*(self.pf.domain_right_edge + self.pf.domain_left_edge)
    width = (self.pf.domain_right_edge - self.pf.domain_left_edge).max()
    self.data_object = self.pf.h.sphere(center - 0.25 * width, width/0.25)

@register_object
def corner_sphere(self):
    width = (self.pf.domain_right_edge - self.pf.domain_left_edge).max()
    self.data_object = self.pf.h.sphere(self.pf.domain_left_edge, width/0.25)

@register_object
def all_data(self):
    self.data_object = self.pf.h.all_data()

class YTFieldValuesTest(YTStaticOutputTest):
    def run(self):
        vals = self.data_object[self.field].copy()
        vals.sort()
        self.result = hashlib.sha256(vals.tostring()).hexdigest()

    def compare(self, old_result):
        if self.result != old_result: raise FieldHashesDontMatch

    def setup(self):
        YTStaticOutputTest.setup(self)
        known_objects[self.object_name](self)

for object_name in known_objects:
    for field in field_list + particle_field_list:
        create_test(YTFieldValuesTest, "%s_%s" % (object_name, field),
                    field = field, object_name = object_name)
