/**
 * Gestion dynamique du formulaire de facture
 * Ajout/suppression de lignes de produits avec calculs automatiques
 */

// Compteur de lignes
let ligneCounter = 0;

// Données des produits (chargées depuis le serveur)
let produitsData = [];

/**
 * Initialiser le formulaire
 */
document.addEventListener('DOMContentLoaded', function() {
    // Charger les produits
    chargerProduits();
     
    // Événements
    document.getElementById('btn-ajouter-ligne').addEventListener('click', ajouterLigne);
    document.getElementById('remise_globale').addEventListener('input', calculerTotaux);
});

/**
 * Charger la liste des produits depuis l'API
 */
function chargerProduits() {
    fetch('/api/produits')
        .then(response => response.json())
        .then(data => {
            produitsData = data;
            
            // Vérifier s'il y a des lignes existantes (mode édition)
            // lignesExistantes est défini dans edit_facture.html ou vaut undefined en création
            const hasExistingLines = typeof lignesExistantes !== 'undefined' && lignesExistantes.length > 0;
            
            // Ajouter première ligne SEULEMENT si mode création
            if (!hasExistingLines) {
                ajouterLigne();
            }
        })
        .catch(error => {
            console.error('Erreur chargement produits:', error);
            alert('Erreur lors du chargement des produits. Veuillez recharger la page.');
        });
}

/**
 * Ajouter une nouvelle ligne de produit
 */
function ajouterLigne() {
    ligneCounter++;
    
    const tbody = document.getElementById('lignes-facture');
    const tr = document.createElement('tr');
    tr.id = `ligne-${ligneCounter}`;
    tr.dataset.ligne = ligneCounter;
    
    tr.innerHTML = `
        <td>
            <select class="form-select form-select-sm produit-select" 
                    name="lignes[${ligneCounter}][produit_id]" 
                    data-ligne="${ligneCounter}" 
                    required>
                <option value="">-- Sélectionner --</option>
                ${produitsData.map(p => `
                    <option value="${p.id}" 
                            data-prix="${p.prix_ht}" 
                            data-tva="${p.taux_tva}"
                            data-stock="${p.stock_actuel || 'null'}"
                            data-gerer-stock="${p.gerer_stock}">
                        ${p.reference ? p.reference + ' - ' : ''}${p.designation}
                    </option>
                `).join('')}
            </select>
            <input type="hidden" name="lignes[${ligneCounter}][designation]" class="ligne-designation">
        </td>
        <td>
            <input type="number" 
                   class="form-control form-control-sm text-end quantite" 
                   name="lignes[${ligneCounter}][quantite]" 
                   data-ligne="${ligneCounter}"
                   value="1" 
                   min="0.01" 
                   step="0.01" 
                   required>
            <small class="text-danger stock-alert" style="display:none;"></small>
        </td>
        <td>
            <input type="number" 
                   class="form-control form-control-sm text-end prix-unitaire" 
                   name="lignes[${ligneCounter}][prix_unitaire_ht]" 
                   data-ligne="${ligneCounter}"
                   value="0.00" 
                   min="0" 
                   step="0.01" 
                   required>
        </td>
        <td>
            <input type="number" 
                   class="form-control form-control-sm text-end taux-tva" 
                   name="lignes[${ligneCounter}][taux_tva]" 
                   data-ligne="${ligneCounter}"
                   value="20.00" 
                   min="0" 
                   max="100" 
                   step="0.01" 
                   required>
        </td>
        <td>
            <input type="number" 
                   class="form-control form-control-sm text-end remise-ligne" 
                   name="lignes[${ligneCounter}][remise_ligne]" 
                   data-ligne="${ligneCounter}"
                   value="0" 
                   min="0" 
                   max="100" 
                   step="0.01">
        </td>
        <td class="text-end">
            <span class="total-ligne-ht fw-bold">0.00 €</span>
        </td>
        <td class="text-center">
            <button type="button" 
                    class="btn btn-sm btn-danger btn-supprimer-ligne" 
                    data-ligne="${ligneCounter}"
                    title="Supprimer la ligne">
                <i class="bi bi-trash"></i>
            </button>
        </td>
    `;
    
    tbody.appendChild(tr);
    
    // Événements de la ligne
    const select = tr.querySelector('.produit-select');
    const quantite = tr.querySelector('.quantite');
    const prix = tr.querySelector('.prix-unitaire');
    const tva = tr.querySelector('.taux-tva');
    const remise = tr.querySelector('.remise-ligne');
    const btnSupprimer = tr.querySelector('.btn-supprimer-ligne');
    
    select.addEventListener('change', function() {
        onProduitChange(ligneCounter);
    });
    
    quantite.addEventListener('input', function() {
        verifierStock(ligneCounter);
        calculerTotalLigne(ligneCounter);
    });
    
    prix.addEventListener('input', function() {
        calculerTotalLigne(ligneCounter);
    });
    
    tva.addEventListener('input', function() {
        calculerTotalLigne(ligneCounter);
    });
    
    remise.addEventListener('input', function() {
        calculerTotalLigne(ligneCounter);
    });
    
    btnSupprimer.addEventListener('click', function() {
        supprimerLigne(ligneCounter);
    });
}

