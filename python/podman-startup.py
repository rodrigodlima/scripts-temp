import subprocess
import os

# Caminho do certificado montado dentro da Podman machine
CERT_PATH_VM = "/mnt/certs/minha_ca.crt"

# Nome que o certificado terá dentro da trust store
CERT_NAME = "minha_ca.crt"

# Comandos que serão executados dentro da VM
commands = [
    f"sudo cp {CERT_PATH_VM} /etc/pki/ca-trust/source/anchors/{CERT_NAME}",
    "sudo update-ca-trust extract"
]

# Executa os comandos via `podman machine ssh`
for cmd in commands:
    print(f"Executando: {cmd}")
    subprocess.run(["podman", "machine", "ssh", cmd], check=True)

print("✅ Certificado instalado com sucesso na Podman machine.")
