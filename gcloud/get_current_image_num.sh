DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


num=$(curl -s -u _token:$(gcloud auth print-access-token) \
    https://$(cat $DIR/drepov2)/$1/tags/list | jsawk -n 'out(this.tags)' \
    | python -c 'import sys, json, math; print int(math.ceil(max([float(o.replace("v", "")) for o in json.loads(sys.stdin.readlines()[0])])));' 2>/dev/null)


if [[ ! -z "${num// }" ]]
    then
    echo $num
else
    echo -1
fi
