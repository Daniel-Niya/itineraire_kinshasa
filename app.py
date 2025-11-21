from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import random
import base64
import os
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

def image_to_base64(image_path):
    """Convertit une image en base64 avec gestion d'erreur"""
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                # Déterminer le type MIME basé sur l'extension
                if image_path.lower().endswith('.webp'):
                    mime_type = "webp"
                elif image_path.lower().endswith('.jpg') or image_path.lower().endswith('.jpeg'):
                    mime_type = "jpeg"
                elif image_path.lower().endswith('.png'):
                    mime_type = "png"
                else:
                    mime_type = "jpeg"  # défaut
                return f"data:image/{mime_type};base64,{encoded_string}"
        else:
            print(f"Image non trouvée: {image_path}")
            return None
    except Exception as e:
        print(f"Erreur conversion image {image_path}: {e}")
        return None

def get_landmark_image(landmark_name, local_path=None):
    """Retourne l'image d'un landmark avec fallback"""
    if local_path:
        base64_image = image_to_base64(local_path)
        if base64_image:
            return base64_image
    
    # Images par défaut depuis Unsplash
    default_images = {
        "Rond-point Victoire": "https://images.unsplash.com/photo-1580651315530-69c8e0026375?w=400&h=300&fit=crop",
        "Gare Centrale": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=400&h=300&fit=crop",
        "Gombe": "https://images.unsplash.com/photo-1574786351745-ba6c11bf7c52?w=400&h=300&fit=crop",
        "Lingwala": "https://images.unsplash.com/photo-1558002037-f4d8b18df6b9?w=400&h=300&fit=crop",
        "Kasa-Vubu": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&h=300&fit=crop",
        "Matonge": "https://images.unsplash.com/photo-1552733407-5d5c46c3bb3b?w=400&h=300&fit=crop",
        "Barumbu": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&h=300&fit=crop",
        "Ngaliema": "https://images.unsplash.com/photo-1464822759844-d94c9f9e6f67?w=400&h=300&fit=crop",
        "Lemba": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop",
        "Limete": "https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=400&h=300&fit=crop"
    }
    return default_images.get(landmark_name, "https://images.unsplash.com/photo-1552733407-5d5c46c3bb3b?w=400&h=300&fit=crop")

# Coordonnées corrigées basées sur vos données (NE PAS CHANGER)
LANDMARKS = {
    "Rond-point Victoire": {
        "lat": -4.340787, 
        "lon": 15.313731,
        "image": get_landmark_image("Rond-point Victoire", "/Users/mac/Downloads/conduite/Project/static/uploads/victoire.webp"),
        "description": "Point central de Kinshasa, lieu de rassemblement important"
    },
    "Gare Centrale": { 
        "lat": -4.301203, 
        "lon": 15.317859,
        "image": get_landmark_image("Gare Centrale", "/Users/mac/Downloads/conduite/Project/static/uploads/gare.jpg"),
        "description": "Principale gare routière et ferroviaire de Kinshasa"
    }, 
    "Gombe": {
        "lat": -4.30306, 
        "lon": 15.30333,
        "image": get_landmark_image("Gombe", "/Users/mac/Downloads/conduite/Project/static/uploads/Gombe.jpeg"),
        "description": "Quartier administratif et commercial"
    },
    "Lingwala": {
        "lat": -4.325425071279868,
        "lon": 15.296128605102115,
        "image": get_landmark_image("Lingwala", "/Users/mac/Downloads/conduite/Project/static/uploads/lingwala.png"),
        "description": "Quartier résidentiel et commercial animé"
    },
    "Kasa-Vubu": {
        "lat": -4.34250, 
        "lon": 15.30528,
        "image": get_landmark_image("Kasavubu", "/Users/mac/Downloads/conduite/Project/static/uploads/KASAVUBU.jpeg"),
        "description": "Commune populaire au cœur de Kinshasa"
    },
    "Matonge": {
        "lat": -4.34022, 
        "lon": 15.31599,
        "image": get_landmark_image("Matonge", "/Users/mac/Downloads/conduite/Project/static/uploads/matonge.png"),
        "description": "Quartier culturel et commercial réputé"
    },
    "Barumbu": {
        "lat": -4.31694, 
        "lon": 15.32778,
        "image": get_landmark_image("Barumbu", "/Users/mac/Downloads/conduite/Project/static/uploads/ndolo.jpeg"),
        "description": "Commune historique près du fleuve Congo"
    },
    "Ngaliema": {
        "lat": -4.37247, 
        "lon": 15.25459,
        "image": get_landmark_image("Ngaliema", "/Users/mac/Downloads/conduite/Project/static/uploads/ngaliema.webp"),
        "description": "Quartier résidentiel huppé avec vue sur le fleuve"
    },
    "Lemba": {
        "lat": -4.39611, 
        "lon": 15.31917,
        "image": get_landmark_image("Lemba", "/Users/mac/Downloads/conduite/Project/static/uploads/lemba.jpeg"),
        "description": "Quartier universitaire et résidentiel"
    },
    "Limete": {
        "lat": -4.37439, 
        "lon": 15.34542,
        "image": get_landmark_image("Limete", "/Users/mac/Downloads/conduite/Project/static/uploads/limete.jpeg"),
        "description": "Zone industrielle et résidentielle importante"
    }
}

