import os
import sys
import rollbar


def main():

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


rollbar.report_message("Rollbar настроен корректно", "info")

try:
    1 / 0
except Exception:
    rollbar.report_exc_info()

if __name__ == '__main__':
    main()
