from fastapi import APIRouter, Depends, HTTPException, Query, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional
from model.user import Role
from model.course import Level
from model.session import Status
from schemas.user_schema import UserCreate, UserUpdate, UserRead
from schemas.courses_schema import CoursesCreateSchema, ModifyCoursesSchema, ShowCoursesSchema
from schemas.sessions_schema import SessionCreate, SessionUpdate, SessionRead
from schemas.user_session_schema import EnrollmentCreate, EnrollmentResponse
from services.auth_service import AuthService
from services.user_service import UserService
from services.courses_services import CourseService
from services.session_services import SessionService
from services.user_session_services import UserSessionService
from utils.security import verify_token
from model.database import get_db
from sqlalchemy.orm import Session as DBSession

router = APIRouter(prefix="/admin", include_in_schema=False)

# ============= TEMPLATE NAVBAR =============

NAVBAR_TEMPLATE = """
<nav class="navbar">
    <div class="navbar-container">
        <img src="static/simplon_logo.svg"></img>
        <div class="navbar-menu">
            <ul class="navbar-nav">
                <li><a href="/admin/users" class="nav-link">Utilisateurs</a></li>
                <li><a href="/admin/courses" class="nav-link">Cours</a></li>
                <li><a href="/admin/sessions" class="nav-link">Sessions</a></li>
                <li><a href="/admin/enrollments" class="nav-link">Inscriptions</a></li>
            </ul>
            <a href="/admin/logout" class="logout-btn">Déconnexion</a>
        </div>
    </div>
</nav>
"""

# ============= DASHBOARD PRINCIPAL =============

@router.get("/", response_class=HTMLResponse)
async def dashboard_home():
    """Page d'accueil - Permet login/signup sans authentification"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard Formation</title>
        <link rel="stylesheet" href="/admin/static/style.css">
        <style>
            .login-container {
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 80vh;
            }
            .login-box {
                background: white;
                padding: 2rem;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                width: 100%;
                max-width: 400px;
            }
            .login-box h1 {
                text-align: center;
                margin-bottom: 2rem;
            }
            .tabs {
                display: flex;
                gap: 1rem;
                margin-bottom: 2rem;
                border-bottom: 2px solid #ecf0f1;
            }
            .tabs button {
                flex: 1;
                padding: 1rem;
                background: none;
                border: none;
                border-bottom: 3px solid transparent;
                cursor: pointer;
                color: #7f8c8d;
            }
            .tabs button.active {
                color: #123744;
                border-bottom-color: #123744;
            }
            .tab-content {
                display: none;
            }
            .tab-content.active {
                display: block;
            }
        </style>
    </head>
    <body>
        <nav class="navbar">
            <div class="navbar-container">
                <img src="static/simplon_logo.svg"></img>
            </div>
        </nav>

        <div class="container">
            <div class="login-container">
                <div class="login-box">
                    <h1>Bienvenue</h1>

                    <div class="tabs">
                        <button class="tab-btn active" onclick="switchTab('login', event)">Connexion</button>
                        <button class="tab-btn" onclick="switchTab('signup', event)">Inscription</button>
                    </div>

                    <div id="login" class="tab-content active">
                        <form method="POST" action="/admin/login" class="form">
                            <input type="email" name="username" placeholder="Email" required>
                            <input type="password" name="password" placeholder="Mot de passe" required>
                            <button type="submit" class="btn-primary">Se connecter</button>
                        </form>
                    </div>

                    <div id="signup" class="tab-content">
                        <form method="POST" action="/admin/signup" class="form">
                            <input type="text" name="first_name" placeholder="Prénom" required>
                            <input type="text" name="last_name" placeholder="Nom" required>
                            <input type="email" name="email" placeholder="Email" required>
                            <input type="password" name="password" placeholder="Mot de passe" required>
                            <select name="role" required>
                                <option value="STUDENT">Étudiant</option>
                                <option value="TEACHER">Professeur</option>
                                <option value="ADMIN">Admin</option>
                            </select>
                            <button type="submit" class="btn-primary">S'inscrire</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        <script>
            function switchTab(name, e) {
                e.preventDefault();
                document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
                document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
                document.getElementById(name).classList.add('active');
                e.target.classList.add('active');
            }
        </script>
    </body>
    </html>
    """