# Points d'intérêt: coordonnées réalistes et positionnées sur/près des routes principales
POINTS_OF_INTEREST = {
    "Marché Central": {
        "lat": -4.3070,
        "lon": 15.3120,
        "image": get_landmark_image("Marché Central", "/Users/mac/Downloads/conduite/Project/static/uploads/marche_central.jpeg"),
        "type": "commerce",
        "description": "Grand marché situé sur un axe commercial proche de Gombe/Victoire"
    },
    "Stade des Martyrs": {
        "lat": -4.3278,
        "lon": 15.3149,
        "image": get_landmark_image("Stade des Martyrs", "/Users/mac/Downloads/conduite/Project/static/uploads/stade_martyrs.jpeg"),
        "type": "sport",
        "description": "Stade national situé le long d'un grand boulevard"
    },
    "Université de Kinshasa": {
        "lat": -4.4120,
        "lon": 15.3050,
        "image": get_landmark_image("Université de Kinshasa", "/Users/mac/Downloads/conduite/Project/static/uploads/unikin.jpeg"),
        "type": "éducation",
        "description": "Campus universitaire à Lemba, accessible par la route principale"
    },
    "Place de la Gare": {
        "lat": -4.30125,
        "lon": 15.31800,
        "image": get_landmark_image("Place de la Gare", "/Users/mac/Downloads/conduite/Project/static/uploads/place_gare.jpeg"),
        "type": "transport",
        "description": "Place immédiatement devant la Gare Centrale"
    },
    "Hôpital Général": {
        "lat": -4.3145,
        "lon": 15.2920,
        "image": get_landmark_image("Hôpital Général", "/Users/mac/Downloads/conduite/Project/static/uploads/images.jpeg"),
        "type": "santé",
        "description": "Hôpital principal sur un axe médical bien desservi"
    },
    "Tour de l'Échangeur": {
        "lat": -4.3245,
        "lon": 15.3048,
        "image": get_landmark_image("Tour de l'Échangeur", "/Users/mac/Downloads/conduite/Project/static/uploads/limete.jpeg"),
        "type": "infrastructure",
        "description": "Intersection / échangeur important sur le réseau routier"
    },
    "Palais du Peuple": {
        "lat": -4.3198,
        "lon": 15.3152,
        "image": get_landmark_image("Palais du Peuple", "/Users/mac/Downloads/conduite/Project/static/uploads/palais-du-peuple.jpg"),
        "type": "gouvernement",
        "description": "Siège du parlement, situé en zone administrative"
    },
    "Ambassade de France": {
        "lat": -4.3079,
        "lon": 15.2751,
        "image": get_landmark_image("Ambassade de France", "/Users/mac/Downloads/conduite/Project/static/uploads/ambassade_de_france.jpeg"),
        "type": "diplomatie",
        "description": "Représentation diplomatique sur un axe sécurisé"
    },
    "Aéroport de Ndjili": {
        "lat": -4.3850,
        "lon": 15.4448,
        "image": get_landmark_image("Aéroport de Ndjili", "/Users/mac/Downloads/conduite/Project/static/uploads/ndjili.jpeg"),
        "type": "transport",
        "description": "Aéroport international, connecté via la route d'accès principale"
    },
    "Pont Maréchal": {
        "lat": -4.3005,
        "lon": 15.2945,
        "image": get_landmark_image("Pont Maréchal", "/Users/mac/Downloads/conduite/Project/static/uploads/pont_marechal.jpeg"),
        "type": "infrastructure",
        "description": "Pont sur le fleuve/local, positionné sur un axe routier stratégique"
    },
    "Stade Tata Raphaël": {
        "lat": -4.3385,
        "lon": 15.2810,
        "image": get_landmark_image("Stade Tata Raphaël", "/Users/mac/Downloads/conduite/Project/static/uploads/matonge.png"),
        "type": "sport",
        "description": "Stade historique accessible depuis les grands boulevards"
    },
    "Musée National": {
        "lat": -4.3183,
        "lon": 15.2982,
        "image": get_landmark_image("Musée National", "/Users/mac/Downloads/conduite/Project/static/uploads/musee_national.jpeg"),
        "type": "culture",
        "description": "Musée situé proche d'axes piétonniers et routiers principaux"
    },
    "Jardin Botanique": {
        "lat": -4.3495,
        "lon": 15.2952,
        "image": get_landmark_image("Jardin Botanique", "/Users/mac/Downloads/conduite/Project/static/uploads/jardin.jpeg"),
        "type": "nature",
        "description": "Espace vert en périphérie, accessible par une route secondaire connectée"
    },
    "Grand Hôtel Kinshasa": {
        "lat": -4.3021,
        "lon": 15.3022,
        "image": get_landmark_image("Grand Hôtel Kinshasa", "/Users/mac/Downloads/conduite/Project/static/uploads/grand_hotel.jpeg"),
        "type": "hôtellerie",
        "description": "Hôtel situé sur un axe hôtelier près du centre"
    },
    "Centre Commercial": {
        "lat": -4.3075,
        "lon": 15.3048,
        "image": get_landmark_image("Centre Commercial", "/Users/mac/Downloads/conduite/Project/static/uploads/commercial.jpeg"),
        "type": "commerce",
        "description": "Grand centre commercial sur un boulevard principal"
    }
}
OSRM_BASE = "https://router.project-osrm.org"

