from copy import copy
from functools import wraps
from typing import Callable, List, Optional, Literal
from ..calculus import Sq, Tm, Cn, Prf

def instance_rule(side: Literal["ant", "suc"], instance: type, label: str): # pylint: disable=unsubscriptable-object
    """This function is a decorator which compose over the internal rule representation."""
    def decorator(func: Callable[[Sq, Tm], List[Sq]]):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Optional[Prf]: # pylint: disable=unsubscriptable-object
            sq = copy(args[0])
            matchid = None
            for id, x in enumerate(getattr(sq, side).inner):
                if isinstance(x, instance):
                    matchid = id
                    break
            else:
                return None
            match = getattr(sq, side).inner.pop(matchid)
            return Prf(args[0], func(sq, match), label)
        return wrapper
    return decorator

def assert_arity(arity: int):
    """Helper decorator to bail if any matched connective has the wrong arity.

    This would mean that something is wrong in the code.
    """
    def decorator(func: Callable[[Sq, Tm], List[Sq]]):
        @wraps(func)
        def wrapper(*args, **kwargs):
            assert len(args[1].tms) == arity
            return func(*args, **kwargs)
        return wrapper
    return decorator

@assert_arity(1)
def u1(sq: Sq, x: Cn) -> List[Sq]:
    sq.suc.inner.append(x.tms[0])
    return [sq]

@assert_arity(1)
def u2(sq: Sq, x: Cn) -> List[Sq]:
    sq.ant.inner.append(x.tms[0])
    return [sq]

@assert_arity(2)
def b1(sq: Sq, x: Cn) -> List[Sq]:
    sq.ant.inner.append(x.tms[0])
    return [sq]

@assert_arity(2)
def b2(sq: Sq, x: Cn) -> List[Sq]:
    sq.ant.inner.append(x.tms[1])
    return [sq]
    
@assert_arity(2)
def b3(sq: Sq, x: Cn) -> List[Sq]:
    sq2 = copy(sq)
    sq.suc.inner.append(x.tms[0])
    sq2.suc.inner.append(x.tms[1])
    return [sq, sq2]
    
@assert_arity(2)
def b4(sq: Sq, x: Cn) -> List[Sq]:
    sq.suc.inner.append(x.tms[0])
    return [sq]
    
@assert_arity(2)
def b5(sq: Sq, x: Cn) -> List[Sq]:
    sq.suc.inner.append(x.tms[1])
    return [sq]
    
@assert_arity(2)
def b6(sq: Sq, x: Cn) -> List[Sq]:
    sq2 = copy(sq)
    sq.ant.inner.append(x.tms[0])
    sq2.ant.inner.append(x.tms[1])
    return [sq, sq2]