import subprocess

if __name__ == "__main__":
    try:
        out_bytes = subprocess.check_output(['iptables','-L','-v', '-n', '-x', '--line-numvers'])
        out_text = out_bytes.decode('utf-8')
    except subprocess.CalledProcessError as e:
        out_bytes = e.output       # Output generated before error
        code      = e.returncode   # Return code