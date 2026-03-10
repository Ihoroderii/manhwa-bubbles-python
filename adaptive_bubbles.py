"""Compatibility shim: forward imports from examples/experiments/adaptive_bubbles."""
try:
    import sys, os
    _exp = os.path.join(os.path.dirname(__file__), 'examples', 'experiments')
    if _exp not in sys.path:
        sys.path.insert(0, _exp)
    from adaptive_bubbles import *  # noqa: F401,F403
except ImportError:
    pass
