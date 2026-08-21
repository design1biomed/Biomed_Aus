import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bmi_aus.settings')
django.setup()

from main.models import ExtractCategory

def populate():
    if ExtractCategory.objects.exists():
        print("Extract categories already exist.")
        return

    extracts = [
        {
            'title': 'Cosmeceutical',
            'subtitle': 'Bio-Active',
            'image_path': 'static/images/cosmetic_ingredients.png',
            'order': 1
        },
        {
            'title': 'Nutraceutical',
            'subtitle': 'High Potency',
            'image_path': 'static/images/sports_nutrition.png',
            'order': 2
        },
        {
            'title': 'Food Colors',
            'subtitle': '100% Natural',
            'image_path': 'static/images/food_colors.png',
            'order': 3
        }
    ]

    for item in extracts:
        # Check if file exists, WebP vs PNG etc
        path_png = item['image_path']
        path_webp = item['image_path'].replace('.png', '.webp')
        
        path_to_use = None
        if os.path.exists(path_png):
            path_to_use = path_png
        elif os.path.exists(path_webp):
            path_to_use = path_webp
            
        extract = ExtractCategory(
            title=item['title'],
            subtitle=item['subtitle'],
            order=item['order']
        )
        
        if path_to_use:
            with open(path_to_use, 'rb') as f:
                extract.image.save(os.path.basename(path_to_use), File(f), save=True)
        else:
            extract.save()
            print(f"Could not find image for {item['title']}")
            
    print("Populated Extract Categories!")

if __name__ == '__main__':
    populate()
