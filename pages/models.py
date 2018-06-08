from django.db import models


class Puzzle(models.Model):
    puzzle_blank = models.CharField(max_length=81)
    puzzle_solved = models.CharField(max_length=81)


def image_up_hand(instance, filename):
    return 'uploaded-img/{}'.format(filename)


class UploadedImage(models.Model):
    file = models.ImageField(upload_to=image_up_hand)