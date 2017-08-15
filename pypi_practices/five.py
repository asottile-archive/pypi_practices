PY2 = str is bytes
PY3 = str is not bytes

if PY2:  # pragma: no cover (PY2 only)
    text = unicode  # noqa (PY2 only)
    import __builtin__ as builtins  # noqa (Intentionally unused)
else:  # pragma: no cover (PY3 only)
    text = str
    import builtins  # noqa (Intentional unused)
