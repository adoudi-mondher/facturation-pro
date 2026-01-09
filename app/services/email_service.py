"""
Service d'envoi d'emails
"""
from flask_mail import Mail, Message
from flask import current_app, render_template_string
import os

class EmailService:
    """Service d'envoi d'emails avec pièces jointes"""
    
    def __init__(self, mail_instance=None):
        """
        Initialise le service email
        
        Args:
            mail_instance: Instance Flask-Mail (optionnel)
        """
        self.mail = mail_instance
    
    @staticmethod
    def send_document_email(document, destinataire, message_personnalise="", entreprise=None):
        """
        Envoie un document (facture ou devis) par email avec PDF attaché
        
        Args:
            document: Instance de Document (facture ou devis)
            destinataire: Email du destinataire
            message_personnalise: Message personnalisé (optionnel)
            entreprise: Instance Entreprise pour les infos expéditeur
            
        Returns:
            tuple: (success: bool, message: str)
        """
        from flask_mail import Mail, Message as MailMessage
        
        try:
            # Vérifier la configuration SMTP
            if not current_app.config.get('MAIL_SERVER'):
                return False, "Configuration email non définie. Veuillez configurer les paramètres SMTP."
            
            mail = Mail(current_app)
            
            # Type de document
            doc_type = "facture" if document.type == 'facture' else "devis"
            doc_type_article = "la facture" if document.type == 'facture' else "le devis"
            
            # Objet de l'email
            sujet = f"{doc_type.capitalize()} {document.numero} - {entreprise.nom if entreprise else 'Mon Entreprise'}"
            
            # Corps de l'email HTML
            html_body = EmailService._get_email_template(
                document=document,
                message_personnalise=message_personnalise,
                entreprise=entreprise,
                doc_type=doc_type,
                doc_type_article=doc_type_article
            )
            
            # Corps de l'email texte brut (fallback)
            text_body = f"""
Bonjour,

Veuillez trouver ci-joint {doc_type_article} {document.numero}.

{message_personnalise if message_personnalise else ''}

Montant total : {float(document.total_ttc):.2f} €

Cordialement,
{entreprise.nom if entreprise else 'Mon Entreprise'}
            """.strip()
            
            # Créer le message
            msg = MailMessage(
                subject=sujet,
                sender=(entreprise.nom if entreprise else 'Mon Entreprise', 
                       current_app.config.get('MAIL_DEFAULT_SENDER')),
                recipients=[destinataire],
                body=text_body,
                html=html_body
            )
            
            # Attacher le PDF si disponible
            if document.pdf_path and os.path.exists(document.pdf_path):
                pdf_filename = f"{doc_type}_{document.numero.replace('/', '_')}.pdf"
                with open(document.pdf_path, 'rb') as pdf_file:
                    msg.attach(
                        pdf_filename,
                        'application/pdf',
                        pdf_file.read()
                    )
            else:
                return False, "PDF non trouvé. Veuillez générer le PDF avant d'envoyer l'email."
            
            # Envoyer
            mail.send(msg)
            
            return True, f"Email envoyé avec succès à {destinataire}"
            
        except Exception as e:
            return False, f"Erreur lors de l'envoi : {str(e)}"
    
    @staticmethod
    def _get_email_template(document, message_personnalise, entreprise, doc_type, doc_type_article):
        """
        Génère le template HTML de l'email
        
        Args:
            document: Document à envoyer
            message_personnalise: Message personnalisé
            entreprise: Infos entreprise
            doc_type: Type de document (facture/devis)
            doc_type_article: Type avec article (la facture/le devis)
            
        Returns:
            str: HTML de l'email
        """
        # Couleurs professionnelles
        color_primary = '#2C3E50'
        color_accent = '#3498DB'
        color_light = '#ECF0F1'
        
        template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: 'Helvetica', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: {color_primary};
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px 5px 0 0;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .content {{
            background-color: white;
            padding: 30px;
            border: 1px solid {color_light};
            border-top: none;
        }}
        .document-info {{
            background-color: {color_light};
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .document-info p {{
            margin: 5px 0;
        }}
        .amount {{
            font-size: 28px;
            color: {color_accent};
            font-weight: bold;
            text-align: center;
            padding: 20px;
            background-color: {color_light};
            border-radius: 5px;
            margin: 20px 0;
        }}
        .message {{
            background-color: #FFF9E6;
            border-left: 4px solid #F4A460;
            padding: 15px;
            margin: 20px 0;
            font-style: italic;
        }}
        .footer {{
            text-align: center;
            color: #666;
            font-size: 12px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid {color_light};
        }}
        .button {{
            display: inline-block;
            padding: 12px 30px;
            background-color: {color_accent};
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{doc_type.capitalize()} {document.numero}</h1>
    </div>
    
    <div class="content">
        <p>Bonjour,</p>
        
        <p>Veuillez trouver ci-joint <strong>{doc_type_article} {document.numero}</strong>.</p>
        
        {'<div class="message">' + message_personnalise + '</div>' if message_personnalise else ''}
        
        <div class="document-info">
            <p><strong>Client :</strong> {document.client.nom_complet}</p>
            <p><strong>Date d'émission :</strong> {document.date_emission.strftime('%d/%m/%Y')}</p>
            {('<p><strong>Date d' + chr(39) + 'échéance :</strong> ' + document.date_echeance.strftime("%d/%m/%Y") + '</p>') if document.date_echeance else ''}
            {f'<p><strong>Conditions :</strong> {document.conditions_paiement}</p>' if document.conditions_paiement else ''}
        </div>
        
        <div class="amount">
            Montant total : {float(document.total_ttc):.2f} €
        </div>
        
        <p>Le document est joint à cet email au format PDF.</p>
        
        <p>Pour toute question, n'hésitez pas à nous contacter.</p>
        
        <p>Cordialement,<br>
        <strong>{entreprise.nom if entreprise else 'Mon Entreprise'}</strong></p>
    </div>
    
    <div class="footer">
        <p>{entreprise.nom if entreprise else 'Mon Entreprise'}</p>
        {f'<p>{entreprise.adresse}, {entreprise.code_postal} {entreprise.ville}</p>' if entreprise and entreprise.adresse else ''}
        {f'<p>Tél : {entreprise.telephone} | Email : {entreprise.email}</p>' if entreprise else ''}
        {f'<p>SIRET : {entreprise.siret} | TVA : {entreprise.tva_intra}</p>' if entreprise and entreprise.siret else ''}
    </div>
</body>
</html>
        """
        
        return template.strip()
    
    @staticmethod
    def test_smtp_connection(smtp_server, smtp_port, smtp_user, smtp_password, use_tls=True):
        """
        Teste la connexion SMTP
        
        Args:
            smtp_server: Serveur SMTP
            smtp_port: Port SMTP
            smtp_user: Utilisateur
            smtp_password: Mot de passe
            use_tls: Utiliser TLS
            
        Returns:
            tuple: (success: bool, message: str)
        """
        import smtplib
        from email.mime.text import MIMEText
        
        try:
            # Connexion au serveur
            if use_tls:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            
            # Authentification
            server.login(smtp_user, smtp_password)
            server.quit()
            
            return True, "Connexion SMTP réussie !"
            
        except smtplib.SMTPAuthenticationError:
            return False, "Erreur d'authentification. Vérifiez l'email et le mot de passe."
        except smtplib.SMTPConnectError:
            return False, f"Impossible de se connecter au serveur {smtp_server}:{smtp_port}"
        except Exception as e:
            return False, f"Erreur : {str(e)}"
