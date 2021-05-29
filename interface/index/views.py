import uuid
import zipfile
import os

from django.shortcuts import render
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404

from index.models import Refactoring
from index.forms import DynamicForm


def import_refactorings():
    import sys
    import os
    sys.path.append(os.path.dirname(settings.BASE_DIR))
    refactorings_module = __import__('refactorings')  # import code
    utilization_module = __import__('utilization')
    sys.path.pop()
    return refactorings_module, utilization_module


def index(request):
    context = {
        'index': True
    }
    return render(request, 'index/index.html', context)


def retrieve_file_paths(dirName):
    filePaths = []
    for root, directories, files in os.walk(dirName):
        for filename in files:
            filePath = os.path.join(root, filename)
            filePaths.append(filePath)
    return filePaths


def refactoring_detail(request, refactoring_id):
    refactoring = get_object_or_404(Refactoring, id=refactoring_id)
    parameters = refactoring.parameters.all()
    dynamic_fields = []
    for param in parameters:
        dynamic_fields.append({
            'name': param.name,
            'type': param.data_type,
            'hint': param.description
        })
    form = DynamicForm(dynamic_fields=dynamic_fields)
    context = {
        'refactoring': refactoring,
        'form': form,
        'refactorings': True,
    }
    if request.method == "POST":
        form = DynamicForm(request.POST, request.FILES, dynamic_fields=dynamic_fields)
        if form.is_valid():
            # Extract Zip File
            project_file = form.cleaned_data.pop('project_file')
            name = uuid.uuid4().hex[:16]
            dir_path = f'./media/{name}/'
            with zipfile.ZipFile(project_file) as zip_ref:
                zip_ref.extractall(dir_path)
            abs_dir_path = os.path.abspath(dir_path)
            # Create Understand Database
            refactorings, utilization = import_refactorings()
            refactoring_map = refactorings.refactoring_map
            udb_path = utilization.utils.create_understand_database(abs_dir_path)
            # Run Refactoring Main Function
            refactoring_main = refactoring_map.get(refactoring.map_string)
            if refactoring_main:
                refactoring_main.main(udb_path=udb_path, **form.cleaned_data)
                os.remove(udb_path)
                zip_name = os.path.join('./media/', f'{name}.zip')
                with zipfile.ZipFile(zip_name, 'w') as zip_file:
                    for folderName, subfolders, filenames in os.walk(dir_path):
                        for filename in filenames:
                            # create complete filepath of file in directory
                            filePath = os.path.join(folderName, filename)
                            # Add file to zip
                            zip_file.write(filePath, filePath[len(dir_path):])

                with open(zip_name, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='application/force-download')
                    response['Content-Disposition'] = 'attachment; filename="%s"' % 'refactored.zip'
                    return response
            else:
                return Http404("Refactoring not found!")
        else:
            print(form.errors)
    return render(request, 'index/refactoring_detail.html', context)


def about_us(request):
    context = {
        'about_us': True
    }
    return render(request, 'index/about_us.html', context)
