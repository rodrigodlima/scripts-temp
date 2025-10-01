import subprocess
import sys
import os
from pathlib import Path

# Lê o caminho do certificado de uma variável de ambiente
CERT_FILE = os.getenv("CERT_FILE")

if not CERT_FILE:
    print("❌ Variável de ambiente CERT_FILE não definida.")
    print("   Use: export CERT_FILE=/caminho/do/certificado.crt")
    sys.exit(1)

CERT_FILE = Path(CERT_FILE)

# Nome da Podman machine (default no macOS é "podman-machine-default")
PODMAN_MACHINE = "podman-machine-default"

# Caminho onde a CA deve ser instalada na VM
# Fedora/RHEL → /etc/pki/ca-trust/source/anchors
# Debian/Ubuntu → /usr/local/share/ca-certificates
VM_CERT_PATHS = [
    "/etc/pki/ca-trust/source/anchors",
    "/usr/local/share/ca-certificates"
]

def run_cmd(cmd):
    """Executa comando e trata erros"""
    print(f"--> Executando: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERRO: {result.stderr.strip()}")
        sys.exit(result.returncode)
    return result.stdout.strip()

def main():
    if not CERT_FILE.exists():
        print(f"❌ Certificado não encontrado: {CERT_FILE}")
        sys.exit(1)

    # Copiar o certificado para a VM (ficará no $HOME dentro da VM)
    run_cmd([
        "podman", "machine", "scp", str(CERT_FILE),
        f"{PODMAN_MACHINE}:{CERT_FILE.name}"
    ])

    # Monta um comando que tenta mover para todos os paths possíveis e atualizar certificados
    ssh_cmd = " || ".join([
        f"sudo mv {CERT_FILE.name} {path}/ && (sudo update-ca-trust || sudo update-ca-certificates)"
        for path in VM_CERT_PATHS
    ])

    run_cmd(["podman", "machine", "ssh", PODMAN_MACHINE, ssh_cmd])

    print("✅ Certificado instalado com sucesso na Podman machine.")

if __name__ == "__main__":
    main()
