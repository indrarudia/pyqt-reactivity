# pyqt-reactivity

## Description

pyqt-reactivity is a project that aims to provide basic reactivity module for
PyQt widgets.

## Installation

Install the latest version from PyPI:

    pip install -U pyqt-reactivity

## Usage

To use basic reactivity module, see the following example:

```python
from pyqt_reactivity import Ref, computed, ref

# Create a reactive reference.
a = ref(1)
a.watch(lambda v: print("a updated:", v))


# Define a computed function that depends on the reactive reference.
def a_squared(a: Ref[float]) -> float:
    return a.value**2


# Create a computed reference.
b = computed(a_squared, args=(a,))
b.watch(lambda v: print("b updated:", v))

# Update the reactive reference.
a.value = 2
```

See more implementations on [examples](examples/) folder.

## License

[MIT](LICENSE)
