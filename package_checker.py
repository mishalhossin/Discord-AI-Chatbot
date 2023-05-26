import subprocess
import os

def check_and_install_packages(requirements_file='requirements.txt'):
    # Check if a flag file exists indicating the first run
    first_run_flag = '.first_run.flag'
    if os.path.isfile(first_run_flag):
        return

    def check_packages():
        with open(requirements_file, 'r') as file:
            packages = [line.strip() for line in file]

        missing_packages = []
        for package in packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)

        return missing_packages

    def install_package(package):
        subprocess.call(['pip', 'install', package])

    missing_packages = check_packages()

    if missing_packages:
        print("The following packages are missing:")
        print('\n'.join(missing_packages))
        print("Installing missing packages...")
        for package in missing_packages:
            print("Installing", package)
            install_package(package)
        print("All required packages installed.")

        # Create a flag file to indicate the first run
        with open(first_run_flag, 'w') as flag_file:
            pass
    else:
        print("All required packages are already installed.")

check_and_install_packages()
