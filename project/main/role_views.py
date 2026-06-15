from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from .models import ManagedModule

User = get_user_model()


def superuser_required(view_func): 
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), '/login/')
        if not request.user.is_superuser:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapper


def _relevant_permissions():
    model_names = ManagedModule.objects.filter(is_active=True).values_list(
        'content_type__model', flat=True
    )
    return (
        Permission.objects
        .filter(content_type__app_label='main', content_type__model__in=model_names)
        .select_related('content_type')
        .order_by('content_type__model', 'codename')
    )


class RoleForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Permissions',
    )

    class Meta:
        model = Group
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['permissions'].queryset = _relevant_permissions()
        if self.instance.pk:
            self.fields['permissions'].initial = self.instance.permissions.all()

    def save(self, commit=True):
        group = super().save(commit=commit)
        if commit:
            group.permissions.set(self.cleaned_data['permissions'])
        return group


class UserRoleForm(forms.Form):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all().order_by('name'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Roles',
    )


@superuser_required
def role_list(request):
    groups = Group.objects.all().order_by('name')
    return render(request, 'admin/role_list.html', {'groups': groups, 'active': 'roles'})


@superuser_required
def role_create(request):
    form = RoleForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Role "{form.instance.name}" created.')
        return redirect('role_list')
    return render(request, 'admin/role_form.html', {'form': form, 'is_new': True, 'active': 'roles'})


@superuser_required
def role_edit(request, pk):
    group = get_object_or_404(Group, pk=pk)
    form = RoleForm(request.POST or None, instance=group)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'Role "{group.name}" updated.')
        return redirect('role_list')
    return render(request, 'admin/role_form.html', {
        'form': form, 'is_new': False, 'group': group, 'active': 'roles',
    })


@superuser_required
def role_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        name = group.name
        group.delete()
        messages.success(request, f'Role "{name}" deleted.')
        return redirect('role_list')
    return render(request, 'admin/confirm_delete.html', {
        'obj': group, 'type': 'Role', 'cancel': 'role_list', 'active': 'roles',
    })


@superuser_required
def user_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'admin/user_list.html', {'users': users, 'active': 'users'})


@superuser_required
def user_role_assign(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    form = UserRoleForm(request.POST or None, initial={'groups': user_obj.groups.all()})
    if request.method == 'POST' and form.is_valid():
        user_obj.groups.set(form.cleaned_data['groups'])
        messages.success(request, f'Roles updated for {user_obj.username}.')
        return redirect('rbac_user_list')
    return render(request, 'admin/user_role_assign.html', {
        'form': form, 'user_obj': user_obj, 'active': 'users',
    })
