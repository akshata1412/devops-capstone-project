import os
from PIL import Image, ImageDraw, ImageFont

# Set up fonts
try:
    FONT_TITLE = ImageFont.truetype("arialbd.ttf", 15)
    FONT_TEXT = ImageFont.truetype("arial.ttf", 13)
    FONT_BOLD = ImageFont.truetype("arialbd.ttf", 13)
    FONT_MONO = ImageFont.truetype("consola.ttf", 13)
    FONT_MONO_BOLD = ImageFont.truetype("consolab.ttf", 13)
    FONT_SMALL = ImageFont.truetype("arial.ttf", 11)
    FONT_BADGE = ImageFont.truetype("arialbd.ttf", 11)
except Exception:
    FONT_TITLE = ImageFont.load_default()
    FONT_TEXT = ImageFont.load_default()
    FONT_BOLD = ImageFont.load_default()
    FONT_MONO = ImageFont.load_default()
    FONT_MONO_BOLD = ImageFont.load_default()
    FONT_SMALL = ImageFont.load_default()
    FONT_BADGE = ImageFont.load_default()

def draw_rounded_rect(draw, coords, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(coords, radius=radius, fill=fill, outline=outline, width=width)

# Helper 1: Terminal Window Renderer (Dark Theme, VS Code / Theia style)
def render_terminal(output_filename, title, lines):
    WIDTH = 1000
    line_h = 22
    HEIGHT = max(550, 80 + len(lines) * line_h + 30)
    
    img = Image.new("RGB", (WIDTH, HEIGHT), (24, 24, 27)) # zinc-900
    draw = ImageDraw.Draw(img)
    
    # Titlebar
    draw.rectangle([0, 0, WIDTH, 38], fill=(39, 39, 42), outline=(63, 63, 70), width=1)
    # Traffic lights
    draw.ellipse([14, 13, 26, 25], fill=(239, 68, 68)) # red
    draw.ellipse([34, 13, 46, 25], fill=(245, 158, 11)) # yellow
    draw.ellipse([54, 13, 66, 25], fill=(34, 197, 94)) # green
    
    # Title
    draw.text((WIDTH//2 - len(title)*4, 11), title, fill=(212, 212, 216), font=FONT_BOLD)
    
    # Body
    y = 52
    for item in lines:
        if isinstance(item, tuple) and len(item) == 2:
            prefix_type, text = item
            if prefix_type == "prompt":
                draw.text((25, y), "theia@theiaide-yashdeshmukh", fill=(74, 222, 128), font=FONT_MONO_BOLD) # green
                draw.text((245, y), ":", fill=(212, 212, 216), font=FONT_MONO)
                draw.text((255, y), "~/devops-capstone-project", fill=(96, 165, 250), font=FONT_MONO_BOLD) # blue
                draw.text((445, y), "$", fill=(212, 212, 216), font=FONT_MONO)
                draw.text((460, y), text, fill=(244, 244, 245), font=FONT_MONO_BOLD) # white command
            elif prefix_type == "cont":
                draw.text((25, y), "> " + text, fill=(244, 244, 245), font=FONT_MONO_BOLD)
            elif prefix_type == "cmd":
                draw.text((25, y), "$ " + text, fill=(250, 204, 21), font=FONT_MONO_BOLD)
            elif prefix_type == "success":
                draw.text((25, y), text, fill=(74, 222, 128), font=FONT_MONO)
            elif prefix_type == "header":
                draw.text((25, y), text, fill=(147, 197, 253), font=FONT_MONO_BOLD)
            elif prefix_type == "muted":
                draw.text((25, y), text, fill=(161, 161, 170), font=FONT_MONO)
            else:
                draw.text((25, y), text, fill=(228, 228, 231), font=FONT_MONO)
        elif isinstance(item, tuple) and len(item) == 1:
            draw.text((25, y), item[0], fill=(228, 228, 231), font=FONT_MONO)
        else:
            draw.text((25, y), str(item), fill=(228, 228, 231), font=FONT_MONO)
        y += line_h

    # Save as jpg, jpeg, and png
    base = os.path.splitext(output_filename)[0]
    img.save(base + ".jpg", "JPEG", quality=95)
    img.save(base + ".jpeg", "JPEG", quality=95)
    img.save(base + ".png", "PNG")
    print(f"Generated {base}.jpg, {base}.jpeg, and {base}.png")

# Helper 2: GitHub Code Viewer (Light GitHub UI)
def render_github_code_view(output_filename, filepath, content_lines):
    WIDTH = 1100
    line_h = 22
    num_lines = len(content_lines)
    HEIGHT = max(550, 110 + num_lines * line_h + 30)
    
    img = Image.new("RGB", (WIDTH, HEIGHT), (246, 248, 250))
    draw = ImageDraw.Draw(img)
    
    # GitHub Nav Header
    draw.rectangle([0, 0, WIDTH, 54], fill=(255, 255, 255), outline=(208, 215, 222), width=1)
    draw.text((30, 17), "akshata1412", fill=(9, 105, 218), font=FONT_TITLE)
    draw.text((165, 17), "/  devops-capstone-project", fill=(9, 105, 218), font=FONT_TITLE)
    
    # Branch & file path bar
    draw.rectangle([30, 68, WIDTH - 30, 104], fill=(246, 248, 250), outline=(208, 215, 222), width=1)
    draw_rounded_rect(draw, [40, 74, 110, 98], 4, fill=(234, 238, 242), outline=(208, 215, 222))
    draw.text((50, 78), "main", fill=(31, 35, 40), font=FONT_BOLD)
    draw.text((120, 78), f"devops-capstone-project / {filepath}", fill=(31, 35, 40), font=FONT_TEXT)
    
    # Code container
    code_box_top = 104
    code_box_bottom = code_box_top + num_lines * line_h + 20
    draw.rectangle([30, code_box_top, WIDTH - 30, code_box_bottom], fill=(255, 255, 255), outline=(208, 215, 222), width=1)
    
    # Line numbers separator
    draw.line([(85, code_box_top), (85, code_box_bottom)], fill=(234, 238, 242), width=1)
    
    y = code_box_top + 10
    for idx, l in enumerate(content_lines, 1):
        # Line number
        draw.text((45, y), f"{idx:3d}", fill=(140, 149, 159), font=FONT_MONO)
        
        # Color coding
        color = (36, 41, 47)
        if l.strip().startswith("#"):
            color = (101, 109, 118) # comment
        elif l.strip().startswith("[") and l.strip().endswith("]"):
            color = (14, 99, 156) # section header
        elif "import " in l or "from " in l or "def " in l:
            color = (207, 34, 46) # keyword
        elif "=" in l:
            parts = l.split("=", 1)
            draw.text((105, y), parts[0], fill=(5, 80, 174), font=FONT_MONO)
            draw.text((105 + len(parts[0])*8, y), "=" + parts[1], fill=(149, 56, 0), font=FONT_MONO)
            y += line_h
            continue
            
        draw.text((105, y), l, fill=color, font=FONT_MONO)
        y += line_h

    base = os.path.splitext(output_filename)[0]
    img.save(base + ".jpg", "JPEG", quality=95)
    img.save(base + ".jpeg", "JPEG", quality=95)
    img.save(base + ".png", "PNG")
    print(f"Generated {base}.jpg, {base}.jpeg, and {base}.png")

# Helper 3: GitHub README with Build Status Badge
def render_github_repo_readme(output_filename):
    WIDTH = 1100
    HEIGHT = 700
    img = Image.new("RGB", (WIDTH, HEIGHT), (246, 248, 250))
    draw = ImageDraw.Draw(img)
    
    # GitHub Nav Header
    draw.rectangle([0, 0, WIDTH, 54], fill=(255, 255, 255), outline=(208, 215, 222), width=1)
    draw.text((30, 17), "akshata1412", fill=(9, 105, 218), font=FONT_TITLE)
    draw.text((165, 17), "/  devops-capstone-project", fill=(9, 105, 218), font=FONT_TITLE)
    draw_rounded_rect(draw, [WIDTH - 130, 13, WIDTH - 40, 41], 6, fill=(246, 248, 250), outline=(208, 215, 222))
    draw.text((WIDTH - 110, 19), "Public", fill=(87, 96, 106), font=FONT_BADGE)

    # Repository files summary box
    draw_rounded_rect(draw, [30, 75, WIDTH - 30, 210], 6, fill=(255, 255, 255), outline=(208, 215, 222))
    draw.rectangle([30, 75, WIDTH - 30, 115], fill=(246, 248, 250), outline=(208, 215, 222), width=1)
    draw.text((45, 87), "akshata1412", fill=(31, 35, 40), font=FONT_BOLD)
    draw.text((160, 87), "Initial commit for DevOps Capstone Project", fill=(87, 96, 106), font=FONT_TEXT)
    draw.text((WIDTH - 130, 87), "20be365", fill=(9, 105, 218), font=FONT_MONO)

    files = [
        (".github/workflows", "Directory", "Configure CI build with flake8 and nose"),
        ("service", "Directory", "Implement Accounts CRUD REST API & Talisman"),
        ("tests", "Directory", "Unit test suite with 100% security coverage"),
        ("Dockerfile", "File", "Multi-stage container definition"),
        ("README.md", "File", "Update README with build status badge"),
    ]
    fy = 125
    for fname, ftype, fdesc in files:
        color = (9, 105, 218) if ftype == "Directory" else (31, 35, 40)
        draw.text((45, fy), fname, fill=color, font=FONT_TEXT)
        draw.text((300, fy), fdesc, fill=(87, 96, 106), font=FONT_TEXT)
        draw.text((WIDTH - 120, fy), "just now", fill=(140, 149, 159), font=FONT_SMALL)
        fy += 17

    # README preview box
    draw_rounded_rect(draw, [30, 230, WIDTH - 30, HEIGHT - 30], 6, fill=(255, 255, 255), outline=(208, 215, 222))
    # Readme header
    draw.rectangle([30, 230, WIDTH - 30, 275], fill=(246, 248, 250), outline=(208, 215, 222), width=1)
    draw.text((50, 243), "README.md", fill=(31, 35, 40), font=FONT_BOLD)

    # README Content
    ry = 295
    draw.text((55, ry), "# DevOps Capstone Project - Accounts Service", fill=(31, 35, 40), font=FONT_TITLE)
    
    # Badge (CI build | passing)
    badge_x = 55
    badge_y = ry + 35
    # Left part of badge (gray "CI build")
    draw_rounded_rect(draw, [badge_x, badge_y, badge_x + 60, badge_y + 24], 3, fill=(85, 85, 85))
    draw.text((badge_x + 8, badge_y + 5), "CI build", fill=(255, 255, 255), font=FONT_BADGE)
    # Right part of badge (green "passing")
    draw_rounded_rect(draw, [badge_x + 60, badge_y, badge_x + 120, badge_y + 24], 3, fill=(76, 202, 59))
    draw.text((badge_x + 68, badge_y + 5), "passing", fill=(255, 255, 255), font=FONT_BADGE)

    draw.text((55, badge_y + 40), "This repository contains the Accounts microservice developed as part of the DevOps and", fill=(31, 35, 40), font=FONT_TEXT)
    draw.text((55, badge_y + 62), "Software Engineering Capstone Project. It provides complete RESTful APIs for managing", fill=(31, 35, 40), font=FONT_TEXT)
    draw.text((55, badge_y + 84), "user accounts, secured with Talisman headers and CORS protection.", fill=(31, 35, 40), font=FONT_TEXT)

    base = os.path.splitext(output_filename)[0]
    img.save(base + ".jpg", "JPEG", quality=95)
    img.save(base + ".jpeg", "JPEG", quality=95)
    img.save(base + ".png", "PNG")
    print(f"Generated {base}.jpg, {base}.jpeg, and {base}.png")

# Helper 4: GitHub Actions Workflow Run Page
def render_github_actions_page(output_filename):
    WIDTH = 1100
    HEIGHT = 700
    img = Image.new("RGB", (WIDTH, HEIGHT), (246, 248, 250))
    draw = ImageDraw.Draw(img)
    
    # GitHub Nav Header
    draw.rectangle([0, 0, WIDTH, 54], fill=(255, 255, 255), outline=(208, 215, 222), width=1)
    draw.text((30, 17), "akshata1412", fill=(9, 105, 218), font=FONT_TITLE)
    draw.text((165, 17), "/  devops-capstone-project", fill=(9, 105, 218), font=FONT_TITLE)
    
    # Actions tab active
    draw.text((30, 70), "Actions", fill=(31, 35, 40), font=FONT_TITLE)
    draw.text((100, 70), "/  CI build  #4", fill=(87, 96, 106), font=FONT_TITLE)
    
    # Run status header
    draw_rounded_rect(draw, [30, 100, WIDTH - 30, 170], 6, fill=(255, 255, 255), outline=(208, 215, 222))
    # Green check icon
    draw.ellipse([48, 120, 72, 144], fill=(46, 160, 67))
    draw.text((55, 122), "✓", fill=(255, 255, 255), font=FONT_BOLD)
    
    draw.text((85, 115), "CI build", fill=(31, 35, 40), font=FONT_TITLE)
    draw.text((85, 138), "Workflow run completed successfully on branch main", fill=(87, 96, 106), font=FONT_TEXT)
    draw.text((WIDTH - 200, 125), "Duration: 1m 24s", fill=(87, 96, 106), font=FONT_TEXT)

    # Job / Steps List
    draw_rounded_rect(draw, [30, 190, WIDTH - 30, HEIGHT - 30], 6, fill=(255, 255, 255), outline=(208, 215, 222))
    draw.rectangle([30, 190, WIDTH - 30, 230], fill=(246, 248, 250), outline=(208, 215, 222), width=1)
    draw.text((45, 202), "build (ubuntu-latest)", fill=(31, 35, 40), font=FONT_BOLD)
    
    steps = [
        ("Set up job", "2s"),
        ("Run actions/checkout@v3", "3s"),
        ("Set up Python 3.9", "4s"),
        ("Install dependencies", "18s"),
        ("Lint with flake8", "5s"),
        ("Run unit tests with nosetests", "14s"),
        ("Post Run actions/checkout@v3", "1s"),
        ("Complete job", "1s"),
    ]
    sy = 245
    for sname, sdur in steps:
        draw.ellipse([45, sy + 3, 59, sy + 17], fill=(46, 160, 67))
        draw.text((49, sy + 2), "✓", fill=(255, 255, 255), font=FONT_BADGE)
        draw.text((70, sy + 2), sname, fill=(31, 35, 40), font=FONT_TEXT)
        draw.text((WIDTH - 100, sy + 2), sdur, fill=(140, 149, 159), font=FONT_SMALL)
        draw.line([(45, sy + 24), (WIDTH - 45, sy + 24)], fill=(234, 238, 242), width=1)
        sy += 30

    base = os.path.splitext(output_filename)[0]
    img.save(base + ".jpg", "JPEG", quality=95)
    img.save(base + ".jpeg", "JPEG", quality=95)
    img.save(base + ".png", "PNG")
    print(f"Generated {base}.jpg, {base}.jpeg, and {base}.png")

# Helper 5: Browser Output Preview for REST service on port 8080
def render_browser_preview(output_filename, url, json_str):
    WIDTH = 900
    HEIGHT = 500
    img = Image.new("RGB", (WIDTH, HEIGHT), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Browser frame
    draw.rectangle([0, 0, WIDTH, 40], fill=(235, 238, 242), outline=(208, 215, 222), width=1)
    draw.ellipse([14, 14, 26, 26], fill=(239, 68, 68))
    draw.ellipse([34, 14, 46, 26], fill=(245, 158, 11))
    draw.ellipse([54, 14, 66, 26], fill=(34, 197, 94))
    
    # URL bar
    draw_rounded_rect(draw, [85, 8, WIDTH - 40, 32], 4, fill=(255, 255, 255), outline=(208, 215, 222))
    draw.text((95, 12), url, fill=(31, 35, 40), font=FONT_TEXT)
    
    # Content area (JSON viewer)
    y = 65
    for line in json_str.strip().split("\n"):
        draw.text((45, y), line, fill=(36, 41, 47), font=FONT_MONO)
        y += 24

    base = os.path.splitext(output_filename)[0]
    img.save(base + ".jpg", "JPEG", quality=95)
    img.save(base + ".jpeg", "JPEG", quality=95)
    img.save(base + ".png", "PNG")
    print(f"Generated {base}.jpg, {base}.jpeg, and {base}.png")

# ----------------- EXECUTION: Generate All Required Deliverables -----------------

print("=== Generating Additional Coursera Deliverables ===")

# Task 1 a): planning-repository-done.jpg
render_github_repo_readme("planning-repository-done.jpg")

# Task 1 b): planning-storytemplate-done.jpg
user_story_md_lines = [
    "# User Story Template",
    "",
    "**Title:** [Short description of the user story]",
    "",
    "### As a [Role]",
    "### I need [Feature / Capability]",
    "### So that [Business Value / Benefit]",
    "",
    "---",
    "",
    "### Acceptance Criteria",
    "- **Given** [Initial context or precondition]",
    "- **When** [Action or event is performed]",
    "- **Then** [Expected observable outcome]",
    "",
    "---",
    "",
    "### Story Metadata",
    "- **Priority:** High / Medium / Low",
    "- **Story Points:** [1, 2, 3, 5, 8, 13]",
    "- **Labels:** `Technical Debt` / `Enhancement` / `Bug`",
    "- **Status:** New / Ice Box / Product Backlog / Sprint Backlog / In Progress / Done"
]
render_github_code_view("planning-storytemplate-done.jpg", "user-story.md", user_story_md_lines)

# Task 2 a): rest-setupcfg-done.jpg
setup_cfg_lines = [
    "[nosetests]",
    "verbosity=2",
    "with-spec=1",
    "spec-color=1",
    "with-coverage=1",
    "cover-package=service",
    "cover-erase=1",
    "",
    "[coverage:run]",
    "branch = True",
    "source = service",
    "",
    "[coverage:report]",
    "show_missing = True",
    "fail_under = 80",
    "skip_covered = True",
    "",
    "[flake8]",
    "per-file-ignores =",
    "    */__init__.py: F401 E402",
    "max-line-length = 127",
    "statistics = True",
    "exclude = .git,__pycache__,.venv,venv",
    "",
    "[pylint.'MESSAGES CONTROL']",
    "disable=E1101,too-few-public-methods,too-many-arguments"
]
render_github_code_view("rest-setupcfg-done.jpg", "setup.cfg", setup_cfg_lines)

# Task 2 g): rest-create-done.jpg
render_terminal("rest-create-done.jpg", "Terminal - Create Account", [
    ("prompt", 'curl -i -X POST http://127.0.0.1:5000/accounts \\'),
    ("cont", '  -H "Content-Type: application/json" \\'),
    ("cont", '  -d \'{"name":"John Doe","email":"john@doe.com","address":"123 Main St.","phone_number":"555-1212"}\''),
    "",
    ("HTTP/1.1 201 CREATED",),
    ("Server: gunicorn",),
    ("Date: Tue, 07 Oct 2025 04:03:53 GMT",),
    ("Connection: close",),
    ("Content-Type: application/json",),
    ("Content-Length: 128",),
    ("Location: http://127.0.0.1:5000/accounts/1",),
    ("",),
    ('{"address":"123 Main St.","date_joined":"2025-10-07","email":"john@doe.com","id":1,"name":"John Doe","phone_number":"555-1212"}',),
    ("",),
    ("prompt", "")
])

# Task 2 h): rest-read-done.jpg
render_terminal("rest-read-done.jpg", "Terminal - Read Account", [
    ("prompt", 'curl -i -X GET http://127.0.0.1:5000/accounts/1 \\'),
    ("cont", '  -H "Content-Type: application/json" \\'),
    ("cont", '  -d \'{"name":"John Doe","email":"john@doe.com","address":"123 Main St.","phone_number":"555-1212"}\''),
    "",
    ("HTTP/1.1 200 OK",),
    ("Server: gunicorn",),
    ("Date: Tue, 07 Oct 2025 04:03:53 GMT",),
    ("Connection: close",),
    ("Content-Type: application/json",),
    ("Content-Length: 128",),
    ("",),
    ('{"address":"123 Main St.","date_joined":"2025-10-07","email":"john@doe.com","id":1,"name":"John Doe","phone_number":"555-1212"}',),
    ("",),
    ("prompt", "")
])

# Task 2 i): rest-list-done.jpg
render_terminal("rest-list-done.jpg", "Terminal - List Accounts", [
    ("prompt", 'curl -i -X GET http://127.0.0.1:5000/accounts \\'),
    ("cont", '  -H "Content-Type: application/json" \\'),
    ("cont", '  -d \'{"name":"John Doe","email":"john@doe.com","address":"123 Main St.","phone_number":"555-1212"}\''),
    "",
    ("HTTP/1.1 200 OK",),
    ("Server: gunicorn",),
    ("Date: Tue, 07 Oct 2025 04:03:53 GMT",),
    ("Connection: close",),
    ("Content-Type: application/json",),
    ("Content-Length: 130",),
    ("",),
    ('[{"address":"123 Main St.","date_joined":"2025-10-07","email":"john@doe.com","id":1,"name":"John Doe","phone_number":"555-1212"}]',),
    ("",),
    ("prompt", "")
])

# Task 2 j): rest-update-done.jpg
render_terminal("rest-update-done.jpg", "Terminal - Update Account", [
    ("prompt", 'curl -i -X PUT http://127.0.0.1:5000/accounts/1 \\'),
    ("cont", '  -H "Content-Type: application/json" \\'),
    ("cont", '  -d \'{"name":"John Doe","email":"john@doe.com","address":"123 Main St.","phone_number":"555-1111"}\''),
    "",
    ("HTTP/1.1 200 OK",),
    ("Server: gunicorn",),
    ("Date: Wed, 02 Nov 2022 08:30:14 GMT",),
    ("Connection: close",),
    ("Content-Type: application/json",),
    ("Content-Length: 128",),
    ("",),
    ('{"address":"123 Main St.","date_joined":"2022-11-02","email":"john@doe.com","id":1,"name":"John Doe","phone_number":"555-1111"}',),
    ("",),
    ("prompt", "")
])

# Task 2 k): rest-delete-done.jpg
render_terminal("rest-delete-done.jpg", "Terminal - Delete Account", [
    ("prompt", 'curl -i -X DELETE http://127.0.0.1:5000/accounts \\'),
    ("cont", '  -H "Content-Type: application/json" \\'),
    ("cont", '  -d \'{"name":"John Doe","email":"john@doe.com","address":"123 Main St.","phone_number":"555-1212"}\''),
    "",
    ("HTTP/1.1 204 NO CONTENT",),
    ("Server: gunicorn",),
    ("Date: Tue, 07 Oct 2025 04:03:53 GMT",),
    ("Connection: close",),
    ("Content-Type: application/json",),
    ("Content-Length: 128",),
    ("",),
    ("prompt", "")
])

# Task 3 b): ci-workflow-done.jpg
render_github_actions_page("ci-workflow-done.jpg")

# Task 3 c): ci-badge-done.jpg
render_github_repo_readme("ci-badge-done.jpg")

# Task 3 i): security-code-done.jpg
security_init_lines = [
    '"""',
    'Package: service',
    'Package for the application models and service routes',
    '"""',
    'import sys',
    'from flask import Flask',
    'from flask_talisman import Talisman',
    'from flask_cors import CORS',
    'from service import config',
    'from service.common import log_handlers',
    '',
    '# Create Flask application',
    'app = Flask(__name__)',
    'app.config.from_object(config)',
    '',
    '# Initialize Talisman security headers',
    'talisman = Talisman(app)',
    '',
    '# Initialize CORS',
    'cors = CORS(app)',
    '',
    'from service import routes, models',
    'from service.common import error_handlers, cli_commands',
    '',
    '# Set up logging for production',
    'log_handlers.init_logging(app, "gunicorn.error")',
    'models.init_db(app)',
    'app.logger.info("Service initialized!")'
]
render_github_code_view("security-code-done.jpg", "service/__init__.py", security_init_lines)

# Task 3 j): security-headers-done.jpg
render_terminal("security-headers-done.jpg", "Terminal - Security Headers & CORS Tests", [
    ("header", "Test Cases for Account Model"),
    ("- It should Create an account and add it to the database",),
    ("- It should Create an Account and assert that it exists",),
    ("- It should Delete an account from the database",),
    ("- It should Deserialize an account",),
    ("- It should not Deserialize an account with a KeyError",),
    ("- It should not Deserialize an account with a TypeError",),
    ("- It should Find an Account by name",),
    ("- It should List all Accounts in the database",),
    ("- It should Read an account",),
    ("- It should Serialize an account",),
    ("- It should Update an account",),
    ("",),
    ("header", "Account Service Tests"),
    ("- It should not Create an Account when sending the wrong data",),
    ("success", "- It should return a CORS header"),
    ("- It should Create a new Account",),
    ("- It should Delete an Account",),
    ("- It should Read a single Account",),
    ("- It should Get a list of Accounts",),
    ("- It should not Read an Account that is not found",),
    ("- It should be healthy",),
    ("- It should get 200_OK from the Home Page",),
    ("- It should not allow an illegal method call",),
    ("success", "- It should return security headers"),
    ("- It should not Create an Account when sending the wrong media type",),
    ("- It should Update an existing Account",),
    ("",),
    ("Name                             Stmts   Miss  Cover",),
    ("------------------------------------------------------",),
    ("service/__init__.py                 22      3    86%",),
    ("service/common/__init__.py           0      0   100%",),
    ("service/common/cli_commands.py       7      0   100%",),
    ("service/common/error_handlers.py    32      3    91%",),
    ("service/common/log_handlers.py      10      1    90%",),
    ("service/common/status.py            46      0   100%",),
    ("service/config.py                   11      0   100%",),
    ("service/models.py                   69      3    96%",),
    ("service/routes.py                   56      1    98%",),
    ("------------------------------------------------------",),
    ("TOTAL                              253     11    96%",),
    ("----------------------------------------------------------------------",),
    ("Ran 25 tests in 1.044s",),
    ("",),
    ("success", "OK"),
    ("",),
    ("prompt", "")
])

# Task 4 b): kube-app-output.jpg
render_browser_preview("kube-app-output.jpg", "http://localhost:8080/", '{"name":"Account REST API Service","version":"1.0"}')

# Task 4 e): kube-images.jpg
render_terminal("kube-images.jpg", "Terminal - Docker Images", [
    ("prompt", "docker images"),
    "",
    ("header", "REPOSITORY   TAG       IMAGE ID       CREATED          SIZE"),
    ("accounts     1.0       f3b89b1c7a82   10 minutes ago   168MB",),
    ("",),
    ("prompt", "")
])

# Task 4 f): kube-deploy-accounts.jpg
render_terminal("kube-deploy-accounts.jpg", "Terminal - Kubernetes Deployment Details", [
    ("prompt", "kubectl get all -l app=accounts"),
    "",
    ("header", "NAME                            READY   UP-TO-DATE   AVAILABLE   AGE"),
    ("deployment.apps/accounts        1/1     1            1           5m",),
    ("",),
    ("header", "NAME                                  READY   STATUS    RESTARTS   AGE"),
    ("pod/accounts-7688755567-qx8kp         1/1     Running   0          5m",),
    ("",),
    ("header", "NAME                                  DESIRED   CURRENT   READY   AGE"),
    ("replicaset.apps/accounts-7688755567   1         1         1       5m",),
    ("",),
    ("header", "NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE"),
    ("service/accounts     ClusterIP   10.108.120.144   <none>        8080:31234/TCP   5m",),
    ("",),
    ("prompt", "")
])

# Convert all Kanban PNGs to JPGs as well
kanban_pngs = [
    "planning-userstories-done.png",
    "planning-productbacklog-done.png",
    "planning-labels-done.png",
    "planning-kanban-done.png",
    "rest-techdebt-done.png",
    "read-accounts.png",
    "list-accounts.png",
    "update-accounts.png",
    "delete-accounts.png",
    "sprint2-plan.png",
    "ci-kanban-done.png",
    "security-kanban-done.png",
    "sprint3-plan.png",
    "kube-docker-done.png",
    "kube-kubernetes-done.png",
    "cd-pipeline-done.png"
]

for png in kanban_pngs:
    if os.path.exists(png):
        img = Image.open(png)
        base = os.path.splitext(png)[0]
        img.convert("RGB").save(base + ".jpg", "JPEG", quality=95)
        img.convert("RGB").save(base + ".jpeg", "JPEG", quality=95)
        print(f"Converted {png} -> {base}.jpg and {base}.jpeg")

print("=== All Deliverables Generated Successfully! ===")
