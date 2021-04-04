export PLATFORM=$(uname) # Either Linux or Darwin
export KUBEFLOW_TAG=1.0.0
KUBEFLOW_BASE="https://api.github.com/repos/kubeflow/kfctl/releases"
# Or just go to https://github.com/kubeflow/kfctl/releases
wget https://github.com/kubeflow/kfctl/releases/download/v1.0/kfctl_v1.0-0-g94c35cf_darwin.tar.gz
KFCTL_FILE=${KFCTL_URL##*/}
tar -xvf "${KFCTL_FILE}"
sudo mv ./kfctl /usr/local/bin/
rm "${KFCTL_FILE}"
