from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET, require_http_methods
import json
from .models import User
import logging

logger = logging.getLogger(__name__)


@csrf_exempt  # Utilise cette ligne si tu testes en dehors des formulaires Django (par ex., Postman)
@require_POST
def create_user(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({'error': 'Username et password sont requis'}, status=400)

        user_id = User.create_user(username, password)
        return JsonResponse({'message': 'Utilisateur créé avec succès', 'user_id': str(user_id)}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides'}, status=400)


@csrf_exempt
@require_POST
def create_multiple_users(request):
    try:
        user_ids = User.create_multiple_users(count=100)
        return JsonResponse({
            'message': '100 utilisateurs créés avec succès',
            'user_ids': [str(user_id) for user_id in user_ids]
        }, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt  # Utilise cette ligne si tu testes en dehors des formulaires Django (par ex., Postman)
@require_GET
def get_user(request, user_id):
    user = User.get_user(user_id)
    if user:
        return JsonResponse(user)
    return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)


@csrf_exempt  # Utilise cette ligne si tu testes en dehors des formulaires Django (par ex., Postman)
@require_GET
def get_users(request):
    user = User.get_users()
    if user:
        return JsonResponse(user, safe=False)
    return JsonResponse({'error': 'No Users in the mongo database'}, status=404)


@csrf_exempt
@require_http_methods(["PUT"])
def update_user(request, user_id):
    logger.info("Requête PUT reçue pour la mise à jour de l'utilisateur avec l'ID : %s", user_id)
    try:
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        new_data = {}

        if username:
            new_data["username"] = username
        if password:
            new_data["password"] = password

        if not new_data:
            return JsonResponse({'error': 'Aucune donnée à mettre à jour'}, status=400)

        result = User.update_user(user_id, new_data)
        if result.matched_count > 0:
            return JsonResponse({'message': 'Utilisateur mis à jour avec succès'})
        return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides'}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_user(request, user_id):
    logger.info("Requête DELETE reçue pour la suppression de l'utilisateur avec l'ID : %s", user_id)
    result = User.delete_user(user_id)
    if result.deleted_count > 0:
        logger.info("Utilisateur supprimé avec succès.")
        return JsonResponse({'message': 'Utilisateur supprimé avec succès'})
    else:
        logger.info("Utilisateur non trouvé.")
        return JsonResponse({'error': 'Utilisateur non trouvé'}, status=404)
