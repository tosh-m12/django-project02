from waitress import serve
from daily_report_project.wsgi import application

serve(application, host='0.0.0.0', port=8002)