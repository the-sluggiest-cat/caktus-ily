from django.test import TestCase

from .factories import ClueFactory, EntryFactory, PuzzleFactory


class TestXWordModels(TestCase):

    # S: using "str()" to get the repr is a bad idea
    # consider using "repr()" instead, as it's unlikely to have
    # been touched in any way by the developer (compared to
    # __str__())

    def test_clue(self):
        clue = ClueFactory()
        string_repr = str(clue)
        self.assertTrue(clue.entry.entry_text in string_repr)
        self.assertTrue(clue.clue_text in string_repr)

    def test_entry(self):
        entry = EntryFactory()
        string_repr = str(entry)
        self.assertTrue(entry.entry_text in string_repr)

    def test_puzzle(self):
        puzzle = PuzzleFactory()
        string_repr = str(puzzle)
        self.assertTrue(puzzle.publisher in string_repr)
        self.assertTrue(str(puzzle.date) in string_repr)