/**
 * Quand un produit est sélectionné, remplir automatiquement les champs
 */
function onProduitChange(ligneId) {
    const select = document.querySelector(`select[data-ligne="${ligneId}"]`);
    const option = select.options[select.selectedIndex];
    
    if (!option.value) return;
    
    const prix = parseFloat(option.dataset.prix);
    const tva = parseFloat(option.dataset.tva);
    const designation = option.text;
    
    // Remplir les champs
    document.querySelector(`input.prix-unitaire[data-ligne="${ligneId}"]`).value = prix.toFixed(2);
    document.querySelector(`input.taux-tva[data-ligne="${ligneId}"]`).value = tva.toFixed(2);
    document.querySelector(`input.ligne-designation[name="lignes[${ligneId}][designation]"]`).value = designation;
    
    // Vérifier le stock
    verifierStock(ligneId);
    
    // Calculer
    calculerTotalLigne(ligneId);
}

/**
 * Vérifier le stock disponible
 */
function verifierStock(ligneId) {
    const select = document.querySelector(`select[data-ligne="${ligneId}"]`);
    const option = select.options[select.selectedIndex];
    
    if (!option.value) return;
    
    const gererStock = option.dataset.gererStock === 'true';
    const stockActuel = parseFloat(option.dataset.stock);
    const quantite = parseFloat(document.querySelector(`input.quantite[data-ligne="${ligneId}"]`).value);
    const alertElement = document.querySelector(`#ligne-${ligneId} .stock-alert`);
    
    if (gererStock && !isNaN(stockActuel)) {
        if (quantite > stockActuel) {
            alertElement.textContent = `⚠️ Stock insuffisant (${stockActuel} disponible)`;
            alertElement.style.display = 'block';
        } else if (quantite === stockActuel) {
            alertElement.textContent = `ℹ️ Dernier(s) en stock`;
            alertElement.style.display = 'block';
            alertElement.classList.remove('text-danger');
            alertElement.classList.add('text-warning');
        } else {
            alertElement.style.display = 'none';
        }
    } else {
        alertElement.style.display = 'none';
    }
}

/**
 * Calculer le total d'une ligne
 */
