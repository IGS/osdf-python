[![PyPI version](https://img.shields.io/pypi/v/osdf-python.svg)](https://pypi.python.org/pypi/osdf-python)

# osdf-python

[![Join the chat at https://gitter.im/ihmpdcc/osdf-python](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/ihmpdcc/osdf-python?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

    import pprint
    from osdf import OSDF

    server = "server.ip.dns.address"
    username = "user"
    password = "password"
    port = 8123

    osdf = OSDF(server, username, password, port)

    info = osdf.get_info()

    pprint.pprint(info)
