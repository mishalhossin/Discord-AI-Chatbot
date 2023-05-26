import subprocess

def check_and_install_packages(requirements_file='requirements.txt'):
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

    def install_packages():
        subprocess.call(['pip', 'install', '-r', requirements_file])

    missing_packages = check_packages()

    if missing_packages:
        print("The following packages are missing:")
        print('\n'.join(missing_packages))
        print("Installing missing packages...")
        install_packages()
        print("All required packages installed.")
    else:
        print("All required packages are already installed.")
