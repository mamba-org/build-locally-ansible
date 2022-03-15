### Installation

```
mamba create -n ansible boto3 ansible ovh && mamba activate ansible
ansible-galaxy collection install git+https://github.com/dorgeln/infra-ovh-ansible-module
ansible-galaxy install mambaorg.micromamba
ansible-galaxy install geerlingguy.docker
```

### Configuration

#### OVH API key

Create an OVH API token: https://api.ovh.com/createToken/

#### OVH service name

Get your OVH service name: https://api.ovh.com/console/#/cloud/project#GET

#### OVH SSH keyid
Get your OVH SSH keyid: https://api.ovh.com/console/#/cloud/project/%7BserviceName%7D/sshkey#GET

#### Create secrets.yaml

It's not strictly necessary, but it's a good security practice to use ansible-vault for your secrets

```
openssl rand -base64 32 > ~/.vault_pass.txt`
ansible-vault create group_vars/all/secrets.yaml`
```

Configure your secrets in `group_vars/all/secrets.yaml`

```
ovh_app_key: "OVH Application Key"
ovh_app_secret: "OVH Application Secret"
ovh_consumer_key: "OVH Consumer Key"
ovh_service_name: "OVH Service Name"
ovh_ssh_keyid: "SSH KEYID"
gh_token: "Github Personal access token"
aws_key_id: "AWS KEY ID"
aws_secret_key: "AWS SECRET KEY"
aws_bucket: "conda-uploads"
```

Configure your OVH image settings in `group_vars/all/ovh.yaml`

```
ovh_endpoint: "ovh-eu"
ovh_region: "DE1"
ovh_image_id: "e1896f5f-230b-477e-925d-a7f620c363ac"
ovh_flavor_id: "3be7c73a-735a-4ee1-b8d4-83feb080109d"
ovh_user: "ubuntu"
ovh_instances:
  - ansible-builder
```

### Run Playbook

The ovh feedstock builder can be run with:

```
ansible-playbook ovh_builder.yml
```

If you want to build a specific PR you can pass a PR number as extra-vars:

```
ansible-playbook ovh_builder.yml --extra-vars "gh_pr=157"
```