@router.post("/login")
async def login(
        username: str = Form(...),
        password: str = Form(...),
        db: DBSession = Depends(get_db)
):
    """Login - Crée un token et redirige"""
    try:
        service = AuthService(db=db)
        token_response = service.login(username, password)

        response = RedirectResponse(url="/admin/dashboard", status_code=303)
        response.set_cookie(
            key="access_token",
            value=token_response.access_token,
            httponly=True,
            secure=False,
            samesite="lax"
        )
        return response
    except Exception as e:
        return HTMLResponse(
            status_code=401,
            content='<h1>Erreur</h1><p>Email ou mot de passe incorrect</p><a href="/admin/">Réessayer</a>'
        )


@router.post("/signup")
async def signup(
        first_name: str = Form(...),
        last_name: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        role: str = Form(default="STUDENT"),
        db: DBSession = Depends(get_db)
):
    """Signup - Crée un nouvel utilisateur"""
    try:
        service = UserService(db=db)
        user_data = UserCreate(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            role=Role[role],
            register_date=date.today()
        )
        service.create_user(user_data)
        return RedirectResponse(url="/admin/", status_code=303)
    except Exception as e:
        return HTMLResponse(
            status_code=400,
            content=f'<h1>Erreur</h1><p>{str(e)}</p><a href="/admin/">Réessayer</a>'
        )


@router.get("/dashboard", response_class=HTMLResponse)
async def main_dashboard(token: dict = Depends(verify_token)):
    """Page principale du dashboard - PROTÉGÉE"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dashboard</title>
        <link rel="stylesheet" href="/admin/static/style.css">
    </head>
    <body>
        {NAVBAR_TEMPLATE}
        <div class="container">
            <h2>Bienvenue sur le Dashboard</h2>
            <p>Sélectionnez une section dans le menu pour commencer.</p>
        </div>
    </body>
    </html>
    """


@router.get("/logout")
async def logout():
    """Déconnexion"""
    response = RedirectResponse(url="/admin/", status_code=303)
    response.delete_cookie("access_token")
    return response


# ============= USERS =============

@router.get("/users", response_class=HTMLResponse)
async def users_page(
    search: str = Query(default=""),
    token: dict = Depends(verify_token),
    db: DBSession = Depends(get_db)
):
    """Liste des utilisateurs avec filtre par nom/prénom"""
    service = UserService(db=db)
    try:
        users = service.get_all_users()
        
        if search:
            search_lower = search.lower()
            users = [u for u in users if search_lower in u.first_name.lower() or search_lower in u.last_name.lower()]
        
        users_html = "".join([
            f"""
            <tr>
                <td>{u.id}</td>
                <td>{u.first_name} {u.last_name}</td>
                <td>{u.email}</td>
                <td>{u.role}</td>
                <td>
                    <a href="/admin/users/{u.id}/delete" class="btn-delete" onclick="return confirm('Confirmer?')">Supprimer</a>
                </td>
            </tr>
            """ for u in users
        ])
    except:
        users_html = "<tr><td colspan='5'>Erreur lors du chargement des utilisateurs</td></tr>"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Utilisateurs</title>
        <link rel="stylesheet" href="/admin/static/style.css">
    </head>
    <body>
        {NAVBAR_TEMPLATE}
        <div class="container">
            <div class="section">
                <h2>Rechercher</h2>
                <form method="GET" action="/admin/users" class="form" style="max-width: 300px;">
                    <input type="text" name="search" placeholder="Nom ou prénom..." value="{search}">
                    <button type="submit" class="btn-primary">Rechercher</button>
                </form>
            </div>

            <div class="section">
                <h2>Liste des utilisateurs</h2>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nom</th>
                            <th>Email</th>
                            <th>Rôle</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users_html}
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """


# ============= COURSES =============

@router.get("/courses", response_class=HTMLResponse)
async def courses_page(
    token: dict = Depends(verify_token),
    db: DBSession = Depends(get_db)
):
    """Liste des cours avec formulaire de création"""
    from repositories.course_repository import CourseRepository
    service = CourseService(repo=CourseRepository(db=db))
    try:
        courses = service.get_courses()
        courses_html = "".join([
            f"""
            <tr>
                <td>{c.id}</td>
                <td>{c.title}</td>
                <td>{c.description[:50]}...</td>
                <td>{c.duration} h</td>
                <td>{c.level}</td>
                <td>
                    <a href="/admin/courses/{c.id}/delete" class="btn-delete" onclick="return confirm('Confirmer?')">Supprimer</a>
                </td>
            </tr>
            """ for c in courses
        ])
    except:
        courses_html = "<tr><td colspan='6'>Erreur lors du chargement des cours</td></tr>"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cours</title>
        <link rel="stylesheet" href="/admin/static/style.css">
    </head>
    <body>
        {NAVBAR_TEMPLATE}
        <div class="container">
            <div class="section">
                <h2>Ajouter un cours</h2>
                <form method="POST" action="/admin/courses/create" class="form">
                    <input type="text" name="title" placeholder="Titre" required maxlength="255">
                    <textarea name="description" placeholder="Description" required></textarea>
                    <input type="number" name="duration" placeholder="Durée (heures)" required min="1">
                    <select name="level" required>
                        <option value="BEGINNER">Débutant</option>
                        <option value="INTERMEDIATE">Intermédiaire</option>
                        <option value="ADVANCED">Avancé</option>
                    </select>
                    <button type="submit" class="btn-primary">Ajouter</button>
                </form>
            </div>

            <div class="section">
                <h2>Liste des cours</h2>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Titre</th>
                            <th>Description</th>
                            <th>Durée</th>
                            <th>Niveau</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {courses_html}
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """


