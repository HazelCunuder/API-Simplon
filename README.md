# API Simplon

## 📋 Introduction

API Simplon est une **API REST professionnelle** conçue pour digitaliser la gestion complète des formations, sessions et inscriptions au sein d'un centre de formation. Développée dans le cadre d'une formation en Data IA, cette API respecte les standards modernes de développement backend avec une architecture claire, des validations robustes et une couverture de tests.

**Client :** Simplon - Centre de formation  
**Objectif :** Moderniser la gestion des apprenants, formateurs et sessions de formation

---

## 🎯 Description

Actuellement, Simplon gère ses opérations de manière disparate :

- ❌ Les inscriptions via des tableurs
- ❌ Le suivi pédagogique dispersé dans plusieurs outils
- ❌ La gestion des sessions manuelle et peu flexible

**Notre solution** est une API REST centralisée permettant de :

- ✅ Gérer les formations et leurs contenus
- ✅ Planifier et administrer les sessions de formation
- ✅ Gérer les inscriptions et les enregistrements d'apprenants
- ✅ Authentifier les utilisateurs de manière sécurisée
- ✅ Suivre les états des sessions (planifiée, en cours, terminée)

### Fonctionnalités principales

| Fonctionnalité | Description |
|;---;|;---;|
| **Authentification** | Connexion sécurisée avec JWT |
| **Gestion des utilisateurs** | Création, modification et suppression d'utilisateurs |
| **Gestion des formations** | CRUD complet pour les formations |
| **Gestion des sessions** | Planification et suivi des sessions de formation |
| **Inscriptions** | Gestion des enregistrements d'apprenants aux sessions |
| **Validation de données** | DTOs et validation robuste de toutes les entrées |
| **Gestion des erreurs** | Codes d'erreur explicites et messages détaillés |

---

## 🏗️ Architecture

### Stack technique

- **Framework :** FastAPI
- **Base de données :** SQLAlchemy ORM + PostgreSQL
- **Migrations :** Alembic
- **Authentification :** JWT (JSON Web Tokens)
- **Validation :** Pydantic

### Structure du projet

```
.
├── alembic
│   ├── README
│   ├── env.py
│   └── versions
├── assets
│   └── MCD.png
├──src
│   ├── api
│   │   └── v1
│   │       ├── endpoints
│   │       │   ├── auth_endpoints.py
│   │       │   ├── courses_endpoints.py
│   │       │   ├── session_endpoints.py
│   │       │   ├── user_endpoints.py
│   │       │   └── user_session_endpoints.py
│   │       └── routers
│   │           └── api.py
│   ├── main.py
│   ├── model
│   │   ├── course.py
│   │   ├── database.py
│   │   ├── session.py
│   │   ├── user.py
│   │   └── user_session.py
│   ├── repositories
│   │   ├── course_repository.py
│   │   ├── session_repository.py
│   │   ├── user_repository.py
│   │   └── user_session_repo.py
│   ├── requirements.txt
│   ├── schemas
│   │   ├── auth_schema.py
│   │   ├── courses_schema.py
│   │   ├── sessions_schema.py
│   │   ├── user_schema.py
│   │   └── user_session_schema.py
│   ├── services
│   │   ├── auth_service.py
│   │   ├── courses_services.py
│   │   ├── session_services.py
│   │   ├── user_service.py
│   │   └── user_session_services.py
│   ├── tests
│   │   ├── course_test.py
│   │   ├── session_test.py
│   │   ├── user_sessions_test.py
│   │   └── user_test.py
│   └── utils
│       ├── exceptions.py
│       ├── logger.py
│       └── security.py
├── requirements.txt
└── README.md
```

### Architecture en couches

```
Endpoints (routes HTTP)
        ↓
Services (logique métier)
        ↓
Repositories (accès données)
        ↓
Models (ORM SQLAlchemy)
        ↓
Base de données
```

