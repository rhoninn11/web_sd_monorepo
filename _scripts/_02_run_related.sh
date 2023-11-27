export $WEB_SD_BACK="$PROJ_ROOT/web_sd_back"
export $WEB_SD_FRONT="$PROJ_ROOT/web_sd_front"
export $WEB_SD_AI_BACK="$PROJ_ROOT/web_sd"


my_py_conf() {
    alias python=python3
    export PYTHONPATH="$PYTHONPATH:$WEB_SD_AI_BACK/src"
}

run_central () {
    my_py_conf
    cd $WEB_SD_AI_BACK
    python $WEB_SD_AI_BACK/serv/central/main.py
}

run_edge () {
    if [ "$#" -ne 1 ]; then
        echo "cuda dev not specified"
        return 1
    fi

    numval=$1
    port=$((6203 + numval))
    cuda_device="cuda:$numval"

    cd $WEB_SD_AI_BACK
    my_py_conf
    python $WEB_SD_AI_BACK/serv/edge/main.py $port $cuda_device
}

run_back () {
    my_wd="/root/tmp"
    web_sd_back_wd="$my_wd/web_sd_back"
    cd $web_sd_back_wd
    npm run serve
}