@router.post("/courses/create")
async def create_course_form(
    title: str = Form(...),
    description: str = Form(...),
    duration: int = Form(..., gt=0),
    level: str = Form(default="BEGINNER"),
    token: dict = Depends(verify_token),
    db: DBSession = Depends(get_db)
):
    """Créer un cours depuis le formulaire"""
    from repositories.course_repository import CourseRepository
    service = CourseService(repo=CourseRepository(db=db))
    try:
        course_data = CoursesCreateSchema(
            title=title,
            description=description,
            duration=duration,
            level=Level[level]
        )
        service.create(course_data)
        return RedirectResponse(url="/admin/courses", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============= SESSIONS =============

@router.get("/sessions", response_class=HTMLResponse)
async def sessions_page(
    token: dict = Depends(verify_token),
    db: DBSession = Depends(get_db)
):
    """Liste des sessions avec formulaire de création"""
    service = SessionService(db=db)
    try:
        sessions = service.get_all_sessions()
        sessions_html = "".join([
            f"""
            <tr>
                <td>{s.id}</td>
                <td>{s.course_id}</td>
                <td>{s.start_date}</td>
                <td>{s.end_date}</td>
                <td>{s.capacity}</td>
                <td>{s.status}</td>
                <td>
                    <a href="/admin/sessions/{s.id}/delete" class="btn-delete" onclick="return confirm('Confirmer?')">Supprimer</a>
                </td>
            </tr>
            """ for s in sessions
        ])
    except:
        sessions_html = "<tr><td colspan='7'>Erreur lors du chargement des sessions</td></tr>"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sessions</title>
        <link rel="stylesheet" href="/admin/static/style.css">
    </head>
    <body>
        {NAVBAR_TEMPLATE}
        <div class="container">
            <div class="section">
                <h2>Ajouter une session</h2>
                <form method="POST" action="/admin/sessions/create" class="form">
                    <input type="number" name="course_id" placeholder="ID du cours" required>
                    <input type="date" name="start_date" required>
                    <input type="date" name="end_date" required>
                    <input type="number" name="capacity" placeholder="Capacité" required min="1">
                    <button type="submit" class="btn-primary">Ajouter</button>
                </form>
            </div>

            <div class="section">
                <h2>Liste des sessions</h2>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Cours</th>
                            <th>Début</th>
                            <th>Fin</th>
                            <th>Capacité</th>
                            <th>Statut</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {sessions_html}
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    """


@router.post("/sessions/create")
async def create_session_form(
    course_id: int = Form(...),
    start_date: date = Form(...),
    end_date: date = Form(...),
    capacity: int = Form(..., gt=0),
    token: dict = Depends(verify_token),
    db: DBSession = Depends(get_db)
):
    """Créer une session depuis le formulaire"""
    service = SessionService(db=db)
    try:
        session_data = SessionCreate(
            course_id=course_id,
            start_date=start_date,
            end_date=end_date,
            capacity=capacity
        )
        service.create_session(session_data)
        return RedirectResponse(url="/admin/sessions", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ============= ENROLLMENTS =============

@router.get("/enrollments", response_class=HTMLResponse)
async def enrollments_page(
    token: dict = Depends(verify_token),
    db: DBSession = Depends(get_db)
):
    """Page des inscriptions"""
    user_service = UserService(db=db)
    session_service = SessionService(db=db)
    enrollment_service = UserSessionService(db)
    
    try:
        users = user_service.get_all_users()
        sessions = session_service.get_all_sessions()
        enrollments = enrollment_service.get_enrollments()
        
        users_options = "".join([f'<option value="{u.id}">{u.first_name} {u.last_name}</option>' for u in users])
        sessions_options = "".join([f'<option value="{s.id}">Session {s.id} - Cours {s.course_id} ({s.start_date})</option>' for s in sessions])
        
        enrollments_html = "".join([
            f"""
            <tr>
                <td>{e.id}</td>
                <td>{e.user_id}</td>
                <td>{e.session_id}</td>
                <td>{e.enrollment_date}</td>
                <td><a href="/admin/enrollments/{e.id}/delete?user_id={e.user_id}&session_id={e.session_id}" class="btn-delete" onclick="return confirm('Confirmer?')">Supprimer</a></td>
            </tr>
            """ for e in enrollments
        ])
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Inscriptions</title>
            <link rel="stylesheet" href="/admin/static/style.css">
        </head>
        <body>
            {NAVBAR_TEMPLATE}
            <div class="container">
                <div class="section">
                    <h2>Inscrire un utilisateur</h2>
                    <form method="POST" action="/admin/enrollments/create" class="form">
                        <select name="user_id" required>
                            <option value="">Sélectionnez un utilisateur</option>
                            {users_options}
                        </select>
                        <select name="session_id" required>
                            <option value="">Sélectionnez une session</option>
                            {sessions_options}
                        </select>
                        <button type="submit" class="btn-primary">Inscrire</button>
                    </form>
                </div>

                <div class="section">
                    <h2>Liste des inscriptions</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>ID</th>
                                <th>Utilisateur ID</th>
                                <th>Session ID</th>
                                <th>Date d'inscription</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {enrollments_html if enrollments_html else "<tr><td colspan='5'>Aucune inscription</td></tr>"}
                        </tbody>
                    </table>
                </div>
            </div>
        </body>
        </html>
        """
    except Exception as e:
        return HTMLResponse(
            status_code=400,
            content=f'{NAVBAR_TEMPLATE}<div class="container"><h1>Erreur</h1><p>{str(e)}</p></div>'
        )


@router.post("/enrollments/create")
async def create_enrollment_form(
    user_id: int = Form(...),
    session_id: int = Form(...),
    token: dict = Depends(verify_token),
    db: DBSession = Depends(get_db)
):
    """Créer une inscription"""
    service = UserSessionService(db)
    try:
        service.enroll_student(user_id, session_id)
        return RedirectResponse(url="/admin/enrollments", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/enrollments/{enrollment_id}/delete")
async def delete_enrollment_direct(
    enrollment_id: int,
    user_id: int = Query(...),
    session_id: int = Query(...),
    token: dict = Depends(verify_token),
    db: DBSession = Depends(get_db)
):
    """Supprimer une inscription"""
    service = UserSessionService(db)
    try:
        service.unenroll_student(user_id, session_id)
        return RedirectResponse(url="/admin/enrollments", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
