ARG BUILD_FROM
FROM ${BUILD_FROM}

# bluez provides `bluetoothctl`, which pairs/trusts the lights against the
# host's BlueZ (reached over the host D-Bus socket).
RUN apk add --no-cache bluez

# The bridge is copied from this add-on folder, never fetched at build time:
# a rebuild must produce exactly the reviewed code, not whatever a remote
# branch points at. The only download is the pinned MQTT client.
RUN pip install --no-cache-dir "paho-mqtt==2.1.0"
COPY litra_ble /app/litra_ble
ENV PYTHONPATH=/app

COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
