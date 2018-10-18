import subprocess


def start_watching(user):
    try:
        out_bytes = subprocess.check_output(['iptables', '-A', 'OUTPUT', '-p', '-tcp', '--sport', user.port])
    except subprocess.CalledProcessError as e:
        out_bytes = e.output  # Output generated before error
        code = e.returncode  # Return code
        print out_bytes.decode('utf-8')


def check_watching(user_list):
    try:
        out_bytes = subprocess.check_output(['iptables', '-L', '-v', '-n', '-x', '--line-number'])
        out_text = out_bytes.decode('utf-8')
        print out_text
    except subprocess.CalledProcessError as e:
        out_bytes = e.output  # Output generated before error
        code = e.returncode  # Return code
        print out_bytes.decode('utf-8')


def stop_watching(user):
    try:
        out_bytes = subprocess.check_output(['iptables', '-D', 'OUTPUT', '-p', '-tcp', '--sport', user.port])
    except subprocess.CalledProcessError as e:
        out_bytes = e.output  # Output generated before error
        code = e.returncode  # Return code
        print out_bytes.decode('utf-8')


if __name__ == "__main__":
    print "monitor"
