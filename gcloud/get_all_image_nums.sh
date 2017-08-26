DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

curl -s -u _token:$(gcloud auth print-access-token) \
    https://$(cat $DIR/drepov2)/$1/tags/list | jsawk -n 'out(this.tags)'