# Route pour servir les images
@app.route('/uploads/<filename>')
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calcule la distance en km entre deux points géographiques"""
    R = 6371
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)
    
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = sin(dlat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c

def generate_intermediate_points(start, end, num_points=3):
    """Génère des points intermédiaires pour créer des itinéraires alternatifs"""
    points = []
    mid_lat = (start["lat"] + end["lat"]) / 2
    mid_lon = (start["lon"] + end["lon"]) / 2
    
    for i in range(num_points):
        variation_lat = random.uniform(-0.02, 0.02)
        variation_lon = random.uniform(-0.02, 0.02)
        points.append({
            "lat": mid_lat + variation_lat,
            "lon": mid_lon + variation_lon
        })
    
    return points

def get_route_via_waypoints(start, end, waypoints=None):
    """Obtient un itinéraire via des points de passage"""
    if waypoints is None:
        waypoints = []
    
    coords_list = [f"{start['lon']},{start['lat']}"]
    for wp in waypoints:
        coords_list.append(f"{wp['lon']},{wp['lat']}")
    coords_list.append(f"{end['lon']},{end['lat']}")
    coords = ";".join(coords_list)
    
    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "false",
        "alternatives": "false"
    }
    
    url = f"{OSRM_BASE}/route/v1/driving/{coords}"
    
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Erreur OSRM avec waypoints: {e}")
        return None

def generate_stops_for_route(route_type, start, end, route_index):
    """Génère des arrêts pertinents pour un itinéraire donné"""
    route_stops_templates = {
        "direct": [
            ["Marché Central", "Place de la Gare", "Centre Commercial"],
            ["Tour de l'Échangeur", "Grand Hôtel Kinshasa", "Palais du Peuple"],
            ["Hôpital Général", "Musée National", "Jardin Botanique"]
        ],
        "via_intermediate": [
            ["Stade des Martyrs", "Palais du Peuple", "Tour de l'Échangeur"],
            ["Pont Maréchal", "Centre Commercial", "Grand Hôtel Kinshasa"],
            ["Stade Tata Raphaël", "Musée National", "Jardin Botanique"]
        ],
        "via_landmark": [
            ["Université de Kinshasa", "Ambassade de France", "Aéroport de Ndjili"],
            ["Marché Central", "Palais du Peuple", "Stade des Martyrs"],
            ["Hôpital Général", "Centre Commercial", "Grand Hôtel Kinshasa"]
        ]
    }
    
    template_key = route_type if route_type in route_stops_templates else "direct"
    templates = route_stops_templates[template_key]
    selected_template = templates[route_index % len(templates)]
    
    filtered_stops = []
    for stop_name in selected_template:
        if stop_name in POINTS_OF_INTEREST:
            stop_coords = POINTS_OF_INTEREST[stop_name]
            dist_to_start = calculate_distance(start["lat"], start["lon"], 
                                             stop_coords["lat"], stop_coords["lon"])
            dist_to_end = calculate_distance(stop_coords["lat"], stop_coords["lon"],
                                           end["lat"], end["lon"])
            direct_dist = calculate_distance(start["lat"], start["lon"], end["lat"], end["lon"])
            
            # on garde les arrêts qui restent raisonnables le long du trajet
            if (dist_to_start + dist_to_end) < direct_dist * 2.0:
                stop_info = POINTS_OF_INTEREST[stop_name].copy()
                stop_info["name"] = stop_name
                filtered_stops.append(stop_info)
    
    # Si pas assez d'arrêts filtrés, retourner les premiers modèles (fallback)
    if len(filtered_stops) >= 2:
        return filtered_stops[:3]
    else:
        fallback = []
        for stop in selected_template[:3]:
            poi = POINTS_OF_INTEREST.get(stop)
            if poi:
                entry = poi.copy()
                entry["name"] = stop
                fallback.append(entry)
            else:
                fallback.append({"name": stop, "description": "Point d'intérêt", "image": get_landmark_image(stop, "static/uploads/placeholder.webp")})
        return fallback

@app.route("/")
def index():
    return render_template("index.html", landmarks=sorted(LANDMARKS.keys()))

@app.route("/api/routes", methods=["POST"])
def api_routes():
    data = request.get_json(force=True)

    if "start_name" in data:
        sname = data["start_name"]
        if sname not in LANDMARKS:
            return jsonify({"error": f"Start landmark '{sname}' unknown"}), 400
        start = LANDMARKS[sname].copy()
        start["name"] = sname
    elif "start" in data:
        start = data["start"]
        start["name"] = "Point de départ"
    else:
        return jsonify({"error": "start or start_name required"}), 400

    if "end_name" in data:
        ename = data["end_name"]
        if ename not in LANDMARKS:
            return jsonify({"error": f"End landmark '{ename}' unknown"}), 400
        end = LANDMARKS[ename].copy()
        end["name"] = ename
    elif "end" in data:
        end = data["end"]
        end["name"] = "Point d'arrivée"
    else:
        return jsonify({"error": "end or end_name required"}), 400

    alternatives = int(data.get("alternatives", 5))
    if alternatives < 1:
        alternatives = 1
    if alternatives > 8:
        alternatives = 8

    routes = []
    
    # 1. Itinéraire direct (OSRM standard)
    coords = f"{start['lon']},{start['lat']};{end['lon']},{end['lat']}"
    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "false",
        "alternatives": "true"
    }
    url = f"{OSRM_BASE}/route/v1/driving/{coords}"

    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        osrm = r.json()
        
        if "routes" in osrm and len(osrm["routes"]) > 0:
            for idx, route in enumerate(osrm["routes"][:min(3, alternatives)]):
                dist_km = route.get("distance", 0) / 1000.0
                dur_min = route.get("duration", 0) / 60.0
                stops = generate_stops_for_route("direct", start, end, idx)
                
                routes.append({
                    "distance_km": round(dist_km, 3),
                    "duration_min": round(dur_min, 1),
                    "geometry": route.get("geometry"),
                    "summary": route.get("legs", [{}])[0].get("summary", ""),
                    "type": "direct",
                    "stops": stops
                })
    except Exception as e:
        print(f"Erreur OSRM direct: {e}")

    # 2. Générer des itinéraires avec points intermédiaires
    if len(routes) < alternatives:
        intermediate_points = generate_intermediate_points(start, end, num_points=5)
        
        for i, point in enumerate(intermediate_points):
            if len(routes) >= alternatives:
                break
                
            route_data = get_route_via_waypoints(start, end, [point])
            
            if route_data and "routes" in route_data and len(route_data["routes"]) > 0:
                route = route_data["routes"][0]
                dist_km = route.get("distance", 0) / 1000.0
                dur_min = route.get("duration", 0) / 60.0
                
                is_unique = True
                for existing_route in routes:
                    existing_dist = existing_route["distance_km"]
                    if abs(dist_km - existing_dist) < 0.5:
                        is_unique = False
                        break
                
                if is_unique:
                    stops = generate_stops_for_route("via_intermediate", start, end, len(routes))
                    routes.append({
                        "distance_km": round(dist_km, 3),
                        "duration_min": round(dur_min, 1),
                        "geometry": route.get("geometry"),
                        "summary": route.get("legs", [{}])[0].get("summary", ""),
                        "type": "via_intermediate",
                        "stops": stops
                    })

    # 3. Utiliser des landmarks comme points de passage
    if len(routes) < alternatives:
        potential_waypoints = []
        
        for landmark_name, landmark_coords in LANDMARKS.items():
            if (landmark_coords["lat"] == start["lat"] and landmark_coords["lon"] == start["lon"]) or \
               (landmark_coords["lat"] == end["lat"] and landmark_coords["lon"] == end["lon"]):
                continue
            
            dist_to_start = calculate_distance(start["lat"], start["lon"], 
                                             landmark_coords["lat"], landmark_coords["lon"])
            dist_to_end = calculate_distance(landmark_coords["lat"], landmark_coords["lon"],
                                           end["lat"], end["lon"])
            direct_dist = calculate_distance(start["lat"], start["lon"], end["lat"], end["lon"])
            
            if (dist_to_start + dist_to_end) < direct_dist * 1.8:
                potential_waypoints.append(landmark_coords)
        
        for i, waypoint in enumerate(potential_waypoints[:3]):
            if len(routes) >= alternatives:
                break
                
            route_data = get_route_via_waypoints(start, end, [waypoint])
            
            if route_data and "routes" in route_data and len(route_data["routes"]) > 0:
                route = route_data["routes"][0]
                dist_km = route.get("distance", 0) / 1000.0
                dur_min = route.get("duration", 0) / 60.0
                
                is_unique = True
                for existing_route in routes:
                    existing_dist = existing_route["distance_km"]
                    if abs(dist_km - existing_dist) < 0.5:
                        is_unique = False
                        break
                
                if is_unique:
                    stops = generate_stops_for_route("via_landmark", start, end, len(routes))
                    routes.append({
                        "distance_km": round(dist_km, 3),
                        "duration_min": round(dur_min, 1),
                        "geometry": route.get("geometry"),
                        "summary": route.get("legs", [{}])[0].get("summary", ""),
                        "type": "via_landmark",
                        "stops": stops
                    })

    if len(routes) == 0:
        return jsonify({"error": "Aucun itinéraire trouvé"}), 404

    routes.sort(key=lambda x: x["distance_km"])
    shortest_index = 0

    return jsonify({
        "start": start,
        "end": end,
        "routes": routes,
        "shortest_index": shortest_index,
        "total_routes_found": len(routes),
        "osrm_raw_code": 200
    })

@app.route("/api/health")
def health_check():
    return jsonify({"status": "healthy", "service": "Kinshasa Routes API"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
