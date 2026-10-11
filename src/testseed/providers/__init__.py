"""Stateless value generators.

Every provider is a pure function of a :class:`~testseed._random.Stream` and its
inputs. State (counters, uniqueness) lives in :class:`testseed.TestSeed`, which
keeps providers easy to test and to reuse for future models.
"""
