
export $WEB_SD_BACK="$PROJ_ROOT/web_sd_back"
export $WEB_SD_FRONT="$PROJ_ROOT/web_sd_front"
export $WEB_SD_AI_BACK="$PROJ_ROOT/web_sd"

node_install() {
    apt-get update
    apt-get install -y ca-certificates curl gnupg
    mkdir -p /etc/apt/keyrings
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg

    NODE_MAJOR=18
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list

    apt-get update
    apt-get install nodejs -y
}

web_sd_install () {
    cd $WEB_SD_AI_BACK
    pip install -r ./req.txt
    cd $PROJ_ROOT
    npm install
}

create_key_and_cert () {
    BACK_TMP="$WEB_SD_BACK/tmp"
    mkdir -p $BACK_TMP
    cd $BACK_TMP

    openssl genpkey -algorithm RSA -out private-key.pem -pkeyopt rsa_keygen_bits:2048
    openssl req -new -x509 -key private-key.pem -out certificate.pem -days 365
}

build_front () {
    cd $WEB_SD_FRONT
    npm run build
    cp -r "$WEB_SD_FRONT/dist" "$WEB_SD_BACK/public"
}


node_install
build_front
create_key_and_cert

web_sd_install