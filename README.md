# PLEC

To get PLEC with counts but reduntant structures reduced to a single count via clustering:

1. Make envinroment 'oddt_pull' with latest oddt from github master branch (https://oddt.readthedocs.io/en/latest/#installation)
2. Make environment 'pymol' with pymol API
3. `$ python run.py -t <TARGET> -d <DIRECTORY WITH TARGET STRUCTURES>`
4. Clustered PLEC will be in 'PLEC.json' as a list.
