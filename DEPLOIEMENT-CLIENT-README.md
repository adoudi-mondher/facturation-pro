# 🚀 Déploiement Client - Aide-mémoire rapide

## 📝 Résumé : 3 étapes simples pour déployer à distance

### ✅ **Étape 1 : Préparer le package client**

```bash
# ⚠️ IMPORTANT : Utilisez build_for_client (version PROPRE pour clients)
# 1. Builder l'application VERSION CLIENT (sans vos données)
bash packaging/windows/build_for_client.sh
# OU
packaging\windows\build_for_client.bat

# 2. Compiler l'utilitaire Machine ID
build_machine_id_tool.bat

# Résultat :
# - packaging/windows/dist/EasyFacture/  (53 MB, PROPRE)
# - dist/GetMachineID.exe                (10-15 MB)
```

**⚠️ NE PAS utiliser `build.sh` normal** - il contient VOS données de test !

**Deux scripts disponibles :**
- `build.sh` / `build.bat` → Pour VOUS (préserve vos données)
- `build_for_client.sh` / `build_for_client.bat` → Pour CLIENTS (propre)

### 📦 **Étape 2 : Envoyer au client**

**Package à envoyer :**
```
📧 Email avec lien de téléchargement :
   - EasyFacture-v1.6.0.zip (application complète)
   - GetMachineID.exe (utilitaire simple)
   - Instructions.txt
```

**Instructions pour le client :**
```
1. Exécutez GetMachineID.exe
2. Envoyez-nous le fichier machine_id_xxx.txt créé
3. Vous recevrez votre licence par email sous 24h
4. Lancez EasyFacture.exe et entrez la clé reçue
```

### 🔑 **Étape 3 : Générer et envoyer la licence**

```bash
# Lancer le générateur
python generate_customer_license.py

# Menu :
# > Choisir option "2" (Machine ID distant)
# > Coller le Machine ID reçu du client
# > Entrer email client
# > Choisir type de licence (Trial/Annuelle/etc.)

# Résultat : license_client_email_20251212.txt généré
# Envoyer ce fichier au client par email sécurisé
```

---

## 📂 Fichiers importants

| Fichier | Usage |
|---------|-------|
| [get_machine_id.py](get_machine_id.py) | Script pour récupérer Machine ID (client) |
| [generate_customer_license.py](generate_customer_license.py) | Générateur de licences (vous) |
| [build_machine_id_tool.bat](build_machine_id_tool.bat) | Compiler GetMachineID.exe |
| [GUIDE-DEPLOIEMENT-DISTANT.md](GUIDE-DEPLOIEMENT-DISTANT.md) | Guide complet détaillé |

---

## 🎯 Workflow en 1 image

```
VOUS                          CLIENT                         VOUS
────────────────              ────────────────              ────────────────
1. Build app                  2. Reçoit package            3. Génère licence
   + GetMachineID.exe            Exécute GetMachineID         avec Machine ID
                                                              reçu
   ↓                             ↓                            ↓
Envoi ZIP                     Envoie Machine ID           Envoie licence.txt
───────────→                  ───────────→                ───────────→

                              4. Client active
                                 avec la clé
                                 ✅ TERMINÉ
```

---

## 💡 Exemple concret

### Client : Jean Dupont (jean@entreprise.com)

**Jour 1 :**
```bash
# Vous préparez et envoyez
python build_machine_id_tool.bat
# → dist/GetMachineID.exe créé
# → Envoi par email à jean@entreprise.com
```

**Jour 2 :**
```
# Jean exécute GetMachineID.exe
# → Fichier créé : machine_id_PC-JEAN.txt
# → Contenu : a1b2c3d4e5f6789012345678901234ab
# → Jean vous l'envoie par email
```

**Jour 3 :**
```bash
# Vous générez la licence
python generate_customer_license.py
# > Option 2
# > Machine ID : a1b2c3d4e5f6789012345678901234ab
# > Email : jean@entreprise.com
# > Type : Annuelle (365 jours)
# → Fichier créé : license_jean_at_entreprise.com_20251212.txt
```

**Jour 4 :**
```
# Vous envoyez license_jean_at_entreprise.com_20251212.txt
# Jean copie la clé et active l'application
# ✅ Jean peut utiliser Facturation Pro !
```

---

## ⚡ Commandes rapides

```bash
# Build complet (app + utilitaire)
bash packaging/windows/build.sh && build_machine_id_tool.bat

# Générer licence distante
python generate_customer_license.py

# Tester une licence
python test_license.py
```

---

## 📞 En cas de problème

**Client ne peut pas exécuter GetMachineID.exe**
→ Antivirus bloque : ajouter exception ou envoyer version Python

**Machine ID change après mise à jour**
→ Regénérer licence gratuite (changement hostname)

**Licence expirée**
→ Regénérer avec nouvelle date d'expiration

**Support :** adoudi@mondher.ch

---

**Version :** 1.6.0
**Date :** Décembre 2025
**Par :** Mondher ADOUDI - Sidr Valley AI
