#!/usr/bin/env python3.5
from random import random
import unittest

import stack


class StackTests(unittest.TestCase):

    def test_Stack__init__with_single_float_argument(self):
        random_float = random()
        a_stack = stack.Stack(random_float)
        self.assertEqual(a_stack.pop(), random_float)

    def test_Stack__init__with_list_of_floats_argument(self):
        num_vals = 500
        random_float_list = [random() for _ in range(num_vals)]
        random_float_stack = stack.Stack(random_float_list)
        for val in reversed(random_float_list):
            self.assertEqual(val, random_float_stack.pop())

    def test_Stack__init__with_generator_expression_of_random_floats(self):
        num_vals = 100
        float_list = [random() for _ in range(num_vals)]
        gen_exp = (val for val in float_list)
        float_stack = stack.Stack(gen_exp)
        for val in reversed(float_list):
            self.assertEqual(val, float_stack.pop())

    def test_Stack__init__with_Stack_object_argument(self):
        num_vals = 6
        first_stack = stack.Stack(range(num_vals))
        nested_stack = stack.Stack(first_stack)
        # Initializing a new stack from an existing one reverses the order of the
        # original stack
        first_stack_list = list(reversed([first_stack.pop() for _ in range(num_vals)]))
        nested_stack_list = [nested_stack.pop() for _ in range(num_vals)]
        self.assertEqual(first_stack_list, nested_stack_list)

    def test_Stack__init__raises_TypeError_when_two_or_more_args_passed(self):
        max_num_args = 5
        for ii in range(2, max_num_args):
            self.assertRaises(TypeError, stack.Stack, 
                              *tuple(random() for _ in range(ii)))


    def test_empty_stack_pop_error_occurs_for_stack_with_no_values_ever_pushed(self):
        empty_stack = stack.Stack()
        self.assertRaises(stack.EmptyStackPopError, empty_stack.pop)

    def test_empty_stack_pop_error_occurs_for_stack_with_too_many_pop_calls(self):
        empty_stack = stack.Stack()
        num_vals_pushed = 500 # arbitrary
        for ii in range(num_vals_pushed):
            empty_stack.push(random())
        with self.assertRaises(stack.EmptyStackPopError) as context:
            for ii in range(num_vals_pushed + 1):
                empty_stack.pop()

    def test_protected_value_push_error_occurs_when_SENTINEL_pushed(self):
        empty_stack = stack.Stack()
        self.assertRaises(stack.ProtectedValueError, 
                          empty_stack.push, stack.Stack._SENTINEL)

    def test_push_single_float_and_pop_ensuring_equality_between_val_pushed_and_val_popped(self):
        empty_stack = stack.Stack()
        val = random()
        empty_stack.push(val)
        self.assertEqual(val, empty_stack.pop())

    def test_iterator_protocol_make_list_from_empty_stack_and_ensure_empty(self):
        empty_stack = stack.Stack()
        empty_list = list(empty_stack)
        self.assertEqual(empty_list, [])

    def test_iterator_protocol_make_list_from_nonempty_stack(self):
        num_vals = 100  # arbitrary
        vals = [random() for _ in range(num_vals)]
        val_stack = stack.Stack(vals)
        # Note that pushing each val in vals to the stack and then
        # generating a list from Stack.__iter__ reverses the order
        # of vals
        self.assertEqual(list(reversed(vals)), list(val_stack))

    def test_min_method_on_stack_of_random_floats(self):
        num_vals = 100
        vals = [random() for _ in range(num_vals)]
        a_stack = stack.Stack(vals)
        min_val = min(a_stack)
        self.assertEqual(a_stack.min(), min_val)

    def test_bottom_method_on_stack_of_random_floats(self):
        bottom_val = random()
        num_vals = 1000
        a_stack = stack.Stack(bottom_val)
        for _ in range(num_vals-1):
            a_stack.push(random())
        self.assertEqual(a_stack.bottom(), bottom_val)


if __name__ == '__main__':
    unittest.main()
