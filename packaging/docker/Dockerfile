# ===============================================
# Easy Facture - Dockerfile
# Par Mondher ADOUDI - Sidr Valley AI
# Version 1.5.0
# ===============================================

FROM python:3.11-slim

# Métadonnées
LABEL maintainer="Mondher ADOUDI <adoudi@mondher.ch>"
LABEL description="Easy Facture - Logiciel de facturation pour artisans"
LABEL version="1.5.0"

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    FLASK_APP=run.py \
    FLASK_ENV=production \
    PORT=5000

# Créer l'utilisateur non-root
RUN useradd -m -u 1000 easyfacture && \
    mkdir -p /app /app/data /app/logs && \
    chown -R easyfacture:easyfacture /app

# Répertoire de travail
WORKDIR /app

# Copier les dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier l'application
COPY --chown=easyfacture:easyfacture . .

# Passer à l'utilisateur non-root
USER easyfacture

# Créer la base de données au premier démarrage
RUN python3 -c "from app import create_app; from app.extensions import db; app = create_app(); app.app_context().push(); db.create_all()"

# Exposer le port
EXPOSE 5000

# Volume pour les données
VOLUME ["/app/data", "/app/logs"]

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python3 -c "import requests; requests.get('http://localhost:5000', timeout=5)" || exit 1

# Commande de démarrage
CMD ["python3", "run.py", "--host=0.0.0.0", "--port=5000"]
