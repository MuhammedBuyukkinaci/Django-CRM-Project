1) Install Django(Robert Solis) and Django Template by bibhasdn on VSCode.

2) Run the following commands to create an environment, then activate, then install django==3.1.4 and put the packages installed in the nevironment into a yaml file.

```
conda create --name django_crm_env python=3.8
conda activate django_crm_env
pip install django==3.1.4
conda env export | grep -v "^prefix: " > environment.yml
```