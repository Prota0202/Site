import csv
import os
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')  # Remplacez 'mysite.settings' par votre configuration

django.setup()

from account.models import Product  # Importez votre modèle Product

# Chemin vers le fichier CSV
csv_file_path = r'C:\Users\AbdelBadi\Desktop\realistic_shoes.csv'  # Mettez ici le chemin complet

def import_shoes():
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Product.objects.create(
                name=row['name'],
                price=row['price'],
                image_url=row['image_url']
            )
    print("Importation des produits terminée avec succès.")

if __name__ == "__main__":
    import_shoes()
