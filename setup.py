from setuptools import setup,find_packages
from typing import List
requirements = []
def get_requirements(file_path:str)->list[str]:
    
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace("\n","") for req in requirements] 
        return requirements
if '-e.' in requirements:
    requirements.remove('-e.')
setup(                          #it creates a meta data of the project file and used to install all requirement,basically project is started from here
    name='fault_detection',
    version='0.0.1',
    author='Ansuman',
    author_mail='ansumanpattnaik121@gmail.com',
    install_requirements = get_requirements('requirements.txt'),
    packages=find_packages()     #it finds all the packages inside an envirement
)

#to run setup : python setup.py install
#to run requirements : pip install -r requirements.txt