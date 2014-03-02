#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moedjpack.moedj.settings")
    from django.core.management import execute_from_command_line

    if (len(sys.argv) == 2) and (sys.argv[1] == 'run'):
        execute_from_command_line(sys.argv[:1]+["runserver", "0.0.0.0:8090"])
    else:
        execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
