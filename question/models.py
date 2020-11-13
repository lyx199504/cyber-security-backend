# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Question(models.Model):
    questionId = models.AutoField(db_column='question_id', primary_key=True)
    content = models.TextField(db_column='content')
    type = models.IntegerField(db_column='type')
    isCorrect = models.IntegerField(db_column='is_correct')
    createTime = models.DateTimeField(db_column='create_time')
    updateTime = models.DateTimeField(db_column='update_time')

    class Meta:
        managed = False
        db_table = 'question'

    @staticmethod
    def allowFields():
        fields = list(map(lambda field: field.name, Question._meta.fields))
        fields.remove('isCorrect')
        return fields

class Option(models.Model):
    optionId = models.AutoField(db_column='option_id', primary_key=True)
    questionId = models.IntegerField(db_column='question_id')
    content = models.TextField(db_column='content')
    isCorrect = models.IntegerField(db_column='is_correct')
    createTime = models.DateTimeField(db_column='create_time')
    updateTime = models.DateTimeField(db_column='update_time')

    class Meta:
        managed = False
        db_table = 'option'
        # unique_together = (('option_id', 'question_id'),)


