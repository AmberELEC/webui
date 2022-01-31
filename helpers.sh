#!/bin/bash
#
# barrowed from batocera-es-swissknife
# https://github.com/batocera-linux/batocera.linux/blob/master/package/batocera/core/batocera-scripts/scripts/batocera-es-swissknife

# Get all childpids from calling process
function getcpid() {
    local cpids="$(pgrep -P $1)"
    for cpid in $cpids; do
        pidarray+=($cpid)
        getcpid $cpid
    done
}

# Get a sleep while process is active in background
# if PID is still active then use kill -9 switch
function smart_wait() {
    local PID=$2
    local disablekill9=$1
    local watchdog=0
    sleep 1
    while [[ -e /proc/$PID ]]; do
        sleep 0.25
        ((watchdog++))
        [[ $disablekill9 -eq 1 ]] && [[ watchdog -gt 12 ]] && kill -9 $PID
    done
}

# Emulator currently running?
function check_emurun() {
    local RC_PID="$(pgrep -f -n runemu)"
    echo $RC_PID
}

# Kill emulators running in a proper way! (SAVE SRM STATE!)
function emu_kill() {
    RC_PID=$(check_emurun)
    if [[ -n $RC_PID ]]; then
        getcpid $RC_PID
        for ((z=${#pidarray[*]}-1; z>-1; z--)); do
            kill ${pidarray[z]}
            smart_wait 1 ${pidarray[z]}
        done
        unset pidarray
    fi
}

case ${1,,} in
    --emupid)
        # This helps to detect emulator is running or not
        RC_PID=$(check_emurun)
        [[ -n $RC_PID ]] && (echo $RC_PID; exit 0) || (echo 0; exit 1)
    ;;

    --emukill)
        RC_PID=$(check_emurun)
        [[ -n $RC_PID ]] && emu_kill
    ;;
esac
