#!/usr/bin/with-contenv bashio

export UGREEN_NAS_API_SCHEME=$(bashio::config 'UGREEN_NAS_API_SCHEME')
export UGREEN_NAS_API_IP=$(bashio::config 'UGREEN_NAS_API_IP')
export UGREEN_NAS_API_PORT=$(bashio::config 'UGREEN_NAS_API_PORT')
export UGREEN_NAS_API_VERIFY_SSL=$(bashio::config 'UGREEN_NAS_API_VERIFY_SSL')

exec uvicorn main:app --host 0.0.0.0 --port 4115
