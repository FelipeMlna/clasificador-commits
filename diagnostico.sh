#!/bin/bash

echo " DIAGNÓSTICO DEL ENTORNO DE IA"

echo ""
echo "Sistema operativo:"
cat /etc/os-release | grep PRETTY_NAME

echo ""
echo "Arquitectura:"
uname -m

echo ""
echo "Kernel:"
uname -r

echo ""
echo "Git:"
git --version

echo ""
echo "Python:"
python3 --version

echo ""
echo "Docker:"
docker --version

echo ""
echo "Estado de Docker:"
docker info --format '{{.ServerVersion}}' 2>/dev/null || echo "Docker no disponible"

echo ""
echo "WSL:"
if grep -qi microsoft /proc/version; then
    echo "WSL detectado"
else
    echo "WSL no detectado"
fi

echo ""
echo " DIAGNÓSTICO FINALIZADO"

