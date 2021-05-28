from index.models import Refactoring


def refactoring_renderer(request):
    return {
        'all_refactorings': Refactoring.objects.all()
    }
