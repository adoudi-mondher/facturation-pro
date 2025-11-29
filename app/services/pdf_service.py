"""
Service de génération PDF
Design générique et professionnel pour factures et devis
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
import os
from datetime import datetime

class PDFService:
    """Service de génération de PDF pour documents"""
    
    # Couleurs professionnelles neutres
    COLOR_PRIMARY = colors.HexColor('#2C3E50')      # Bleu-gris foncé
    COLOR_SECONDARY = colors.HexColor('#34495E')    # Gris ardoise
    COLOR_ACCENT = colors.HexColor('#3498DB')       # Bleu clair
    COLOR_LIGHT = colors.HexColor('#ECF0F1')        # Gris clair
    COLOR_TEXT = colors.HexColor('#2C3E50')         # Texte foncé
    COLOR_SUCCESS = colors.HexColor('#27AE60')      # Vert pour payé/accepté
    
    def __init__(self, document, entreprise):
        """
        Initialise le service PDF
        
        Args:
            document: Instance de Document (facture ou devis)
            entreprise: Instance de Parametre avec les infos entreprise
        """
        self.document = document
        self.entreprise = entreprise
        self.width, self.height = A4
        self.margin = 15 * mm
        
    def generate(self, output_path):
        """
        Génère le PDF
        
        Args:
            output_path: Chemin du fichier PDF à créer
        """
        # Créer le dossier si nécessaire
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Créer le document PDF
        pdf = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=self.margin,
            leftMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin
        )
        
        # Construire le contenu
        story = []
        
        # En-tête
        story.extend(self._build_header())
        story.append(Spacer(1, 10*mm))
        
        # Informations client
        story.extend(self._build_client_info())
        story.append(Spacer(1, 10*mm))
        
        # Tableau des produits
        story.extend(self._build_products_table())
        story.append(Spacer(1, 10*mm))
        
        # Totaux
        story.extend(self._build_totals())
        story.append(Spacer(1, 10*mm))
        
        # Notes si présentes
        if self.document.notes:
            story.extend(self._build_notes())
            story.append(Spacer(1, 5*mm))
        
        # Mentions légales
        story.extend(self._build_footer())
        
        # Générer le PDF
        pdf.build(story, onFirstPage=self._add_page_number, onLaterPages=self._add_page_number)
        
        return output_path
    
    def _build_header(self):
        """Construit l'en-tête du document"""
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        style_title = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=self.COLOR_PRIMARY,
            spaceAfter=5,
            alignment=TA_RIGHT
        )
        style_subtitle = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=self.COLOR_SECONDARY,
            alignment=TA_RIGHT
        )
        style_company = ParagraphStyle(
            'CompanyInfo',
            parent=styles['Normal'],
            fontSize=10,
            textColor=self.COLOR_TEXT,
            alignment=TA_LEFT
        )
        
        # Données de l'en-tête
        header_data = []
        
        # Colonne gauche : Logo et infos entreprise
        left_col = []
        
        # Logo si disponible
        logo_path = self.entreprise.get('logo_path')
        if logo_path and os.path.exists(logo_path):
            try:
                logo = Image(logo_path, width=40*mm, height=40*mm, kind='proportional')
                left_col.append(logo)
            except:
                pass
        
        # Infos entreprise
        company_info = f"""<b>{self.entreprise.get('nom_entreprise', 'Entreprise')}</b><br/>
{self.entreprise.get('adresse', '')}<br/>
{self.entreprise.get('code_postal', '')} {self.entreprise.get('ville', '')}<br/>
{self.entreprise.get('telephone', '')}<br/>
{self.entreprise.get('email', '')}"""
        
        if self.entreprise.get('siret'):
            company_info += f"<br/>SIRET: {self.entreprise.get('siret')}"
        if self.entreprise.get('tva_intra'):
            company_info += f"<br/>TVA: {self.entreprise.get('tva_intra')}"
        
        left_col.append(Paragraph(company_info, style_company))
        
        # Colonne droite : Type de document et numéro
        right_col = []
        doc_type = "FACTURE" if self.document.type == 'facture' else "DEVIS"
        right_col.append(Paragraph(doc_type, style_title))
        right_col.append(Paragraph(f"N° {self.document.numero}", style_subtitle))
        right_col.append(Spacer(1, 5*mm))
        
        # Date d'émission
        date_label = "Date d'émission :" if self.document.type == 'facture' else "Date d'émission :"
        right_col.append(Paragraph(f"{date_label} {self.document.date_emission.strftime('%d/%m/%Y')}", style_subtitle))
        
        # Date d'échéance ou validité
        if self.document.date_echeance:
            date_label2 = "Date d'échéance :" if self.document.type == 'facture' else "Valable jusqu'au :"
            right_col.append(Paragraph(f"{date_label2} {self.document.date_echeance.strftime('%d/%m/%Y')}", style_subtitle))
        
        # Statut avec badge coloré
        statut_color = self.COLOR_SECONDARY
        if self.document.statut == 'payee' or self.document.statut == 'accepte':
            statut_color = self.COLOR_SUCCESS
        
        statut_text = self.document.statut.capitalize()
        right_col.append(Spacer(1, 3*mm))
        right_col.append(Paragraph(f'<font color="{statut_color.hexval()}"><b>{statut_text}</b></font>', style_subtitle))
        
        # Créer le tableau d'en-tête
        header_table = Table(
            [[left_col, right_col]],
            colWidths=[90*mm, 90*mm]
        )
        
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ]))
        
        elements.append(header_table)
        
        # Ligne de séparation
        elements.append(Spacer(1, 3*mm))
        line_table = Table([['']], colWidths=[180*mm])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, self.COLOR_PRIMARY),
        ]))
        elements.append(line_table)
        
        return elements
    
    def _build_client_info(self):
        """Construit la section informations client"""
        elements = []
        
        styles = getSampleStyleSheet()
        style_label = ParagraphStyle(
            'ClientLabel',
            parent=styles['Normal'],
            fontSize=9,
            textColor=self.COLOR_SECONDARY,
            spaceAfter=2
        )
        style_info = ParagraphStyle(
            'ClientInfo',
            parent=styles['Normal'],
            fontSize=10,
            textColor=self.COLOR_TEXT
        )
        
        # Titre
        elements.append(Paragraph('<b>CLIENT</b>', style_label))
        
        # Infos client
        client = self.document.client
        client_info = f"<b>{client.nom_complet}</b><br/>"
        
        if client.adresse:
            client_info += f"{client.adresse}<br/>"
        if client.code_postal or client.ville:
            client_info += f"{client.code_postal or ''} {client.ville or ''}<br/>"
        if client.email:
            client_info += f"{client.email}<br/>"
        if client.telephone:
            client_info += f"{client.telephone}"
        
        elements.append(Paragraph(client_info, style_info))
        
        return elements
    
    def _build_products_table(self):
        """Construit le tableau des produits"""
        elements = []
        
        # En-têtes
        headers = ['Désignation', 'Qté', 'Prix HT', 'TVA', 'Remise', 'Total HT']
        
        # Données
        data = [headers]
        
        for ligne in self.document.lignes:
            row = [
                ligne.designation,
                f"{ligne.quantite:g}",
                f"{float(ligne.prix_unitaire_ht):.2f} €",
                f"{float(ligne.taux_tva):.1f}%",
                f"{float(ligne.remise_ligne or 0):.1f}%",
                f"{float(ligne.total_ht):.2f} €"
            ]
            data.append(row)
        
        # Créer le tableau
        table = Table(data, colWidths=[70*mm, 20*mm, 25*mm, 20*mm, 20*mm, 25*mm])
        
        # Style du tableau
        table_style = TableStyle([
            # En-tête
            ('BACKGROUND', (0, 0), (-1, 0), self.COLOR_PRIMARY),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            
            # Corps du tableau
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.COLOR_LIGHT]),
            ('GRID', (0, 0), (-1, -1), 0.5, self.COLOR_SECONDARY),
            
            # Alignement
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Padding
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ])
        
        table.setStyle(table_style)
        elements.append(table)
        
        return elements
    
    def _build_totals(self):
        """Construit la section totaux"""
        elements = []
        
        # Données des totaux
        totals_data = []
        
        # Remise globale si applicable
        if self.document.remise_globale and float(self.document.remise_globale) > 0:
            totals_data.append(['', f'Remise globale ({float(self.document.remise_globale):.1f}%)', ''])
        
        totals_data.extend([
            ['', 'Total HT :', f"{float(self.document.total_ht):.2f} €"],
            ['', f'TVA :', f"{float(self.document.total_tva):.2f} €"],
            ['', 'Total TTC :', f"{float(self.document.total_ttc):.2f} €"],
        ])
        
        # Créer le tableau
        totals_table = Table(totals_data, colWidths=[90*mm, 50*mm, 40*mm])
        
        # Style
        totals_style = TableStyle([
            ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -2), 10),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('TEXTCOLOR', (0, -1), (-1, -1), self.COLOR_PRIMARY),
            ('LINEABOVE', (1, -1), (-1, -1), 2, self.COLOR_PRIMARY),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ])
        
        totals_table.setStyle(totals_style)
        elements.append(totals_table)
        
        return elements
    
    def _build_notes(self):
        """Construit la section notes"""
        elements = []
        
        styles = getSampleStyleSheet()
        style_notes = ParagraphStyle(
            'Notes',
            parent=styles['Normal'],
            fontSize=9,
            textColor=self.COLOR_TEXT,
            leftIndent=10,
            rightIndent=10,
            spaceBefore=5,
            spaceAfter=5,
            borderWidth=1,
            borderColor=self.COLOR_LIGHT,
            borderPadding=8,
            backColor=self.COLOR_LIGHT
        )
        
        elements.append(Paragraph('<b>Notes :</b>', styles['Normal']))
        elements.append(Paragraph(self.document.notes.replace('\n', '<br/>'), style_notes))
        
        return elements
    
    def _build_footer(self):
        """Construit le pied de page avec mentions légales"""
        elements = []
        
        styles = getSampleStyleSheet()
        style_footer = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=7,
            textColor=self.COLOR_SECONDARY,
            alignment=TA_CENTER
        )
        
        # Mentions légales
        mentions = self.entreprise.get('mentions_legales', '')
        if not mentions:
            mentions = "Conditions de paiement : "
            if self.document.type == 'facture' and self.document.conditions_paiement:
                mentions += self.document.conditions_paiement
            else:
                mentions += "À réception"
        
        elements.append(Spacer(1, 5*mm))
        elements.append(Paragraph(mentions.replace('\n', '<br/>'), style_footer))
        
        return elements
    
    def _add_page_number(self, canvas, doc):
        """Ajoute le numéro de page"""
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(self.COLOR_SECONDARY)
        page_num = f"Page {canvas.getPageNumber()}"
        canvas.drawRightString(self.width - self.margin, self.margin / 2, page_num)
        canvas.restoreState()