Chaque couche dispose de responsabilités claires et bien définies, facilitant la maintenance et l'évolution du code.

---

## 🔧 Installation

### Prérequis

- **Python** 3.9 ou supérieur
- **PostgreSQL** 12 ou supérieur
- **pip** ou `poetry`

### Étapes d'installation

1. **Cloner le repository**

   ```bash
   git clone <url-du-repository>
   cd api-simplon
   ```

2. **Créer un environnement virtuel**

   ```bash
   python -m venv venv
   source venv/bin/activate    # Sur macOS/Linux
   # ou
   venv\Scripts\activate        # Sur Windows
   ```

3. **Installer les dépendances**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement**

   Créez un fichier `.env` à la racine du projet :

   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/simplon_db
   SECRET_KEY=votre_clé_secrète_très_longue_et_aléatoire
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

5. **Initialiser la base de données**

   ```bash
   # Appliquer les migrations Alembic
   alembic upgrade head
   ```

6. **Lancer l'application**

   ```bash
   uvicorn src.main:app --reload
   ```

L'API sera accessible sur : `http://localhost:8000`

---

## 📖 Utilisation

### Accéder à la documentation interactive

FastAPI génère automatiquement une documentation interactive :

- **Swagger UI** : <http://localhost:8000/docs>
- **ReDoc** : <http://localhost:8000/redoc>

### Exemples d'utilisation

#### 1. Authentification

**Créer un utilisateur**

```bash
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "utilisateur@example.com",
  "password": "MotDePasse123!",
  "first_name": "Jean",
  "last_name": "Dupont"
}
```

**Se connecter**

```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "utilisateur@example.com",
  "password": "MotDePasse123!"
}
```

#### 2. Gestion des formations

**Créer une formation**

```bash
POST /api/v1/courses
Authorization: Bearer <votre_token>
Content-Type: application/json

{
  "title": "Python Avancé",
  "description": "Formation approfondie en Python",
  "duration_hours": 40
}
```

**Récupérer toutes les formations**

```bash
GET /api/v1/courses
```

#### 3. Gestion des sessions

**Créer une session de formation**

```bash
POST /api/v1/sessions
Authorization: Bearer <votre_token>
Content-Type: application/json

{
  "course_id": 1,
  "start_date": "2026-03-01",
  "end_date": "2026-03-31",
  "max_participants": 30
}
```

#### 4. Inscriptions

**Inscrire un utilisateur à une session**

```bash
POST /api/v1/enrollments
Authorization: Bearer <votre_token>
Content-Type: application/json

{
  "user_id": 1,
  "session_id": 1
}
```

### Exécuter les tests

```bash
# Lancer tous les tests
pytest

# Lancer avec couverture
pytest --cov=src

# Lancer un fichier de test spécifique
pytest src/tests/user_test.py
```

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer au projet :

1. **Fork** le repository
2. **Créez une branche** pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. **Commitez vos changements** (`git commit -m 'Add some AmazingFeature'`)
4. **Poussez vers la branche** (`git push origin feature/AmazingFeature`)
5. **Ouvrez une Pull Request**

### Guidelines de contribution

- Respectez la structure en couches (endpoints → services → repositories → models)
- Écrivez des tests pour chaque nouvelle fonctionnalité
- Suivez les conventions de nommage Python (PEP 8)
- Commentez le code complexe
- Mettez à jour la documentation si nécessaire

---

## 👥 Auteurs

Ce projet a été développé par une équipe de trois développeurs :

- **Hazel Cunuder** - [Github](https://github.com/HazelCunuder)
- **Ethan Puype** - [Github](https://github.com/NICHIKU)
- **Umberto Emonds** - [Github](https://github.com/UmbertoEmonds)

**Contexte :** Projet de formation Développeur Data IA - Simplon

---

## 📝 Licence

Ce projet est fourni à des fins éducatives.

---

**Dernière mise à jour :** Février 2026
