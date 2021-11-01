install

`mamba create -n ansible boto3 ansible && mamba activate ansible`

`pip install ovh`

`ansible-galaxy collection install git+https://github.com/synthesio/infra-ovh-ansible-module`

and then run 

`ansible-playbook playbook.yaml --extra-vars @secrets.yaml --extra-vars @variants.yaml`