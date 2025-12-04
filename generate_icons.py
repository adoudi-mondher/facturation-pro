"""
Easy Facture - Générateur d'icônes multi-formats
Par Mondher ADOUDI - Sidr Valley AI

Génère les icônes pour Windows (.ico), Mac (.icns), et Linux (.png)
à partir d'une image PNG source.

Usage:
    python generate_icons.py logo.png
"""

import sys
import os
from PIL import Image

def generate_windows_ico(source_path, output_path):
    """
    Génère un fichier .ico pour Windows
    Contient plusieurs tailles : 16, 32, 48, 64, 128, 256
    """
    print("🪟 Génération icône Windows (.ico)...")
    
    img = Image.open(source_path)
    
    # S'assurer que l'image a un canal alpha (transparence)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Tailles pour Windows
    sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    
    # Créer les icônes à différentes tailles
    img.save(
        output_path,
        format='ICO',
        sizes=sizes
    )
    
    print(f"   ✅ Créé : {output_path}")
    print(f"   Tailles : {', '.join([f'{s[0]}x{s[1]}' for s in sizes])}")

def generate_mac_icns(source_path, output_path):
    """
    Génère un fichier .icns pour Mac
    Nécessite le paquet 'pillow' et 'iconutil' (Mac uniquement)
    
    Sur Windows/Linux : crée juste les PNGs, vous devrez convertir sur Mac
    """
    print("🍎 Génération icône Mac (.icns)...")
    
    img = Image.open(source_path)
    
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Tailles pour macOS
    mac_sizes = [
        (16, 16, 'icon_16x16'),
        (32, 32, 'icon_16x16@2x'),
        (32, 32, 'icon_32x32'),
        (64, 64, 'icon_32x32@2x'),
        (128, 128, 'icon_128x128'),
        (256, 256, 'icon_128x128@2x'),
        (256, 256, 'icon_256x256'),
        (512, 512, 'icon_256x256@2x'),
        (512, 512, 'icon_512x512'),
        (1024, 1024, 'icon_512x512@2x')
    ]
    
    # Créer un dossier temporaire pour les PNGs
    iconset_dir = output_path.replace('.icns', '.iconset')
    os.makedirs(iconset_dir, exist_ok=True)
    
    # Générer chaque taille
    for width, height, name in mac_sizes:
        resized = img.resize((width, height), Image.Resampling.LANCZOS)
        png_path = os.path.join(iconset_dir, f'{name}.png')
        resized.save(png_path, format='PNG')
    
    print(f"   ✅ PNGs créés : {iconset_dir}/")
    
    # Essayer de créer le .icns avec iconutil (Mac seulement)
    if sys.platform == 'darwin':
        import subprocess
        try:
            subprocess.run(['iconutil', '-c', 'icns', iconset_dir, '-o', output_path], check=True)
            print(f"   ✅ Créé : {output_path}")
            # Nettoyer le dossier temporaire
            import shutil
            shutil.rmtree(iconset_dir)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"   ⚠️  iconutil non disponible, gardez le dossier {iconset_dir}")
            print(f"   Sur Mac, lancez : iconutil -c icns {iconset_dir}")
    else:
        print(f"   ⚠️  Conversion .icns nécessite macOS")
        print(f"   Sur Mac, lancez : iconutil -c icns {iconset_dir}")

def generate_linux_png(source_path, output_dir):
    """
    Génère les PNGs pour Linux (différentes tailles)
    """
    print("🐧 Génération icônes Linux (.png)...")
    
    img = Image.open(source_path)
    
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Tailles standard pour Linux
    linux_sizes = [16, 22, 24, 32, 48, 64, 128, 256, 512]
    
    os.makedirs(output_dir, exist_ok=True)
    
    for size in linux_sizes:
        resized = img.resize((size, size), Image.Resampling.LANCZOS)
        png_path = os.path.join(output_dir, f'icon_{size}x{size}.png')
        resized.save(png_path, format='PNG')
    
    # Créer aussi une version haute résolution
    hires = img.resize((1024, 1024), Image.Resampling.LANCZOS)
    hires.save(os.path.join(output_dir, 'icon_1024x1024.png'), format='PNG')
    
    print(f"   ✅ Créés : {output_dir}/icon_*.png")
    print(f"   Tailles : {', '.join([f'{s}x{s}' for s in linux_sizes + [1024]])}")

def create_simple_icon(output_path='logo.png'):
    """
    Crée une icône simple "EF" (Easy Facture) si aucune source fournie
    """
    print("🎨 Création d'une icône par défaut...")
    
    from PIL import ImageDraw, ImageFont
    
    # Créer une image 1024x1024 avec fond bleu
    size = 1024
    img = Image.new('RGBA', (size, size), (0, 119, 190, 255))  # Bleu #0077BE
    draw = ImageDraw.Draw(img)
    
    # Essayer d'utiliser une police système
    try:
        # Taille de police (grande)
        font_size = size // 2
        try:
            # Windows
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                # Linux
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                try:
                    # Mac
                    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
                except:
                    # Fallback
                    font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Texte "EF"
    text = "EF"
    
    # Centrer le texte
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 50  # Ajuster verticalement
    
    # Dessiner le texte en blanc
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # Sauvegarder
    img.save(output_path, format='PNG')
    print(f"   ✅ Icône par défaut créée : {output_path}")
    
    return output_path

def main():
    """Fonction principale"""
    print("=" * 60)
    print("   EASY FACTURE - GÉNÉRATEUR D'ICÔNES")
    print("   Par Mondher ADOUDI - Sidr Valley AI")
    print("=" * 60)
    print()
    
    # Vérifier les arguments
    if len(sys.argv) < 2:
        print("⚠️  Aucune image source fournie")
        print("   Création d'une icône par défaut...")
        print()
        source_image = create_simple_icon('logo.png')
    else:
        source_image = sys.argv[1]
        
        if not os.path.exists(source_image):
            print(f"❌ Fichier non trouvé : {source_image}")
            sys.exit(1)
    
    print(f"📁 Image source : {source_image}")
    print()
    
    # Créer le dossier de sortie
    output_dir = 'icons'
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Générer les icônes
        generate_windows_ico(source_image, os.path.join(output_dir, 'icon.ico'))
        print()
        
        generate_mac_icns(source_image, os.path.join(output_dir, 'icon.icns'))
        print()
        
        generate_linux_png(source_image, os.path.join(output_dir, 'linux'))
        print()
        
        print("=" * 60)
        print("✅ GÉNÉRATION TERMINÉE !")
        print("=" * 60)
        print()
        print(f"📦 Fichiers créés dans : {output_dir}/")
        print()
        print("📁 Structure :")
        print(f"   {output_dir}/")
        print(f"   ├── icon.ico              (Windows)")
        print(f"   ├── icon.icns             (Mac)")
        print(f"   └── linux/")
        print(f"       ├── icon_16x16.png")
        print(f"       ├── icon_32x32.png")
        print(f"       ├── ... (toutes tailles)")
        print(f"       └── icon_1024x1024.png")
        print()
        print("🎯 Prochaines étapes :")
        print("   1. Copier icon.ico dans packaging/windows/")
        print("   2. Copier icon.icns dans packaging/mac/")
        print("   3. Copier linux/*.png dans packaging/linux/")
        print()
        
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()