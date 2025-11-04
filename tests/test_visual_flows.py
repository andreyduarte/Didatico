import pytest
from playwright.sync_api import Page, expect
from app.services.theme_config import get_theme_layouts
from app import create_app, db
from app.models import Lesson, Slide
import time

def test_visual_flows(page: Page):
    # Base URL for the web application
    base_url = "http://127.0.0.1:5000"

    # Create screenshots directory
    import os
    os.makedirs("tests/screenshots", exist_ok=True)

    # --- Setup: Create lesson and slides directly in the database ---
    app = create_app()
    with app.app_context():
        # Find the test user
        from app.models import User
        user = User.query.filter_by(email="testuser@example.com").first()
        if not user:
            # This should not happen if init-db was run, but as a fallback
            user = User(email="testuser@example.com")
            user.set_password("password")
            db.session.add(user)
            db.session.commit()

        # Create a lesson
        lesson = Lesson.query.filter_by(slug="my-test-lesson", user_id=user.id).first()
        if not lesson:
            lesson = Lesson(user_id=user.id, title="My Test Lesson", slug="my-test-lesson", published=False)
            db.session.add(lesson)
            db.session.commit()

        # Delete existing slides for this lesson to ensure a clean slate
        Slide.query.filter_by(lesson_id=lesson.id).delete()

        # Create a slide for each layout
        layouts = get_theme_layouts("default")
        for i, layout in enumerate(layouts):
            slide = Slide(lesson_id=lesson.id, order=i, layout=layout['value'], content_html=f"<h1>{layout['label']}</h1>")
            db.session.add(slide)

        # Publish the lesson
        lesson.published = True
        db.session.commit()

    # 1. Login
    page.goto(f"{base_url}/auth/login")
    page.screenshot(path="tests/screenshots/01_login_page.png")
    page.fill('input[name="email"]', "testuser@example.com")
    page.fill('input[name="password"]', "password")
    page.click('input[type="submit"]')
    expect(page).to_have_url(f"{base_url}/")
    page.screenshot(path="tests/screenshots/02_dashboard_after_login.png")

    # 2. View Lesson and All Slides
    # We can navigate directly to the URL since we know it
    lesson_page_url = f"{base_url}/c/my-test-lesson"
    page.goto(lesson_page_url)
    expect(page).to_have_url(lesson_page_url)

    # Wait for the first slide to be visible
    page.wait_for_selector('.slide')

    for i in range(len(layouts)):
        page.screenshot(path=f"tests/screenshots/03_view_slide_{i+1}_{layouts[i]['value']}.png")
        page.keyboard.press('ArrowRight')
        time.sleep(0.5) # Wait for slide transition
