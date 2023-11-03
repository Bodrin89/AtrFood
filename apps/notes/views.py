from django.shortcuts import render
from .models import Note


def note_view(request, model_name):
    try:
        note = Note.objects.get(name=model_name)
        note = note.text
    except Note.DoesNotExist:
        note = 'Заметки отсутствуют'
    context = {
        'note': note,
    }
    return render(request, 'admin/note.html', context)
