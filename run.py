import os

from app import create_app
import babel

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

@app.template_filter('datetime')
def format_datetime(value, fmt='medium'):
    if fmt == 'full':
        fmt = "EEEE, d. MMMM y 'at' HH:mm"
    elif fmt == 'medium':
        fmt = "EE dd/MM/y HH:mm"
    return babel.dates.format_datetime(value, fmt)

app.jinja_env.filters['datetime'] = format_datetime

if __name__ == '__main__':
    app.run()
