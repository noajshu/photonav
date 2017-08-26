source cluster_env.sh

export APP_NAME="photonav"

export APP_EXTENSION="-http"

workon devops && \
    denv && \
    dbuild $APP_NAME$APP_EXTENSION:v$(gcloud/get_next_image_num.sh $APP_NAME$APP_EXTENSION) images/$APP_NAME$APP_EXTENSION/ && \
    dbuild $APP_NAME-datastore:v$(gcloud/get_next_image_num.sh $APP_NAME-datastore) images/$APP_NAME-datastore/ && \
    dpush $APP_NAME$APP_EXTENSION:v$(gcloud/get_next_image_num.sh $APP_NAME$APP_EXTENSION) && \
    dpush $APP_NAME-datastore:v$(gcloud/get_next_image_num.sh $APP_NAME-datastore) && \
    export PRIMARY_IMAGE_VERSION=$(gcloud/get_current_image_num.sh $APP_NAME$APP_EXTENSION) && \
    export DATASTORE_IMAGE_VERSION=$(gcloud/get_current_image_num.sh $APP_NAME-datastore) && \
    j2 objects/$APP_NAME/controller.yaml.j2 | kubectl delete -f -; \
    j2 objects/$APP_NAME/controller.yaml.j2 | kubectl create -f - && \
    j2 objects/$APP_NAME/service.yaml.j2 | kubectl create -f -
