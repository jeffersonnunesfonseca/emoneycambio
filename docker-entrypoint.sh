#!/bin/bash

if [ -e "/run/secrets/env_vars" ]; then
    export $(cat /run/secrets/env_vars | xargs -0)
fi

exec "$@"%  
