num=`echo "$(gcloud/get_current_image_num.sh $1) + 1" | bc 2>/dev/null`


if [[ ! -z "${num// }" ]]
    then
    echo $num
else
    echo 0
fi
