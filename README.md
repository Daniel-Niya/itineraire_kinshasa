Kinshasa Itinéraires - Guide d'utilisation

## Description du Projet

**Kinshasa Itinéraires** est une application web intelligente de planification de trajets développée spécifiquement pour la ville de Kinshasa, République Démocratique du Congo. Cette plateforme permet aux utilisateurs de trouver les meilleurs itinéraires entre différents points de repère de la ville avec jusqu'à 5 alternatives différentes.

# Objectifs du Projet

- Faciliter la mobilité : Aider les habitants et visiteurs à se déplacer dans Kinshasa
- Optimiser les trajets : Proposer plusieurs itinéraires alternatifs avec comparaison
- Expérience utilisateur : Interface moderne et intuitive adaptée au contexte local
- Données locales : Utilisation de points de repère authentiques de Kinshasa

## Fonctionnalités Principales

## Planification d'Itinéraires
- Sélection facile : Choix parmi 10 points de repère principaux de Kinshasa
- Multiples alternatives : Jusqu'à 5 itinéraires différents par recherche
- Comparaison intelligente : Distance, durée et type d'itinéraire
- Inversion rapide : Échange facile entre départ et arrivée

## Interface Utilisateur
- Design moderne : Interface responsive avec gradient et cartes élégantes
- Carte interactive : Intégration Leaflet avec OpenStreetMap
- Visualisation claire : Couleurs distinctes pour chaque itinéraire
- Popups informatifs : Détails des points d'intérêt avec images

## Informations Détaillées
- Métriques précises : Distance en kilomètres et durée en minutes
- Points d'intérêt : Arrêts importants le long de chaque itinéraire
- Images contextuelles : Photos des landmarks et points d'arrêt
- Recommendations : Mise en évidence de l'itinéraire optimal

## Architecture Technique

## Structure du Projet
```
kinshasa-itineraires/
├── app.py                 # Application Flask principale
├── static/
│   ├── uploads/          # Images des points de repère
│   └── style.css         # Feuilles de style (intégré)
├── templates/
│   └── index.html        # Interface utilisateur
└── requirements.txt      # Dépendances Python
```

### Technologies Utilisées

#### Backend
- Python 3 + Flask : Serveur web et API
- OSRM : Calcul d'itinéraires open-source
- Requests : Communication avec les APIs externes

#### Frontend
- HTML5 + CSS3 : Structure et style
- Bootstrap 5 : Framework CSS responsive
- Leaflet.js : Cartes interactives
- Font Awesome : Icônes
- JavaScript ES6 : Interactivité

#### Services Externes
- OpenStreetMap : Données cartographiques
- OSRM : Moteur de calcul d'itinéraires
- Unsplash : Images par défaut

##  Installation et Démarrage

### Prérequis
- Python 3.8 ou supérieur
- Pip (gestionnaire de packages Python)
- Connexion internet (pour OSRM et cartes)

### Installation

1. Cloner le projet
```bash
git clone <repository-url>
cd kinshasa-itineraires
```

2. Créer un environnement virtuel (recommandé)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. Installer les dépendances
```bash
pip install flask requests
```

4. Démarrer l'application
```bash
python app.py
```

5. Accéder à l'application
Ouvrez votre navigateur et allez sur : `http://localhost:5000`

## Guide d'Utilisation

### Étape 1 : Sélection des Points
1. Départ: Choisissez votre point de départ dans la liste déroulante
2. Arrivée : Sélectionnez votre destination
3. Options : Utilisez le bouton "Inverser" pour échanger départ/arrivée

### Étape 2 : Calcul des Itinéraires
1. Cliquez sur "Afficher les itinéraires (5)"
2. Attendez le calcul des différentes alternatives
3. Observez les résultats sur la carte et dans le panneau latéral

### Étape 3 : Analyse des Résultats
- Carte : Visualisez les 5 itinéraires en couleurs différentes
- Panneau latéral : Comparez distance, durée et points d'intérêt
- Popup : Cliquez sur les itinéraires pour plus de détails
- Zoom : Utilisez les boutons pour centrer sur un itinéraire spécifique

## Points de Repère Disponibles

### Principaux Landmarks
| Point de Repère | Type | Description |
|----------------|------|-------------|
| Rond-point Victoire | Carrefour | Point central de Kinshasa |
| Gare Centrale | Transport | Gare routière et ferroviaire principale |
| Gombe | Quartier | Zone administrative et commerciale |
| Lingwala | Quartier | Zone résidentielle et commerciale |
| Kasa-Vubu | Commune | Cœur populaire de Kinshasa |
| Matonge | Quartier | Zone culturelle et commerciale réputée |
| Barumbu | Commune | Zone historique près du fleuve |
| Ngaliema | Quartier | Zone résidentielle huppée |
| Lemba | Quartier | Zone universitaire et résidentielle |
| Limete | Zone | Zone industrielle et résidentielle |

### Points d'Intérêt
- Marché Central, Stade des Martyrs, Université de Kinshasa
- Palais du Peuple, Ambassade de France, Aéroport de Ndjili
- Hôpital Général, Musée National, Jardin Botanique

## API Endpoints

### `POST /api/routes`
Calcule les itinéraires entre deux points.

Body:
```json
{
  "start_name": "Rond-point Victoire",
  "end_name": "Gare Centrale", 
  "alternatives": 5
}
```

Réponse:
```json
{
  "routes": [
    {
      "distance_km": 8.2,
      "duration_min": 25.5,
      "type": "direct",
      "stops": [...],
      "geometry": {...}
    }
  ],
  "shortest_index": 0,
  "total_routes_found": 5
}
```

### `GET /api/health`
Vérification du statut de l'API.

## Contexte Local Kinshasa

### Spécificités de Mobilité
- Transport informel : Prise en compte des points de convergence naturels
- Infrastructures : Adaptation aux routes et carrefours principaux
- Points de repère: Utilisation de landmarks connus des habitants
- Trafic : Calcul basé sur les conditions routières réelles

### Données Géographiques
- Coordonnées précises : Points géolocalisés avec précision
- Routes actualisées: Basé sur les données OpenStreetMap récentes
- Context local : Points d'intérêt pertinents pour Kinshasa

##  Améliorations Futures

### Fonctionnalités Planifiées
- [ ] Intégration des transports en commun
- [ ] Calcul du coût estimé du trajet
- [ ] Alertes trafic en temps réel
- [ ] Mode hors-ligne basique
- [ ] Application mobile dédiée
- [ ] Historique des recherches
- [ ] Partage d'itinéraires

### Améliorations Techniques
- [ ] Cache des requêtes OSRM
- [ ] Base de données pour persistance
- [ ] Système de sauvegarde des favoris
- [ ] API étendue pour développeurs

##  Contribution

### Développement
Les contributions sont bienvenues ! Voici comment participer :

1. Forkez le projet
2. Créez une branche feature (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Pushez la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Amélioration des Données
- Ajout de nouveaux points de repère
- Correction de coordonnées GPS
- Ajout de photos locales
- Amélioration des descriptions

##  Licence

Ce projet est sous licence BSD - voir le fichier LICENSE pour plus de détails.



## 🙏 Remerciements

- OpenStreetMap pour les données cartographiques
- OSRM pour le calcul d'itinéraires
- Unsplash pour les images de qualité
- La communauté Kinshasa** pour les retours et suggestions
- URKIM LINGWALA notre établissement 
- Doctorant KADIMA DONATIEN pour son soutien technique 

---

Kinshasa Itinéraires - Rendre la mobilité plus intelligente dans la capitale congolaise 
