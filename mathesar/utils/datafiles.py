from time import time
from io import TextIOWrapper

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.core.files.base import ContentFile

from mathesar.serializers import DataFileSerializer
from mathesar.imports.csv import get_sv_dialect
from mathesar.errors import InvalidTableError
from mathesar.models import DataFile


def create_datafile(request, data):
    header = data.get('header', True)

    if 'paste' in data:
        name = str(int(time())) + '.tsv'
        file = ContentFile(str.encode(data['paste']), name=name)
        created_from = 'paste'
    elif 'file' in data:
        file = data['file']
        created_from = 'file'

    text_file = TextIOWrapper(file.file, encoding='utf-8-sig')
    try:
        dialect = get_sv_dialect(text_file)
    except InvalidTableError:
        raise ValidationError('Unable to tabulate data')

    datafile = DataFile(
        file=file,
        created_from=created_from,
        header=header,
        delimiter=dialect.delimiter,
        escapechar=dialect.escapechar,
        quotechar=dialect.quotechar,
    )
    datafile.save()

    serializer = DataFileSerializer(datafile, context={'request': request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)