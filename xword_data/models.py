from django.db import models
import datetime

class Entry(models.Model):
    entry_text: models.CharField = models.CharField(max_length=50, unique=True) 

class Puzzle(models.Model):
    title: models.CharField | None = models.CharField(max_length=255)
    date: models.DateField         = models.DateField()
    byline: models.CharField       = models.CharField(max_length=255)
    publisher: models.CharField    = models.CharField(max_length=12)

class Clue(models.Model):
    entry: models.ForeignKey    =  models.ForeignKey(Entry,  on_delete=models.CASCADE)
    puzzle: models.ForeignKey   = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    clue_text: models.CharField = models.CharField(max_length=512)
    theme:  bool                = False
