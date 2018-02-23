import os

from app import create_app
import babel

config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

@app.template_filter('datetime')
def format_datetime(value, custom=False, fmt='medium'):
    if not custom:
        if fmt == 'full':
            fmt = "EEEE, d. MMMM y 'at' HH:mm vvvv"
        elif fmt == 'medium':
            fmt = "EE dd/MM/y HH:mm vvvv"
            return babel.dates.format_datetime(value, fmt)
    else:
        # TODO: Implement custom date format based on user profile date format
        return babel.dates.format_datetime(value, fmt)

app.jinja_env.filters['datetime'] = format_datetime

if __name__ == '__main__':
    app.run()
