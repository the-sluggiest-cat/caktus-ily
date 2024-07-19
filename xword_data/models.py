from django.db import models
import datetime

class Entry(models.Model):
    entry_text: models.CharField = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.entry_text)

class Puzzle(models.Model):
    title: models.CharField | None = models.CharField(max_length=255)
    date: models.DateField         = models.DateField()
    byline: models.CharField       = models.CharField(max_length=255)
    publisher: models.CharField    = models.CharField(max_length=12)

    def __str__(self):
        return f"Title: {self.title}\nDate: {self.date}\nBy: {self.byline}\nPublisher: {self.publisher}"

class Clue(models.Model):
    entry: models.ForeignKey    =  models.ForeignKey(Entry,  on_delete=models.CASCADE)
    puzzle: models.ForeignKey   = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    clue_text: models.CharField = models.CharField(max_length=512)
    theme:  bool                = False

    def __str__(self):
        return f"Clue: {self.clue_text}\nEntry text: {self.entry.entry_text}"
