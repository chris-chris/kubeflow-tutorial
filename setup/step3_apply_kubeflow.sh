# Pick the correct config file for your platform from
# https://github.com/kubeflow/manifests/tree/[version]/kfdef
# You can download and edit the configuration at this point if you need to.
# For generic Kubernetes with Istio:
MANIFEST_BRANCH=${MANIFEST_BRANCH:-v1.0-branch}
export MANIFEST_BRANCH
MANIFEST_VERSION=${MANIFEST_VERSION:-v1.0.1}
export MANIFEST_VERSION

KF_PROJECT_NAME=${KF_PROJECT_NAME:-hello-kf}
export KF_PROJECT_NAME
mkdir "${KF_PROJECT_NAME}"
pushd "${KF_PROJECT_NAME}"

manifest_root=https://raw.githubusercontent.com/kubeflow/manifests/
# On most environments this will create a "vanilla" Kubeflow install using Istio.
FILE_NAME=kfctl_k8s_istio.${MANIFEST_VERSION}.yaml
KFDEF=${manifest_root}${MANIFEST_BRANCH}/kfdef/${FILE_NAME}
kfctl apply -f $KFDEF -V
echo $?

popd