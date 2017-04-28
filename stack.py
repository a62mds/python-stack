#!/usr/bin/env python3.5
from collections import namedtuple


class EmptyStackPopError(IndexError):
    def __init__(self):
        super().__init__('Trying to pop from an empty stack')


class IncomparableValueError(TypeError):
    pass


class ProtectedValueError(ValueError):
    """Exception raised when a protected value, such as a sentinel value, is
    attempted to be pushed onto a stack.

    Initialization parameters:
        protected_val_name  :str:   name of protected value

    """
    
    def __init__(self, protected_val_name):
        if not isinstance(protected_val_name, str):
            raise ValueError(self.__class__.__name__+
                             '.__init__ expected str arg; got '+
                             type(protected_val_name).__class__.__name__)
        super().__init__("Can't push protected value "+protected_val_name)


StackFrame = namedtuple('StackFrame', ['subframe', 'value'])
"""A StackFrame `frame` in this implementation is a tuple (subframe, value),
where `subframe` is the StackFrame immediately below `frame`, and `value` is
the object stored in `frame`.
"""

class Stack(object):
    """Linked-list implementation of a stack which includes a `min` method
    that runs in constant time, regardless of the depth of the stack.
        
    A Stack object keeps track of only the topmost frame, which is identified
    by the attribute `self.top`. When a Stack object is initialized, its
    `self.top` attribute is assigned the value `Stack._SENTINEL`. A Stack
    object `stack` with stack.top == Stack._SENTINEL is defined as an empty
    Stack, and so each Stack object begins as an empty stack.

    If no arguments are passed to `stack.__init__`, `stack` remains empty until
    `stack.push` is called with an appropriate value. Since the constant time
    `min` method is central to this implementation, successive values must be
    comparable using the `<=` operator. If this is not the case, an
    IncomparableValueError is raised.

    A Stack object may be initialized as an empty stack, as a stack whose topmost
    frame is populated by either a single object or value, or as a multi-frame
    stack whose values are passed to __init__ in an iterable over those values.

    Class attributes:
        Stack._SENTINEL :   bottom frame of every Stack object; a Stack whose 
                            top frame is Stack._SENTINEL is defined to be empty

    Instance attributes:
        self.top    :   topmost stack frame
        self.top_min:   topmost frame of the auxilliary stack of minimum values

    This implementation of a stack uses two stacks: a main stack implemented
    as a linked list of `StackFrame(subframe, value)` namedtuples; and an
    auxilliary stack, implemented in the same way, which contains the
    successively-minimum values pushed onto the stack. For example:

                Operation       Main stack          Aux stack   Comment
        Step 0: stack = Stack() EMPTY               EMPTY       Empty stack init
        Step 1: stack.push(10)  10                  10          first val pushed to aux
        Step 2: stack.push(9)   9->10               9->10       9 <= 10 so 9 pshdto aux
        Step 3: stack.push(11)  11->9->10           9->10       11 > 9 so 11 not pushed
        Step 4: stack.push(0)   0->11->9->10        0->9->10    0 <= 9 so 0 pushdto aux
        Step 4: stack.push(10)  10->0->11->9->10    0->9->10    10 > 0 so 10 not pushed
          ...        ...              ...              ...               ...

    The `stack.min()` method returns `stack.top_min.value`. Its implementation
    consists of simply retrieving the value attribute of the StackFrame
    `stack.top_min`, regardless of the depth of stack, and therefore runs in
    O(1) time.

    """

    _SENTINEL = StackFrame(subframe=(), value=None)
    """
    _SENTINEL is the bottom frame of every Stack object, and a stack whose top
    frame is _SENTINEL is defined to be empty. In this implementation, it is a
    StackFrame with an empty subframe and a value of None. All other
    StackFrames must have a nonempty subframe, so this property alone is enough
    to justify this definition. Note that the value of None is somewhat
    arbitrary.
    """

    def __init__(self, *values):
        """Initializes two empty stacks: the main stack and an auxilliary
        stack of minimum values. Implicit in this implementation is the
        need to be able to compare successive values pushed onto the stack
        using the `<=` operator.

        Parameters:
            (optional) values   :   either a single object or an iterable over
                                    a collection of objects

        Side-effects:
            self.top        :   initialized first to Stack._SENTINEL; if `values`
                                is not None, it is iterated over, pushing each of
                                its objects onto the stack using the Stack.push
                                method
            self.top_min    :   initialized to Stack._SENTINEL and reassigned as
                                appropriate by Stack.push (see the docs for that
                                method for more information)

        Return value:
            None

        Exceptions raised:
            TypeError   :   raised if more than one argument is passed
        """
        # Initialize both the main and auxilliary stacks
        self.top = self.top_min = type(self)._SENTINEL
        if values:
            # If provided, values is expected to be of the form (value,), where
            # `value` is an iterable or a single object
            if not len(values) == 1:
                msg = '{}.__init__ expects at most 2 arguments, {} recieved'
                raise TypeError(msg.format(self.__class__.__name__, len(values)))
            # Unpacking to make things prettier :)
            values, = values
            # If values is iterable, no exception is raised and each value in
            # values is pushed onto the stack
            try:
                for val in values:
                    self.push(val)
            # Otherwise, values is a single value or object
            except TypeError:
                self.push(values)

    @property
    def is_empty(self):
        """Property defining an empty stack. stack.is_empty is True if
        stack.top == _SENTINEL; False otherwise.

        Parameters:
            None

        Side-effects:
            None

        Return type:
            boolean

        Exceptions raised:
            None
        """
        return self.top == type(self)._SENTINEL

    def push(self, new_top):
        """Pushes an element `new_top` onto the top of the stack.

        Parameters:
            new_top :   object comparable to self.top.value via `<=`

        Side-effects:
            self.top    :   reassigned to a new StackFrame with the old
                            self.top as its subframe and new_top as its value,
                            provided new_top isn't a protected value; if it is,
                            a ProtectedValueError is raised
            self.top_min:   if new_top <= self.top_min.value, `self.top_min` is
                            reassigned to a new StackFrame with the old
                            self.top_min as its subframe and new_top as its
                            value
        Return type:
            None

        Exceptions raised:
            ProtectedValueError     :   raised when an attempt is made to push a
                                        protected value onto a Stack
            IncomparableValueError  :   raised when 
        """
        if new_top == type(self)._SENTINEL:
            protected_val_name = self.__class__.__name__ + '._SENTINEL'
            raise ProtectedValueError(protected_val_name)
        # Add a frame with value `new_top` to the main stack
        self.top = StackFrame(subframe=self.top, value=new_top)
        # If appropriate, add a frame with the same value to the auxilliary stack
        try:
            if self.top_min == type(self)._SENTINEL or new_top <= self.top_min.value:
                self.top_min = StackFrame(subframe=self.top_min, value=new_top)
        # If `new_top` cannot be compared with the current minimum value of the main
        # stack using `<=` (i.e. if the statement `new_top <= self.top_min.value`
        # results in a TypeError), raise IncomparableValueError
        except TypeError:
            raise IncomparableValueError

    def pop(self):
        """Pops a value from the top of the stack.

        Parameters:
            None

        Side-effects:
            self.top : reassigned to self.top.subframe if the subframe is not
                       _SENTINEL; if it is, raises EmptyStackPopError

        Return value:
            self.top.value

        Exceptions raised:
            EmptyStackPopError  : raised when pop is called on an empty stack
        """
        if self.is_empty:
            raise EmptyStackPopError
        # Update self.top to the stack frame immediately below itself
        self.top, old_top = self.top
        # If the value being popped from the main stack is equal to the top
        # value of the auxilliary stack, update the aux stack top frame as
        # well
        if self.top_min.value == old_top:
            self.top_min, _ = self.top_min
        return old_top

    def min(self):
        """Returns the minimum value on the stack. Runs in O(1) time.

        Parameters:
            None
        
        Side-effects:
            None

        Return value:
            self.top_min.value

        Exceptions raised:
            None
        """
        return self.top_min.value

    def bottom(self):
        """Returns the value in the bottom stack frame. Relies on the iterator
        protocol to generate a list of the values on the main stack, and returns
        the last value in the list.
        
        Parameters:
            None

        Side-effects:
            None

        Return value:
            list(self)[-1] if stack isn't empty; None if it is

        Exceptions raised:
            None
        """
        return None if self.is_empty else list(self)[-1]

    def __iter__(self):
        """Implementation of the Python iterator protocol. Allows for iteration
        over the values held in a Stack object without altering the Stack itself.
        
        Note about ordering:
        --------------------
        First call to self.__next__() returns the top value stored on the stack;
        the second call returns the value stored in the frame just below the top;
        etc. This means that, for example, list(stack_object) is ordered from top
        to bottom, so that if stack = Stack(iterable), the order of list(stack)
        is the reverse of the order of list(iterable).
        """
        self.iter_curr = self.top
        return self
    def __next__(self):
        if self.iter_curr != type(self)._SENTINEL:
            self.iter_curr, next_value = self.iter_curr
            return next_value
        else:
            raise StopIteration

    def __str__(self):
        return '->'.join(str(value) for value in self)

