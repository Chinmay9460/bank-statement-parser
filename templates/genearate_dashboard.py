# generate_dashboard.py

from jinja2 import Environment, FileSystemLoader

def generate_dashboard():
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template("dashboard.html")

    output = template.render()

    with open("dashboard.html", "w") as f:
        f.write(output)

    print("[INFO] Dashboard generated: dashboard.html")

if __name__ == "__main__":
    generate_dashboard()