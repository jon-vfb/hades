from .cvt import CVTEngine

READ = "read"
WRITE = "write"

class TagBinding:

    """
    Class used within Rackio State Machine.

    This class is used to bind tag values with 
    an instance of a Rackio State Machine object,
    in the machine loop, before executing current
    state, tag bindings of an object are updated
    with last values from the Tag Engine, 
    after execution, the Tag Engine is updated,
    the direction of the binding must be provided, 
    otherwise `read` direction is used.

    Usage:

    ```python
    class TwoStep(RackioStateMachine):

        # states

        state1  = State('State1', initial=True)
        state2  = State('State2')

        # transitions
    
        forward = state1.to(state2)
        back = state2.to(state1)

        # bindings

        t1 = TagBinding("T1")
        t2 = TagBinding("T2", direction="write")
    ```
    """

    tag_engine = CVTEngine()

    def __init__(self, tag, direction="read"):
        
        self.tag = tag
        self.direction = direction
        self.value = None

    def update(self):

        if self.direction == WRITE:

            self.tag_engine.write_tag(self.tag, self.value)

        if self.direction == READ:

            self.value = self.tag_engine.read_tag(self.tag)

class Group:

    pass


class GroupBinding:

    """
    Class used within Rackio State Machine.

    This class is used to bind a tag group values 
    with an instance of a Rackio State Machine object,
    in the machine loop, before executing current
    state, group bindings of an object are updated
    with last values of all tags in that group from 
    the Tag Engine, after execution, the Tag Engine 
    is updated, the direction of the binding must be 
    provided, otherwise `read` direction is used.

    Usage:

    ```python
    class TwoStep(RackioStateMachine):

        # states

        state1  = State('State1', initial=True)
        state2  = State('State2')

        # transitions
    
        forward = state1.to(state2)
        back = state2.to(state1)

        # bindings

        g1 = GroupBinding("G1")
        g2 = GroupBinding("G2", direction="write")
    ```
    """
    
    tag_engine = CVTEngine()

    def __init__(self, group, direction="read"):
        
        self.group = group
        self.direction = direction
        self.values = Group()

        self.tags = self.tag_engine.get_group(self.group)

        self._init_group()

    def _init_group(self):

        for tag in self.tags:
            tag_value = self.tag_engine.read_tag(tag)
            setattr(self.values, tag, tag_value)

    def update(self):

        for tag in self.tags:

            if self.direction == WRITE:

                value = getattr(self.values, tag)

                self.tag_engine.write_tag(tag, value)

            if self.direction == READ:

                value = self.tag_engine.read_tag(tag)

                setattr(self.values, tag, value)
