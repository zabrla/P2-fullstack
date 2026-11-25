def org_atual(request):
    return request.user.perfil.organizacao