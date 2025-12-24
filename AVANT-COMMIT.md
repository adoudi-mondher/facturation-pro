# ✅ Checklist avant commit

## 🎯 Résumé du nettoyage effectué

### ✅ Sécurité
- [x] Licence personnelle sauvegardée → `.personal_backup/`
- [x] Pattern `license_*.txt` ajouté au .gitignore
- [x] Pattern `.personal_backup/` ajouté au .gitignore
- [x] Base de données exclue (déjà dans .gitignore)
- [x] Fichier .env protégé (déjà dans .gitignore)

### ✅ Nettoyage (421 MB libérés)
- [x] `venv/` supprimé (213 MB)
- [x] `venv_build/` supprimé (113 MB)
- [x] `build/`, `dist/` supprimés
- [x] `packaging/windows/build/`, `packaging/windows/dist/` supprimés (93 MB)
- [x] 8 dossiers `__pycache__/` supprimés
- [x] `.pytest_cache/`, `htmlcov/` supprimés
- [x] Backups manuels supprimés (`*.backup`)

### ✅ Documentation
- [x] `CORRECTIONS-BUILD-WINDOWS.md` → `docs/archive/`
- [x] `CHANGELOG-v1.6.0.md` créé
- [x] `COMMIT-MESSAGE.txt` préparé
- [x] Documentation complète et cohérente

---

## 📋 État actuel du projet

### Fichiers modifiés (5)
1. `.gitignore` - Ajout protections
2. `config.py` - Version 1.6.0, LICENSE_ENABLED
3. `run.py` - Intégration licence
4. `packaging/windows/build.bat` - Protection données
5. `packaging/windows/README-WINDOWS.md` - Doc 2 builds

### Nouveaux fichiers majeurs (16+)

#### Système de licence
- `app/utils/license.py`
- `generate_customer_license.py`
- `get_machine_id.py`
- `build_machine_id_tool.bat`
- `test_license.py`

#### Build Windows
- `packaging/windows/build.sh`
- `packaging/windows/build_for_client.sh`
- `packaging/windows/build_for_client.bat`
- `packaging/windows/EasyFacture.spec`
- `EasyFacture.spec`

#### Documentation
- `BUILD-PERSONNEL-VS-CLIENT.md`
- `GUIDE-DEPLOIEMENT-DISTANT.md`
- `DEPLOIEMENT-CLIENT-README.md`
- `PROTECTION-DONNEES-BUILD.md`
- `CHANGELOG-v1.6.0.md`

#### Maintenance
- `cleanup.sh`
- `COMMIT-MESSAGE.txt`
- `docs/archive/`

---

## 🚀 Commandes pour commiter

### Option 1 : Commit simple
```bash
git add .
git commit -F COMMIT-MESSAGE.txt
```

### Option 2 : Commit avec vérification
```bash
# Vérifier les fichiers
git status

# Ajouter tous les fichiers
git add .

# Vérifier ce qui sera commité
git diff --cached --stat

# Commiter avec le message préparé
git commit -F COMMIT-MESSAGE.txt

# Vérifier le commit
git log -1 --stat
```

### Option 3 : Commit par étapes
```bash
# Étape 1 : Système de licence
git add app/utils/license.py generate_customer_license.py get_machine_id.py test_license.py build_machine_id_tool.bat
git commit -m "feat(license): add hardware-based license system"

# Étape 2 : Build Windows
git add packaging/windows/*.sh packaging/windows/*.bat packaging/windows/*.spec EasyFacture.spec
git commit -m "fix(build): improve Windows build and add client build mode"

# Étape 3 : Documentation
git add *.md docs/
git commit -m "docs: add comprehensive deployment and build documentation"

# Étape 4 : Config et cleanup
git add .gitignore config.py run.py cleanup.sh
git commit -m "chore: update config and add cleanup script"
```

---

## ⚠️ Points de vigilance

### Avant de commiter
- [ ] Vérifier qu'aucun fichier sensible n'est dans le commit
  ```bash
  git status | grep -i "license_"
  git status | grep -i ".env"
  git status | grep -i "facturation.db"
  ```

- [ ] Vérifier la taille du commit
  ```bash
  git diff --cached --stat
  # Ne devrait PAS contenir venv/, build/, dist/
  ```

- [ ] Vérifier le .gitignore
  ```bash
  cat .gitignore | grep -E "license|backup|venv"
  ```

### Après le commit (TODO)
- [ ] Recréer venv : `py -m venv venv`
- [ ] Installer dépendances : `pip install -r requirements.txt`
- [ ] Tester le build : `bash packaging/windows/build.sh`
- [ ] Vérifier que l'app fonctionne : `python run.py`
- [ ] Push sur le remote : `git push origin feature/license-system`

---

## 📊 Statistiques du commit

- **Fichiers modifiés** : 5
- **Nouveaux fichiers** : ~20
- **Lignes ajoutées** : ~2000+
- **Documentation** : 5 guides (30+ KB)
- **Espace libéré** : 421 MB
- **Version** : 1.6.0

---

## 🎯 Après le commit

### Test de non-régression
```bash
# 1. Recréer l'environnement
py -m venv venv
source venv/Scripts/activate  # Git Bash
pip install -r requirements.txt

# 2. Tester l'application
python run.py
# → Doit démarrer sur http://localhost:5000

# 3. Tester le build personnel
bash packaging/windows/build.sh
# → Doit créer dist/EasyFacture/

# 4. Tester le build client
bash packaging/windows/build_for_client.sh
# → Doit créer dist/EasyFacture/ SANS données

# 5. Tester la génération de licence
python generate_customer_license.py
# → Option 1 et 2 doivent fonctionner
```

### Push vers le remote
```bash
git push origin feature/license-system
```

### Créer une Pull Request (optionnel)
Si vous utilisez GitHub/GitLab, créer une PR vers `main` avec :
- Titre : "feat: License system v1.6.0 + Windows build improvements"
- Description : Coller le contenu de `CHANGELOG-v1.6.0.md`

---

## 📞 En cas de problème

### Si le commit échoue
```bash
# Annuler les modifications non commitées
git reset --hard

# Restaurer les fichiers supprimés si nécessaire
# (venv/, build/, dist/ peuvent être recréés)
```

### Si vous avez commité un fichier sensible
```bash
# Retirer du dernier commit (avant push)
git reset --soft HEAD~1
git restore --staged <fichier-sensible>
git commit -F COMMIT-MESSAGE.txt

# Si déjà pushé (DANGER)
# Contacter l'admin Git pour rotation des secrets
```

### Si vous voulez revenir en arrière
```bash
# Votre licence est sauvegardée dans :
ls -la .personal_backup/

# Restaurer si besoin
cp .personal_backup/license_*.txt ./
```

---

**Tout est prêt pour le commit ! 🚀**

Date : 12 décembre 2025
Auteur : Mondher ADOUDI
Version : 1.6.0
