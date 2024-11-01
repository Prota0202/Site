from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET, require_http_methods
import json
from .models import User


def create_user(request):
    # Remplace par des valeurs de requête si tu veux gérer des données dynamiques
    username = "new_user"
    password = "secure_password"
    user_id = User.create_user(username, password)
    return JsonResponse({'message': 'Utilisateur créé avec succès', 'user_id': str(user_id)})


def get_user(request, user_id):
    user = User.get_user(user_id)
    if user:
        return JsonResponse(user)
    return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)


def update_user(request, user_id):
    new_data = {
        "username": "updated_username",  # Remplace par des valeurs dynamiques si besoin
        "password": "new_password"
    }
    result = User.update_user(user_id, new_data)
    if result.matched_count > 0:
        return JsonResponse({'message': 'Utilisateur mis à jour avec succès'})
    return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)


def delete_user(request, user_id):
    result = User.delete_user(user_id)
    if result.deleted_count > 0:
        return JsonResponse({'message': 'Utilisateur supprimé avec succès'})
    return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)