function calculerTotalLigne(ligneId) {
    const quantite = parseFloat(document.querySelector(`input.quantite[data-ligne="${ligneId}"]`).value) || 0;
    const prixUnitaire = parseFloat(document.querySelector(`input.prix-unitaire[data-ligne="${ligneId}"]`).value) || 0;
    const remiseLigne = parseFloat(document.querySelector(`input.remise-ligne[data-ligne="${ligneId}"]`).value) || 0;
    
    let totalHT = quantite * prixUnitaire;
    
    // Appliquer la remise de ligne
    if (remiseLigne > 0) {
        totalHT = totalHT * (1 - remiseLigne / 100);
    }
    
    // Afficher
    document.querySelector(`#ligne-${ligneId} .total-ligne-ht`).textContent = formatCurrency(totalHT);
    
    // Recalculer les totaux globaux
    calculerTotaux();
}

/**
 * Supprimer une ligne
 */
function supprimerLigne(ligneId) {
    const tr = document.getElementById(`ligne-${ligneId}`);
    if (tr) {
        tr.remove();
        calculerTotaux();
    }
    
    // Garder au moins une ligne
    const tbody = document.getElementById('lignes-facture');
    if (tbody.children.length === 0) {
        ajouterLigne();
    }
}

/**
 * Calculer les totaux globaux
 */
function calculerTotaux() {
    let totalHT = 0;
    let totalTVA = 0;
    
    // Parcourir toutes les lignes
    const lignes = document.querySelectorAll('#lignes-facture tr');
    lignes.forEach(tr => {
        const ligneId = tr.dataset.ligne;
        
        const quantite = parseFloat(document.querySelector(`input.quantite[data-ligne="${ligneId}"]`).value) || 0;
        const prixUnitaire = parseFloat(document.querySelector(`input.prix-unitaire[data-ligne="${ligneId}"]`).value) || 0;
        const tauxTVA = parseFloat(document.querySelector(`input.taux-tva[data-ligne="${ligneId}"]`).value) || 0;
        const remiseLigne = parseFloat(document.querySelector(`input.remise-ligne[data-ligne="${ligneId}"]`).value) || 0;
        
        let ligneHT = quantite * prixUnitaire;
        
        // Remise de ligne
        if (remiseLigne > 0) {
            ligneHT = ligneHT * (1 - remiseLigne / 100);
        }
        
        const ligneTVA = ligneHT * (tauxTVA / 100);
        
        totalHT += ligneHT;
        totalTVA += ligneTVA;
    });
    
    // Remise globale
    const remiseGlobale = parseFloat(document.getElementById('remise_globale').value) || 0;
    if (remiseGlobale > 0) {
        const montantRemise = totalHT * (remiseGlobale / 100);
        totalHT -= montantRemise;
        totalTVA = totalTVA * (1 - remiseGlobale / 100); // TVA proportionnelle
    }
    
    const totalTTC = totalHT + totalTVA;
    
    // Afficher
    document.getElementById('display-total-ht').textContent = formatCurrency(totalHT);
    document.getElementById('display-total-tva').textContent = formatCurrency(totalTVA);
    document.getElementById('display-total-ttc').textContent = formatCurrency(totalTTC);
    
    // Champs hidden pour soumission
    document.getElementById('total_ht').value = totalHT.toFixed(2);
    document.getElementById('total_tva').value = totalTVA.toFixed(2);
    document.getElementById('total_ttc').value = totalTTC.toFixed(2);
}

/**
 * Formater un montant en euros
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}

/**
 * Validation avant soumission
 */
document.querySelector('form')?.addEventListener('submit', function(e) {
    const lignes = document.querySelectorAll('#lignes-facture tr');
    
    if (lignes.length === 0) {
        e.preventDefault();
        alert('Veuillez ajouter au moins une ligne de produit');
        return false;
    }
    
    // Vérifier les stocks
    let stockOK = true;
    lignes.forEach(tr => {
        const alertElement = tr.querySelector('.stock-alert');
        if (alertElement && alertElement.style.display !== 'none' && alertElement.classList.contains('text-danger')) {
            stockOK = false;
        }
    });
    
    if (!stockOK) {
        const confirmer = confirm('Certains produits ont un stock insuffisant. Continuer quand même ?');
        if (!confirmer) {
            e.preventDefault();
            return false;
        }
    }
});
