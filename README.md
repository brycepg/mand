# mand

``python -m`` doesn't run multiple modules. This package to provides a way to easily run multiple modules with the same interpreter.

Running multiple modules on the same interpreter is great when you want side-effects such as
adding hooks to existing libraries without changing them.

# Installation

    pip install mand

# Command-line usage

Call multiple modules:

    mand a b

Where a and b are modules, ``a`` will be executed, then ``b``

Usage with arguments:

    mand "a foo" "b bar"

such that ``foo`` is an argument to module ``a`` and ``bar`` is an argument to module ``b``.

You can also specify module paths or python files:

    mand path/to/my/file.py pdb


You can also run mand via the ``-m`` statement:

    python -m mand "a foo" "b bar"

## API usage

```python
from mand import mand
mand(["a foo", "b foo"])
# Equivalent usage
mand([("a", "foo bar"), ("b", "foo")])
```
