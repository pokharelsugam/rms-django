from django.shortcuts import render, get_object_or_404, redirect
from .models import Ingredient, IngredientUsage
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import IngredientForm, IngredientUsageForm

def inventory_management(request):
    return render(request, 'inventory-management.html')

@login_required
def ingredient(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'ingredient.html', {'ingredients': ingredients})

@login_required
def ingredient_detail(request, pk):
    if not (request.user.is_admin or request.user.is_manager or request.user.is_chef):
        raise PermissionDenied
    ingredient = get_object_or_404(Ingredient, id=pk)
    return render(request, 'ingredient-detail.html', {'ingredient': ingredient})

@login_required
def ingredient_add(request):
    if not (request.user.is_admin or request.user.is_manager or request.user.is_chef):
        raise PermissionDenied
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredient')
    else:
        form = IngredientForm()
    return render(request, 'ingredient-add-edit.html', {'form': form})

@login_required
def ingredient_edit(request, pk):
    if not (request.user.is_admin or request.user.is_manager or request.user.is_chef):
        raise PermissionDenied
    ingredient = get_object_or_404(Ingredient, id=pk)
    if request.method == 'POST':
        form = IngredientForm(request.POST, instance=ingredient)
        if form.is_valid():
            form.save()
            return redirect('ingredient')
    else:
        form = IngredientForm(instance=ingredient)
    return render(request, 'ingredient-add-edit.html', {'form': form})

@login_required
def ingredient_delete(request, pk):
    if not (request.user.is_admin or request.user.is_manager or request.user.is_chef):
        raise PermissionDenied
    ingredient = get_object_or_404(Ingredient, id=pk)
    if request.method == 'POST':
        ingredient.delete()
        return redirect('ingredient')
    return render(request, 'ingredient-delete-confirm.html', {'ingredient': ingredient})

@login_required
def ingredientusage(request):
    usages = IngredientUsage.objects.all()
    return render(request, 'ingredientusage.html', {'usages': usages})

@login_required
def ingredientusage_detail(request, pk):
    if not (request.user.is_admin or request.user.is_manager or request.user.is_chef):
        raise PermissionDenied
    usage = get_object_or_404(IngredientUsage, id=pk)
    return render(request, 'ingredientusage-detail.html', {'usage': usage})

@login_required
def ingredientusage_add(request):
    if not (request.user.is_admin or request.user.is_manager or request.user.is_chef):
        raise PermissionDenied
    if request.method == 'POST':
        form = IngredientUsageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredient')
    else:
        form = IngredientUsageForm()
    return render(request, 'ingredientusage-add-edit.html', {'form': form})

@login_required
def ingredientusage_edit(request, pk):
    if not (request.user.is_admin or request.user.is_manager or request.user.is_chef):
        raise PermissionDenied
    usage = get_object_or_404(IngredientUsage, id=pk)
    if request.method == 'POST':
        form = IngredientUsageForm(request.POST, instance=usage)
        if form.is_valid():
            form.save()
            return redirect('ingredient')
    else:
        form = IngredientUsageForm(instance=usage)
    return render(request, 'ingredientusage-add-edit.html', {'form': form})

@login_required
def ingredientusage_delete(request, pk):
    if not (request.user.is_admin or request.user.is_manager or request.user.is_chef):
        raise PermissionDenied
    usage = get_object_or_404(IngredientUsage, id=pk)
    if request.method == 'POST':
        usage.delete()
        return redirect('ingredientusage')
    return render(request, 'ingredientusage-delete-confirm.html', {'usage': usage})
