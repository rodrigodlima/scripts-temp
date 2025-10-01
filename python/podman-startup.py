import subprocess

# Caminho do certificado dentro da VM (vindo do bind mount)
CERT_PATH_VM = "/mnt/certs/minha_ca.crt"
# Nome que será dado ao certificado no trust store
CERT_NAME = "minha_ca.crt"

# Lista de comandos a executar dentro da Podman machine
commands = [
    f"sudo cp {CERT_PATH_VM} /etc/pki/ca-trust/source/anchors/{CERT_NAME}",
    "sudo update-ca-trust extract"
]

def run_in_vm(cmd):
    """Executa um comando dentro da Podman machine via SSH"""
    subprocess.run(["podman", "machine", "ssh", cmd], check=True)

if __name__ == "__main__":
    for cmd in commands:
        print(f"➡️ Executando na VM: {cmd}")
        run_in_vm(cmd)

    print("✅ Certificado instalado com sucesso na Podman machine.")
